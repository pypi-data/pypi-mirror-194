"""Definition of platforms for software."""
from __future__ import annotations

from enum import Enum


class PlatformType(str, Enum):
    """Platform types available in this tool."""

    gpt3 = "gpt3"
    chatgpt = "chatgpt"
    cohere = "cohere"
    youchat = "youchat"
    huggingface = "huggingface"

    @staticmethod
    def list() -> list[str]:
        """Obtains string representations of all values.

        Returns:
            List of all values in str.
        """
        return list(map(lambda c: c.value, PlatformType))
