from __future__ import annotations

import logging
from typing import Any, Callable, Dict, Optional, Type, TypeVar

import albumentations as A
import numpy as np
import torch
from albumentations.core.bbox_utils import BboxProcessor
from albumentations.core.keypoints_utils import KeypointsProcessor

logger = logging.getLogger(__name__)
T = TypeVar("T")

# Constants for `albumentations` transformations.  By default, bounding boxes and
# keypoints are not affected by these, so we include additional processors when
# they are present.  See '_prepare_transform' for more details.
MAX_TRANSFORM_RETRIES = 30
LABEL_FIELDS = ["labels"]
BBOX_PROCESSOR = BboxProcessor(
    A.BboxParams(format="pascal_voc", label_fields=LABEL_FIELDS)
)
KEYPOINTS_PROCESSOR = KeypointsProcessor(
    A.KeypointParams(format="xy", label_fields=LABEL_FIELDS)
)


def is_valid_batch(batch: Dict[str, Any]) -> bool:
    if "labels" in batch:
        pass
    if "bboxes" in batch:
        bb = np.asarray(batch["bboxes"])
        if bb.size == 0:
            # No bboxes in array
            return False
        if (bb < 0).any():
            # Negative coordinates
            return False
        if (bb[:, 2] <= bb[:, 0]).any():
            # Non-positive width
            return False
        if (bb[:, 3] <= bb[:, 1]).any():
            # Non-positive height
            return False
    if "mask" in batch:
        pass
    if "segm" in batch:
        pass
    if "keypoints" in batch:
        pass
    return True


def _cast_to_array(value: Any, array_type: Type, dtype: Optional[str] = None):
    cast_to_tensor: Callable = lambda x: torch.atleast_1d(
        torch.from_numpy(np.array(x, dtype=dtype, copy=False))
    )

    if issubclass(array_type, torch.Tensor):
        return cast_to_tensor(value)
    elif issubclass(array_type, np.ndarray):
        return np.atleast_1d(np.array(value, dtype=dtype, copy=False))
    else:
        raise TypeError(f"Could not cast value of type {type(value)} to array.")


def _conditional_cast_to_array(
    value: Any, array_type: Type, dtype: Optional[str] = None
) -> Any:
    try:
        return _cast_to_array(value, array_type, dtype=dtype)
    except:  # noqa E722
        return value


def _clip_boxes_to_image_bounds(
    boxes: np.ndarray, nrows: int, ncols: int
) -> np.ndarray:
    out = np.copy(boxes)
    # Clip x coordinates to image bounds
    out[:, 0] = boxes[:, 0].clip(0, ncols - 1e-8)
    out[:, 2] = boxes[:, 2].clip(1e-8, ncols)
    # Clip y coordinates to image bounds
    out[:, 1] = boxes[:, 1].clip(0, nrows - 1e-8)
    out[:, 3] = boxes[:, 3].clip(1e-8, nrows)
    return out


