from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Sequence, Tuple

from PIL import Image
from torchdata.datapipes.iter import IterableWrapper, IterDataPipe

from sweet_pipes.coco.common import ParallelSampleDownloader, get_coco_captions_json


def _get_captions_by_image_id(annotations: Sequence[Dict]) -> Dict[int, List[str]]:
    out: Dict[int, List[str]] = defaultdict(list)
    for ann in annotations:
        image_id = ann["image_id"]
        out[image_id].append(ann["caption"])

    return out


def coco_captions(
    split: str = "train",
    buffer_size: int = 128,
) -> IterDataPipe[Tuple[Image.Image, List[str]]]:
    captions_json = get_coco_captions_json(split=split)
    images, annotations = captions_json["images"], captions_json["annotations"]
    captions_by_image_id = _get_captions_by_image_id(annotations)
    images_with_captions = [
        (image["coco_url"], captions_by_image_id[image["id"]]) for image in images
    ]

    pipe: IterDataPipe = IterableWrapper(images_with_captions, deepcopy=False)
    pipe = pipe.batch(buffer_size)
    pipe = ParallelSampleDownloader(pipe)
    pipe = pipe.unbatch()

    return pipe


if __name__ == "__main__":
    pipe = coco_captions()
    for image, captions in pipe:
        breakpoint()
        pass
