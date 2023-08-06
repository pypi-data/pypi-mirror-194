import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import SentimentClassifierPromptware  # noqa


class TestSentimentClassifierPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = SentimentClassifierPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software = SentimentClassifierPromptware()
    #     input = {"text": "I love this movie."}
    #     # print complete prompt info for a given example
    #     # print(software.to_code(input))
    #     result = software.execute(input)
    #     self.assertEqual(result, "positive")
