"""Unittest for logprobs_utils."""

from __future__ import annotations

import unittest

from promptware.utils.logprobs_utils import average_logprobs


class MyTestCase(unittest.TestCase):
    token_logprobs = [
        -0.3848996,
        -0.0003108397,
        -0.3952032,
        -1.5530591,
        -0.23971762,
        -0.39673945,
        -0.00012346054,
        -8.065993e-05,
        -0.00017007865,
        -0.026155638,
    ]
    tokens = [
        "\n",
        "\n",
        "I",
        " do",
        " not",
        " like",
        " this",
        " movie",
        ".",
        "<|endoftext|>",
    ]

    def test_default_value(self):

        score1 = average_logprobs(
            token_logprobs=self.token_logprobs, tokens=self.tokens
        )
        self.assertAlmostEqual(score1, -0.3300, places=3)

    def test_end_token(self):

        score2 = average_logprobs(
            token_logprobs=self.token_logprobs,
            tokens=self.tokens,
            end_token="|||",
        )

        self.assertAlmostEqual(
            score2, sum(self.token_logprobs) / len(self.token_logprobs), places=3
        )

    def test_start_end_token(self):

        score3 = average_logprobs(
            token_logprobs=self.token_logprobs,
            tokens=self.tokens,
            start_token="I",
            end_token=" not",
        )
        self.assertAlmostEqual(score3, (-0.3952032 - 1.5530591) / 2, places=3)


if __name__ == "__main__":
    unittest.main()