def _prepare_for_transform(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare the raw sample values to pass them into an 'albumentations'
    transform.  Rename fields to match 'albumentations' conventions (which
    are different from the desired COCO output format), and rearrange/reshape
    arrays where needed.

    Args:
        raw (Dict[str, Any]): Dictionary of raw sample values

    Returns:
        Dict[str, Any]: Reformatted sample values, such that they conform
            to 'albumentations' conventions.
    """
    out = {}
    out["image"] = np.array(raw["image"], dtype=np.uint8, copy=False)
    if "labels" in raw:
        out["labels"] = np.array(raw["labels"], copy=False)
    if "masks" in raw:
        # Rename 'masks' -> 'mask'
        masks: np.ndarray = raw["masks"]
        # Rearrange from (chan, height, width) -> (height, width, chan)
        h, w = masks.shape[-2:]
        out["mask"] = masks.reshape(-1, h, w).transpose((1, 2, 0))
    if "segm" in raw:
        segm: np.ndarray = raw["segm"]
        # Rearrange from (chan, height, width) -> (height, width, chan)
        h, w = segm.shape[-2:]
        out["segm"] = segm.reshape(-1, h, w).transpose((1, 2, 0))
    if "boxes" in raw:
        # Clip bounding boxes to the dimensions of the image/mask.
        # Allows for labeling (or manual hacking) errors in bounding boxes
        # without breaking the 'albumentations' transforms.
        h, w = out["image"].shape[:2]
        out["bboxes"] = _clip_boxes_to_image_bounds(raw["boxes"], nrows=h, ncols=w)

    return out


def _perform_transform(
    prepared: Dict[str, Any],
    transform: A.BasicTransform,
    max_retries: int = MAX_TRANSFORM_RETRIES,
):
    """Perform the 'albumentations' transform on a reformatted dictionary
    of sample values.  We pipe the image, labels, bounding boxes, segmentation
    masks, and keypoints into 'kwargs' for the transform.

    NOTE: Reconfigure the supplementary processors (bboxes or keypoints) for
    each sample.  Allows bounding boxes and/or keypoints to be present in some
    samples, but not others. (Exception is raised if BBOX_PROCESSOR is present,
    but no "bboxes" field is available in the sample.)

    Args:
        prepared (Dict[str, Any]): [description]

    Returns:
        [type]: [description]
    """
    if not is_valid_batch(prepared):
        # ensure the input is valid to be sure that an invalid batch caught
        # later is due to the transform.
        raise ValueError("Invalid batch received before transform")
    kwargs = {"image": prepared["image"]}
    processors = {}

    if "labels" in prepared:
        kwargs["labels"] = prepared["labels"]
    if "bboxes" in prepared:
        kwargs["bboxes"] = prepared["bboxes"]
        if isinstance(transform, A.Compose):
            processors["bboxes"] = BBOX_PROCESSOR
    if "mask" in prepared:
        kwargs["mask"] = prepared["mask"]
    if "segm" in prepared:
        kwargs["segm"] = prepared["segm"]
    if "keypoints" in prepared:
        kwargs["keypoints"] = prepared["keypoints"]
        if isinstance(transform, A.Compose):
            processors["keypoints"] = KEYPOINTS_PROCESSOR

    if isinstance(transform, A.Compose):
        if "segm" in kwargs:
            transform = A.Compose(
                transform.transforms,
                additional_targets={"segm": "mask"},
            )
        transform.processors = processors

    transformed = transform(**kwargs)
    retry_count: int = 0
    while not is_valid_batch(transformed):
        # Ensure that transform did not mangle things
        retry_count += 1
        if retry_count > max_retries:
            raise ValueError(
                f"Transform caused invalid batch. Retried {max_retries} times"
            )
        logger.warn(f"Augmentation caused invalid batch. Retry: {retry_count}")
        transformed = transform(**kwargs)
    return transformed


def _renormalize_keys_after_transform(
    raw: Dict[str, Any], target: Dict[str, Any]
) -> Dict[str, Any]:
    """Reformat field names after performing the 'albumentations' transform.
    Generally, this means converting to COCO conventions.

    Args:
        raw (Dict[str, Any]): Raw sample dictionary, containing unaltered keys.
        target (Dict[str, Any]): Processed sample, after normalizing keys and
            transforming with 'albumentations'.

    Returns:
        Dict[str, Any]: Sample with renormalized keys in COCO format.
    """
    if "masks" in raw:
        target["masks"] = np.transpose(target.pop("mask"), (2, 0, 1))
    if "segm" in raw:
        target["segm"] = np.transpose(target.pop("segm"), (2, 0, 1))
    if "boxes" in raw:
        target["boxes"] = target.pop("bboxes")

    return target


def _cast_to_arrays(target: Dict[str, Any]) -> Dict[str, Any]:
    """Attempt to cast all arrays in the target dictionary to Tensor values.  If
    any value cannot be cast to Tensor, return it unaltered.

    Args:
        target (Dict[str, Any]): Sample dictionary with non-Tensor values.

    Returns:
        Dict[str, Any]: Sample dictionary with Tensor values, where possible.
    """
    array_type = type(target["image"])
    if "boxes" in target:
        target["boxes"] = _cast_to_array(
            target["boxes"], array_type, "float32"
        ).reshape(-1, 4)
    if "masks" in target:
        target["masks"] = _cast_to_array(target["masks"], array_type, "uint8")
    if "segm" in target:
        target["segm"] = _cast_to_array(target["segm"], array_type, "uint8")
    if "labels" in target:
        target["labels"] = _cast_to_array(target["labels"], array_type, "int64")
    if "image_id" in target:
        target["image_id"] = _cast_to_array(target["image_id"], array_type, "int64")
    if "iscrowd" in target:
        target["iscrowd"] = _cast_to_array(target["iscrowd"], array_type, "int64")

    return {k: _conditional_cast_to_array(v, array_type) for k, v in target.items()}


def albumentations_transform(
    inputs: Dict[str, Any], transform: A.BasicTransform
) -> Dict[str, Any]:
    prepared = _prepare_for_transform(inputs)
    out = _perform_transform(prepared, transform)
    out = _renormalize_keys_after_transform(inputs, out)

    target = {**inputs, **out}
    target = _cast_to_arrays(target)

    return target
