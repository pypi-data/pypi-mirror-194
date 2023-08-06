"""Definition of design patterns for software."""
from __future__ import annotations

from enum import Enum


class DesignPatternType(str, Enum):
    """Platform types available in this tool."""

    standalone = "standalone"
    software_composition = "software-composition"
    chain_of_thought = "chain-of-thought"
    chain_of_thought_program = "chain-of-thought-program"
    chain_of_action = "chain_of_action"
    chain_of_thought_action = "chain-of-thought-action"

    @staticmethod
    def list() -> list[str]:
        """Obtains string representations of all values.

        Returns:
            List of all values in str.
        """
        return list(map(lambda c: c.value, DesignPatternType))
