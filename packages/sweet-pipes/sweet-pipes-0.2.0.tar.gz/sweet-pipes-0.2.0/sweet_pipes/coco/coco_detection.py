from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, Generator, List, Sequence, Tuple, Union

import numpy as np
import pycocotools.mask as mask_utils
from PIL import Image
from torchdata.datapipes.iter import IterableWrapper, IterDataPipe

from sweet_pipes.coco.common import ParallelSampleDownloader, get_coco_detection_json


def _get_annotations_by_image_id(annotations: Sequence[Dict]) -> Dict[int, List[Dict]]:
    out: Dict[int, List[Dict]] = defaultdict(list)
    for ann in annotations:
        image_id: int = ann["image_id"]
        out[image_id].append(ann)

    return out


def _ann_to_rle(ann: Dict[str, Any], height: int, width: int) -> np.ndarray:
    segm = ann["segmentation"]
    if type(segm) == list:
        # polygon -- a single object might consist of multiple parts
        # we merge all parts into one mask rle code
        rles = mask_utils.frPyObjects(segm, height, width)
        rle = mask_utils.merge(rles)
    elif type(segm["counts"]) == list:
        # uncompressed RLE
        rle = mask_utils.frPyObjects(segm, height, width)
    else:
        # rle
        rle = ann["segmentation"]
    return rle


def _ann_to_mask(ann: Dict[str, Any], height: int, width: int) -> np.ndarray:
    return mask_utils.decode(_ann_to_rle(ann, height=height, width=width))


def _xywh_to_xyxy(box: Sequence[float]) -> Tuple[float, float, float, float]:
    xmin, ymin, width, height = box
    return (xmin, ymin, xmin + width, ymin + height)


class FormatAnnotations(IterDataPipe):
    def __init__(
        self,
        dp: IterDataPipe[Tuple[Image.Image, List[Dict]]],
        include_masks: bool = True,
    ) -> None:
        super().__init__()
        self.dp = dp
        self.include_masks = include_masks

    def __iter__(self) -> Generator[Tuple[Image.Image, Dict], None, None]:
        for image, anns in self.dp:
            targets = {
                "labels": np.array([a["category_id"] for a in anns]),
                "areas": np.array([a["area"] for a in anns]),
                "boxes": np.array([_xywh_to_xyxy(a["bbox"]) for a in anns]),
            }
            if self.include_masks:
                height, width = image.height, image.width
                targets["masks"] = np.array(
                    [_ann_to_mask(a, height=height, width=width) for a in anns]
                )

            if image.mode != "RGB":
                image = image.convert("RGB")

            yield image, targets


def coco_detection(
    split: str = "train",
    year: Union[str, int] = "2017",
    shuffle: bool = False,
    buffer_size: int = 128,
    include_masks: bool = True,
) -> IterDataPipe[Tuple[Image.Image, Dict]]:
    detection_json = get_coco_detection_json(split=split, year=year)
    images, annotations = detection_json["images"], detection_json["annotations"]
    anns_by_image_id = _get_annotations_by_image_id(annotations)
    images_with_anns = [
        (image["coco_url"], anns_by_image_id[image["id"]]) for image in images
    ]

    pipe: IterDataPipe = IterableWrapper(images_with_anns, deepcopy=False)
    if shuffle:
        pipe = pipe.shuffle()

    pipe = pipe.batch(buffer_size)
    pipe = ParallelSampleDownloader(pipe)
    pipe = pipe.unbatch()
    pipe = FormatAnnotations(pipe, include_masks=include_masks)

    return pipe
