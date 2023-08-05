#  Copyright (c) 2021 GradsFlow. All rights reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import dataclasses
import logging
from typing import Optional

import pytorch_lightning as pl
from torch.utils.data import DataLoader, Dataset

from gradsflow.data.ray_dataset import RayDataset

logger = logging.getLogger("core.data")


@dataclasses.dataclass(init=False)
class Data:
    dataloader: DataLoader
    dataset: [RayDataset, Dataset]


class AutoDataset:
    def __init__(
        self,
        train_dataloader: Optional[DataLoader] = None,
        val_dataloader: Optional[DataLoader] = None,
        datamodule: Optional[pl.LightningDataModule] = None,
        num_classes: Optional[int] = None,
    ):

        self.meta = {}
        self.datamodule = None
        self.train_dataloader = train_dataloader
        self.val_dataloader = val_dataloader
        self.num_classes = num_classes

        if (datamodule or train_dataloader) is None:
            raise UserWarning("Both datamodule and train_dataloader can't be None!")

        if all((datamodule, train_dataloader)):
            logger.warning("Both datamodule and train_dataloader is set! Using datamodule over train_dataloader.")

        if not datamodule:
            self.train_dataloader = train_dataloader
            self.val_dataloader = val_dataloader
            self.num_classes = num_classes

        elif isinstance(datamodule, pl.LightningDataModule):
            self.datamodule = datamodule
            self.train_dataloader = datamodule.train_dataloader()
            self.val_dataloader = datamodule.val_dataloader()
            if hasattr(datamodule, "num_classes"):
                self.num_classes = datamodule.num_classes
            if hasattr(datamodule, "num_labels"):
                self.meta["num_labels"] = datamodule.num_labels

        self.meta["num_classes"] = self.num_classes
