"""Unit test for Scoring."""

import os
import unittest

import openai

os_api_key = os.getenv("OS_API_KEY")
openai.api_key = os_api_key


class TestScoring(unittest.TestCase):
    def test_score(self):
        response = openai.Completion.create(
            model="text-curie-001",
            prompt="I love this movie.",
            temperature=0,
            max_tokens=10,
            logprobs=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            n=1,
            echo=False,
        )
        out = response["choices"][0]
        print(out)
