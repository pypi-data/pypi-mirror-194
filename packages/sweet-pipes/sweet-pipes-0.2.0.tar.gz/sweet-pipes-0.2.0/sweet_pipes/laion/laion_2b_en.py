import asyncio
import io
import os
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from tempfile import TemporaryDirectory
from typing import Callable, Dict, Generator, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from PIL import Image
from torchdata.datapipes import functional_datapipe
from torchdata.datapipes.iter import IterableWrapper, IterDataPipe
from torchdata.datapipes.utils import StreamWrapper

from sweet_pipes.utils.fileio import async_batch_get_request

METADATA_URL = "https://mystic.the-eye.eu/public/AI/cah/laion5b/embeddings/laion2B-en/laion2B-en-metadata/metadata_{idx:04d}.parquet"
IMG_EMBEDDING_URL = "https://mystic.the-eye.eu/public/AI/cah/laion5b/embeddings/laion2B-en/img_emb/img_emb_{idx:04d}.npy"
TXT_EMBEDDING_URL = "https://mystic.the-eye.eu/public/AI/cah/laion5b/embeddings/laion2B-en/text_emb/text_emb_{idx:04d}.npy"
NUM_URLS = 2314


CachedFileType = Tuple[str, StreamWrapper]
LaionInputsType = Tuple[CachedFileType, CachedFileType, CachedFileType]
LaionBatchType = Tuple[pd.DataFrame, np.ndarray, np.ndarray]
LaionMetadataType = Tuple[pd.Series, np.ndarray, np.ndarray]
LaionSampleType = Tuple[Image.Image, str, Dict]


def _write_in_chunks(
    f_in: io.BufferedIOBase,
    f_out: io.BufferedIOBase,
    # Read/write chunk_size is given in bytes.  Default is 8 MiB.
    chunk_size: int = 8 * (2**20),
):
    while True:
        data = f_in.read(chunk_size)
        if not data:
            break
        f_out.write(data)


class ParallelFileCacher(IterDataPipe):
    def __init__(
        self,
        *dps: IterDataPipe[Tuple[str, io.BufferedIOBase]],
        # Read/write chunk_size is given in bytes.  Default is 8 MiB.
        chunk_size: int = 8 * (2**20),
    ) -> None:
        super().__init__()
        self.dps = dps
        self.chunk_size = chunk_size

    def __iter__(self) -> Generator[Tuple[str, StreamWrapper], None, None]:
        for inputs in zip(*self.dps):
            urls, streams = list(zip(*inputs))
            cache_dir = TemporaryDirectory()
            paths = [os.path.join(cache_dir.name, os.path.basename(u)) for u in urls]
            files = [open(path, "wb") for path in paths]

            write_fn = partial(_write_in_chunks, chunk_size=self.chunk_size)
            with ThreadPoolExecutor() as pool:
                _ = list(pool.map(write_fn, streams, files))

            _ = [f.close() for f in files]
            # Wrap the temporary directory in 'StreamWrapper', so that TorchData
            # automatically cleans it up when it goes out of context.
            yield paths, StreamWrapper(cache_dir)


@functional_datapipe("cache_local_file")
class LocalFileCacher(IterDataPipe):
    def __init__(self, dp: IterDataPipe[Tuple[str, io.BufferedIOBase]]) -> None:
        super().__init__()
        self.dp = dp

    def __iter__(self) -> Generator[Tuple[str, StreamWrapper], None, None]:
        for url, stream in self.dp:
            cache_dir = TemporaryDirectory()
            path = os.path.join(cache_dir.name, os.path.basename(url))

            with open(path, "wb") as f:
                for line in stream:
                    f.write(line)

            # Wrap the temporary directory in 'StreamWrapper', so that TorchData
            # automatically cleans it up when it goes out of context.
            yield path, StreamWrapper(cache_dir)


@functional_datapipe("read_laion_batches")
class LaionBatchReader(IterDataPipe):
    def __init__(self, dp: IterDataPipe[LaionInputsType]):
        super().__init__()
        self.dp = dp

    def __iter__(self) -> Generator[LaionBatchType, None, None]:
        for (pq_path, img_path, txt_path), _ in self.dp:
            # for (pq_path, _), (img_path, _), (txt_path, _) in self.dp:
            idx: int = 0
            parquet_file = pq.ParquetFile(pq_path)
            img_embeddings = np.load(img_path, mmap_mode="r")
            txt_embeddings = np.load(txt_path, mmap_mode="r")

            for batch in parquet_file.iter_batches():
                df = batch.to_pandas()
                num_rows = len(df)
                _img_embeddings = np.array(
                    img_embeddings[idx : idx + num_rows], copy=True
                )
                _txt_embeddings = np.array(
                    txt_embeddings[idx : idx + num_rows], copy=True
                )
                idx += num_rows

                yield df, _img_embeddings, _txt_embeddings


@functional_datapipe("iter_laion_metadata")
class LaionMetadataIterator(IterDataPipe):
    def __init__(self, dp: IterDataPipe[LaionBatchType]):
        super().__init__()
        self.dp = dp

    def __iter__(self):
        for df, img_embeds, txt_embeds in self.dp:
            for (_, row), img, txt in zip(df.iterrows(), img_embeds, txt_embeds):
                yield row, img, txt


