from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class DatasetConfig:
    dataset_name: str
    sub_dataset: Optional[str] = None
    split_name: str = "test"
    n_samples: int = 3
