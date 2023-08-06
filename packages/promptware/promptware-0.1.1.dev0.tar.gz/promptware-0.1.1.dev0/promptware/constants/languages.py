"""Definition of languages for software."""
from __future__ import annotations

from enum import Enum


class LanguageType(str, Enum):
    """Language types available in this tool."""

    zh = "zh"
    en = "en"
    python = "python"
    javascript = "javascript"
    sql = "sql"
    haskell = "haskell"
    color_code = "color-code"
    emoji = "emoji"

    @staticmethod
    def list() -> list[str]:
        """Obtains string representations of all values.

        Returns:
            List of all values in str.
        """
        return list(map(lambda c: c.value, LanguageType))
