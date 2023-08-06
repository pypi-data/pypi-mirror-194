"""Unittest for huggingface.py"""

import unittest

from promptware.kernels.api import huggingface


class TestHuggingface(unittest.TestCase):
    @unittest.skip("large model is required")
    def test_get_model_card(self):
        model_name = "facebook/opt-350m"
        prompt = "Today is a good day. Let's"
        response = huggingface.generate(
            model_name,
            prompt,
            do_sample=False,
            num_beams=2,
        )
        print(response["text"])
        self.assertTrue(len(response["text"]) > 0)
