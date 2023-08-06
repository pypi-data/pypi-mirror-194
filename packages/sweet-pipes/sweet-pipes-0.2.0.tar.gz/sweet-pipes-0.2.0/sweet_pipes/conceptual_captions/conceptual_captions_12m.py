import io
import json
import os
from typing import Dict, Tuple, Union

from PIL import Image
from torchdata.datapipes.iter import IterableWrapper, IterDataPipe

TAR_URL = "https://huggingface.co/datasets/laion/conceptual-captions-12m-webdataset/resolve/main/data/{idx:05d}.tar"
NUM_TAR_FILES = 1100


def _decode_tar(
    item: Tuple[str, io.BufferedIOBase]
) -> Tuple[str, Union[str, Dict, Image.Image]]:
    filename, stream = item
    _, ext = os.path.splitext(filename)

    if ext == ".txt":
        return filename, stream.read().decode("utf-8")
    elif ext == ".json":
        return filename, json.load(stream)
    elif ext in ".jpg":
        return filename, Image.open(stream)

    raise ValueError


def _datapipe(shuffle: bool = False) -> IterDataPipe:
    dp = IterableWrapper(
        [TAR_URL.format(idx=idx) for idx in range(NUM_TAR_FILES)], deepcopy=False
    )
    if shuffle:
        dp = dp.shuffle()

    dp = (
        dp.sharding_filter()
        .read_from_http()
        .read_from_stream()
        .map(lambda x: (x[0], io.BytesIO(x[1])))
    )

    dp = dp.load_from_tar().map(_decode_tar).webdataset()
    if shuffle:
        dp.shuffle(buffer_size=1000)

    return dp


def conceptual_captions_12m(shuffle: bool = False):
    return _datapipe(shuffle=shuffle)


if __name__ == "__main__":
    from tqdm import tqdm

    pipe = conceptual_captions_12m(shuffle=True)

    for sample in tqdm(pipe):
        # breakpoint()
        pass
