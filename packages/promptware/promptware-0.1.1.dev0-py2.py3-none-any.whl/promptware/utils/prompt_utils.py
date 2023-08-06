"""Utilities for promptware."""

from __future__ import annotations

from collections.abc import Callable
import inspect


def get_code_as_string(func_name: Callable) -> str:

    if not callable(func_name):
        raise ValueError(f"Function {func_name} is not callable")

    return inspect.getsource(func_name).strip()


def get_template(prompt_template: Callable) -> str:
    return get_code_as_string(prompt_template).split("=")[-1]