class ParallelSampleLoader(IterDataPipe):
    def __init__(
        self,
        dp: IterDataPipe,
        max_workers: Optional[int] = 32,
        mini_batch_size: int = 16,
    ) -> None:
        super().__init__()
        self.dp = dp
        self.max_workers = max_workers
        self.mini_batch_size = mini_batch_size

    def __iter__(self) -> Generator[Tuple[str, bytes], None, None]:
        for batch in self.dp:
            rows, img_embeds, txt_embeds = list(zip(*batch))
            row_batches = [
                rows[i : i + self.mini_batch_size]
                for i in range(0, len(rows), self.mini_batch_size)
            ]
            with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
                img_batches = pool.map(
                    lambda b: asyncio.run(
                        async_batch_get_request([x["url"] for x in b])
                    ),
                    row_batches,
                )

            images = [img for img_batch in img_batches for img in img_batch]
            infos = [
                {"img_embed": img_embed, "txt_embed": txt_embed, **row.to_dict()}
                for row, img_embed, txt_embed in zip(rows, img_embeds, txt_embeds)
            ]

            batch_results = []
            for _image, info in zip(images, infos):
                if _image is None:
                    continue
                try:
                    image = Image.open(io.BytesIO(_image))
                    batch_results.append((image, info))
                except Exception:
                    continue

            yield batch_results


def _laion_datapipe(
    metadata_urls: Sequence[str],
    img_embedding_urls: Sequence[str],
    txt_embedding_urls: Sequence[str],
    filter_metadata: Optional[Callable[[LaionMetadataType], bool]] = None,
    filter_samples: Optional[Callable[[LaionSampleType], bool]] = None,
    num_threads: int = 32,
    batch_size: int = 256,
):
    # metadata_pipe = IterableWrapper(metadata_urls).read_from_http().cache_local_file()
    # img_pipe = IterableWrapper(img_embedding_urls).read_from_http().cache_local_file()
    # txt_pipe = IterableWrapper(txt_embedding_urls).read_from_http().cache_local_file()
    metadata_pipe = IterableWrapper(metadata_urls).read_from_http()
    img_pipe = IterableWrapper(img_embedding_urls).read_from_http()
    txt_pipe = IterableWrapper(txt_embedding_urls).read_from_http()

    pipe = metadata_pipe.zip(img_pipe, txt_pipe)
    pipe = ParallelFileCacher(metadata_pipe, img_pipe, txt_pipe)
    pipe = pipe.read_laion_batches().iter_laion_metadata()
    pipe = pipe.sharding_filter()

    if filter_metadata is not None:
        pipe = pipe.filter(filter_metadata)

    pipe = pipe.batch(batch_size=batch_size)
    pipe = ParallelSampleLoader(
        pipe,
        max_workers=num_threads,
        mini_batch_size=max(1, batch_size // num_threads),
    )
    pipe = pipe.unbatch()
    if filter_samples:
        pipe = pipe.filter(filter_samples)

    return pipe


def laion_2b_en(
    filter_metadata: Optional[Callable[[LaionMetadataType], bool]] = None,
    filter_samples: Optional[Callable[[LaionSampleType], bool]] = None,
    num_threads: int = 32,
    batch_size: int = 256,
) -> IterDataPipe:
    metadata_urls = [METADATA_URL.format(idx=idx) for idx in range(NUM_URLS)]
    img_embedding_urls = [IMG_EMBEDDING_URL.format(idx=idx) for idx in range(NUM_URLS)]
    txt_embedding_urls = [TXT_EMBEDDING_URL.format(idx=idx) for idx in range(NUM_URLS)]
    return _laion_datapipe(
        metadata_urls=metadata_urls,
        img_embedding_urls=img_embedding_urls,
        txt_embedding_urls=txt_embedding_urls,
        filter_metadata=filter_metadata,
        filter_samples=filter_samples,
        num_threads=num_threads,
        batch_size=batch_size,
    )


if __name__ == "__main__":
    from tqdm import tqdm

    # NUM_PROCESSES = 8
    # parquet_urls = [PARQUET_URL.format(idx=idx) for idx in range(NUM_PARQUET_FILES)]
    # shard_size = ceil(len(parquet_urls) / NUM_PROCESSES)
    # parquet_shards = [
    #     parquet_urls[i : i + shard_size]
    #     for i in range(0, len(parquet_urls), shard_size)
    # ]
    # def _run_laion_pipeline(parquet_shards, index, **kwargs):
    #     progbar = tqdm(position=index)
    #     pipe = _laion_datapipe(parquet_shards, **kwargs)
    #     for sample in pipe:
    #         progbar.update(n=1)
    # with ProcessPoolExecutor(max_workers=NUM_PROCESSES) as pool:
    #     # run_fn = partial(_run_laion_pipeline, progbar=progbar)
    #     futures = pool.map(_run_laion_pipeline, parquet_shards, range(NUM_PROCESSES))
    #     _ = list(futures)
    # import clip
    # import torch
    # device = "cuda" if torch.cuda.is_available() else "cpu"
    # model, _ = clip.load("ViT-L/14", jit=False, device=device)
    # texts = [
    #     "a picture of food on a plate",
    #     # "a picture of food without a plate",
    #     # "not a picture of food",
    # ]
    # with torch.no_grad():
    #     text_tensors = clip.tokenize(texts).to(device)
    #     text_features: torch.Tensor = model.encode_text(text_tensors)
    #     text_features /= text_features.norm(dim=-1, keepdim=True)
    # features = text_features.half().cpu().numpy()
    # def filter_metadata(row: LaionMetadataType) -> bool:
    #     series, img_embed, txt_embed = row
    #     if series["width"] < 300 or series["height"] < 300:
    #         return False
    #     img_similarity = (features @ img_embed).item()
    #     if img_similarity < 0.25:
    #         return False
    #     print(series["caption"])
    #     print(img_similarity)
    #     breakpoint()
    #     return True

    pipe = laion_2b_en(batch_size=1)
    for image, info in tqdm(pipe):
        breakpoint()
        pass
