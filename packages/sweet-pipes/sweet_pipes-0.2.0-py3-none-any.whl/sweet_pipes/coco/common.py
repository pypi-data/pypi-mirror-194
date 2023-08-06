from __future__ import annotations

import asyncio
import io
import json
import os
from typing import Any, Dict, Generator, List, Sequence, Tuple, Union
from zipfile import ZipFile

import torch
import wget
from PIL import Image
from torchdata.datapipes.iter import IterDataPipe

from sweet_pipes.utils.fileio import async_batch_get_request

COCO_ANNOTATIONS_URL = (
    "http://images.cocodataset.org/annotations/annotations_trainval{year}.zip"
)
TRAIN_CAPTIONS_JSON = "annotations/captions_train{year}.json"
VAL_CAPTIONS_JSON = "annotations/captions_val{year}.json"
TRAIN_INSTANCES_JSON = "annotations/instances_train{year}.json"
VAL_INSTANCES_JSON = "annotations/instances_val{year}.json"
TRAIN_KEYPOINTS_JSON = "annotations/person_keypoints_train{year}.json"
VAL_KEYPOINTS_JSON = "annotations/person_keypoints_val{year}.json"

TORCH_HUB_DIR = torch.hub.get_dir()
CACHE_DIR = os.path.join(TORCH_HUB_DIR, "coco")


def download_coco_json(cache_dir: str = CACHE_DIR, year: Union[str, int] = "2017"):
    os.makedirs(cache_dir, exist_ok=True)
    zip_path = os.path.join(cache_dir, "annotations.zip")

    if not os.path.exists(zip_path):
        print("Downloading COCO detection annotations.")
        wget.download(COCO_ANNOTATIONS_URL.format(year=year), zip_path)

    with ZipFile(zip_path, mode="r") as zip:
        train_captions_json = TRAIN_CAPTIONS_JSON.format(year=year)
        val_captions_json = VAL_CAPTIONS_JSON.format(year=year)
        if not os.path.exists(os.path.join(cache_dir, train_captions_json)):
            zip.extract(train_captions_json, path=cache_dir)
        if not os.path.exists(os.path.join(cache_dir, val_captions_json)):
            zip.extract(val_captions_json, path=cache_dir)

        train_instances_json = TRAIN_INSTANCES_JSON.format(year=year)
        val_instances_json = VAL_INSTANCES_JSON.format(year=year)
        if not os.path.exists(os.path.join(cache_dir, train_instances_json)):
            zip.extract(train_instances_json, path=cache_dir)
        if not os.path.exists(os.path.join(cache_dir, val_instances_json)):
            zip.extract(val_instances_json, path=cache_dir)

        train_keypoints_json = TRAIN_KEYPOINTS_JSON.format(year=year)
        val_keypoints_json = VAL_KEYPOINTS_JSON.format(year=year)
        if not os.path.exists(os.path.join(cache_dir, train_keypoints_json)):
            zip.extract(train_keypoints_json, path=cache_dir)
        if not os.path.exists(os.path.join(cache_dir, val_keypoints_json)):
            zip.extract(val_keypoints_json, path=cache_dir)


def get_coco_captions_json(
    split: str, year: Union[str, int] = "2017", cache_dir: str = CACHE_DIR
) -> Dict[str, List]:
    download_coco_json(cache_dir=cache_dir, year=year)

    if split == "train":
        json_file = TRAIN_CAPTIONS_JSON.format(year=year)
    elif split == "val":
        json_file = VAL_CAPTIONS_JSON.format(year=year)
    else:
        raise ValueError(f"Invalid split '{split}'. Available: ['train', 'val'].")

    with open(os.path.join(CACHE_DIR, json_file)) as f:
        return json.load(f)


def get_coco_detection_json(
    split: str, year: Union[str, int] = "2017", cache_dir: str = CACHE_DIR
) -> Dict[str, List]:
    download_coco_json(cache_dir=cache_dir, year=year)

    if split == "train":
        json_file = TRAIN_INSTANCES_JSON.format(year=year)
    elif split == "val":
        json_file = VAL_INSTANCES_JSON.format(year=year)
    else:
        raise ValueError(f"Invalid split '{split}'. Available: ['train', 'val'].")

    with open(os.path.join(CACHE_DIR, json_file)) as f:
        return json.load(f)


def get_coco_keypoints_json(
    split: str, year: Union[str, int] = "2017", cache_dir: str = CACHE_DIR
) -> Dict[str, List]:
    download_coco_json(cache_dir=cache_dir, year=year)

    if split == "train":
        json_file = TRAIN_KEYPOINTS_JSON.format(year=year)
    elif split == "val":
        json_file = VAL_KEYPOINTS_JSON.format(year=year)
    else:
        raise ValueError(f"Invalid split '{split}'. Available: ['train', 'val'].")

    with open(os.path.join(CACHE_DIR, json_file)) as f:
        return json.load(f)


InputSample = Tuple[str, Any]
OutputSample = Tuple[Image.Image, Any]


class ParallelSampleDownloader(IterDataPipe):
    def __init__(self, dp: IterDataPipe[Sequence[InputSample]]) -> None:
        super().__init__()
        self.dp = dp

    def __iter__(self) -> Generator[List[OutputSample], None, None]:
        for batch in self.dp:
            images = asyncio.run(async_batch_get_request([x[0] for x in batch]))
            anns = [x[1] for x in batch]

            batch_results = []
            for _image, _anns in zip(images, anns):
                if _image is None:
                    continue
                try:
                    image = Image.open(io.BytesIO(_image))
                    batch_results.append((image, _anns))
                except Exception:
                    continue

            yield batch_results
