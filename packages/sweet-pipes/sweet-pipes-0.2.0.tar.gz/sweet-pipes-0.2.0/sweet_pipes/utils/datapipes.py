from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Any, Callable, Dict, Generator, List, Optional, Sequence, Tuple

import albumentations as A
import numpy as np
from torchdata.datapipes import functional_datapipe
from torchdata.datapipes.iter import IterDataPipe

from sweet_pipes.utils.albumentations import albumentations_transform

CocoInputType = Tuple[np.ndarray, Dict[str, Any]]


class AlbumentationsTransform(IterDataPipe):
    def __init__(self, dp: IterDataPipe[CocoInputType], transform: A.BasicTransform):
        super().__init__()
        self.dp = dp
        self.transform = transform

    def __iter__(self) -> Generator[CocoInputType, None, None]:
        for image, targets in self.dp:
            inputs = {"image": image, **targets}
            if self.transform is not None:
                outputs = albumentations_transform(inputs, self.transform)
            else:
                outputs = inputs

            image = outputs.pop("image")
            yield image, outputs


@functional_datapipe("batch_albumentations_transform")
class BatchAlbumentationsTransform(IterDataPipe):
    def __init__(
        self,
        dp: IterDataPipe[Sequence[CocoInputType]],
        transform: A.BasicTransform,
        max_workers: Optional[int] = None,
    ):
        super().__init__()
        self.dp = dp
        self.transform = transform
        self.max_workers = max_workers

    def __iter__(self) -> Generator[List[CocoInputType], None, None]:
        transform_fn = partial(albumentations_transform, transform=self.transform)
        for batch in self.dp:
            batch_inputs = [{"image": image, **targets} for image, targets in batch]
            with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
                batch_outputs = list(pool.map(transform_fn, batch_inputs))

            images = [output.pop("image") for output in batch_outputs]
            yield list(zip(images, batch_outputs))


@functional_datapipe("torchvision_transform")
class TorchvisionTransform(IterDataPipe):
    def __init__(
        self,
        dp: IterDataPipe[Tuple[Any, Any]],
        transform: Callable,
        target_transform: Optional[Callable] = None,
    ):
        super().__init__()
        self.dp = dp
        self.transform = transform
        self.target_transform = target_transform

    def __iter__(self) -> Generator[Tuple[Any, Any], None, None]:
        for image, target in self.dp:
            _image = self.transform(image)
            if self.target_transform is not None:
                _target = self.target_transform
            else:
                _target = target

            yield _image, _target


@functional_datapipe("batch_torchvision_transform")
class BatchTorchvisionTransform(IterDataPipe):
    def __init__(
        self,
        dp: IterDataPipe[List[Tuple[Any, Any]]],
        transform: Callable,
        target_transform: Optional[Callable] = None,
    ):
        super().__init__()
        self.dp = dp
        self.transform = transform
        self.target_transform = target_transform

    def __iter__(self) -> Generator[List[Tuple[Any, Any]], None, None]:
        def _perform_transform(inputs: Tuple[Any, Any]) -> Tuple[Any, Any]:
            image, target = inputs
            _image = self.transform(image)
            if self.target_transform is not None:
                _target = self.target_transform
            else:
                _target = target
            return _image, _target

        with ThreadPoolExecutor() as pool:
            for batch in self.dp:
                yield list(pool.map(_perform_transform, batch))
