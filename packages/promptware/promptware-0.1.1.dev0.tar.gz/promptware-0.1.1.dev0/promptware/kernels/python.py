from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from promptware.kernels.kernel import Kernel, KernelConfig


@dataclass
class PythonKernelConfig(KernelConfig):
    version: str = "3.9"

    def to_kernel(self) -> Kernel:
        return PythonKernel()


class PythonKernel(Kernel):
    def __init__(self, globals: Optional[dict] = None, locals: Optional[dict] = None):
        self.globals = globals if globals is not None else {}
        self.locals = locals if locals is not None else {}

    def execute(self, input: str) -> dict:
        try:
            exec(input, self.globals, self.locals)
            return self.locals
        except Exception as err:
            print(f"Error executing python script: {err}")
            return {}
