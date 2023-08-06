from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Any


@dataclass
class KernelConfig:
    @abc.abstractmethod
    def to_kernel(self) -> Kernel:
        return Kernel(self)


class Kernel:
    def __init__(self, config: Any):
        self.config = config
