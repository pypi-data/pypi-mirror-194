"""Utilities for Logprobs."""

from __future__ import annotations


def average_logprobs(
    token_logprobs: list[float],
    tokens: list[str],
    start_token: str | None = None,
    end_token: str = "<|endoftext|>",
) -> float:
    """
    Compute the average log-prob of a sequence of token sequences.

    Parameters
    ----------
    token_logprobs : list[float]
        A list of log-probabilities.
    tokens : list[str]
    """

    start_token_index = (
        0
        if start_token is None or start_token not in tokens
        else len(tokens) - tokens[::-1].index(start_token) - 1
    )
    end_token_index = (
        len(tokens) if end_token not in tokens else tokens.index(end_token)
    )

    if end_token_index == 0:
        raise ValueError(f"there is no valid token: {tokens[0]}")
    if start_token_index >= end_token_index:
        raise ValueError(f"illegal start token {start_token}")

    return sum(token_logprobs[start_token_index:end_token_index]) / (
        end_token_index - start_token_index
    )
