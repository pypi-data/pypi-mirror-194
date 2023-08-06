import asyncio
import io
from concurrent.futures import ThreadPoolExecutor
from typing import Generator, Optional, Tuple

from PIL import Image
from torchdata.datapipes.iter import HttpReader, IterDataPipe, LineReader

from sweet_pipes.utils.fileio import async_batch_get_request

TSV_URLS = {
    "train": "https://storage.googleapis.com/gcc-data/Train/GCC-training.tsv?_ga=2.191230122.-1896153081.1529438250",
    "val": "https://storage.cloud.google.com/gcc-data/Validation/GCC-1.1.0-Validation.tsv?_ga=2.141047602.-1896153081.1529438250",
}


class BatchSampleLoader(IterDataPipe):
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
            mini_batches = [
                batch[i : i + self.mini_batch_size]
                for i in range(0, len(batch), self.mini_batch_size)
            ]
            with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
                image_batches = pool.map(
                    lambda b: asyncio.run(async_batch_get_request([x[1] for x in b])),
                    mini_batches,
                )

            images = [img for mini_batch in image_batches for img in mini_batch]
            captions = [x[0] for x in batch]

            batch_results = []
            for _image, caption in zip(images, captions):
                if _image is None:
                    continue
                try:
                    image = Image.open(io.BytesIO(_image))
                    batch_results.append((image, caption))
                except Exception:
                    continue

            yield batch_results


def _base_datapipe(tsv_url: str, batch_size: int = 256) -> IterDataPipe:
    pipe = HttpReader([tsv_url])
    pipe = LineReader(pipe, return_path=False)
    pipe = pipe.map(lambda line: line.decode("utf-8").split("\t"))

    pipe = pipe.batch(batch_size=batch_size)
    pipe = BatchSampleLoader(pipe)
    pipe = pipe.unbatch()

    return pipe


def conceptual_captions_3m(split: str = "train") -> IterDataPipe:
    return _base_datapipe(tsv_url=TSV_URLS[split])


if __name__ == "__main__":
    from tqdm import tqdm

    pipe = conceptual_captions_3m()
    for sample in tqdm(pipe):
        pass
