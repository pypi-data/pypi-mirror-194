from typing import Iterable, Optional, Tuple, TypeVar, Union

import numpy as np
from torchdata.dataloader2 import DataLoader2
from torchdata.dataloader2.adapter import Adapter
from torchdata.dataloader2.reading_service import ReadingServiceInterface
from torchdata.datapipes import functional_datapipe
from torchdata.datapipes.map import MapDataPipe

from pyPhasesML.DataAugmentation import DataAugmentation

T_co = TypeVar("T_co", covariant=True)


@functional_datapipe("unzipXY")
class ZipperMapDataPipe(MapDataPipe[Tuple[T_co, ...]]):
    datapipes: Tuple[MapDataPipe[T_co], ...]

    def __init__(self, datapipe: MapDataPipe[T_co]) -> None:
        self.datapipe = datapipe

    def __getitem__(self, index) -> Tuple[T_co, ...]:
        x, y = zip(*self.datapipe[index])
        return np.array(x), np.array(y)

    def __len__(self) -> int:
        return len(self.datapipe)


class AugmentationDataset(MapDataPipe):
    def __init__(self, dataExporterSignals, dataExporterFeatures, augmentationSteps, splitName):
        self.dataExporterSignals = dataExporterSignals
        self.dataExporterFeatures = dataExporterFeatures
        self.augmentationSteps = augmentationSteps

    def __len__(self):
        return len(self.dataExporterSignals)

    def __getitem__(self, idx):
        segmentX, segmentY = self.dataExporterSignals[idx], self.dataExporterFeatures[idx]
        # convert to numpy arrays
        return np.array(segmentX), np.array(segmentY)


class AugmentationDataLoaderXY(DataLoader2):
    def __init__(
        self,
        dataset: AugmentationDataset,
        dataAugmentation: DataAugmentation,
        batchSize,
        datapipe_adapter_fn: Optional[Union[Iterable[Adapter], Adapter]] = None,
        reading_service: Optional[ReadingServiceInterface] = None,
    ) -> None:
        datapipe = dataset.map(dataAugmentation)
        datapipe = datapipe.batch(batchSize)
        datapipe = datapipe.unzipXY()
        super().__init__(datapipe, datapipe_adapter_fn, reading_service)

    def __len__(self):
        return len(self.datapipe)
    
    def generator(self):
        while True:
            for d in self:
                yield d
