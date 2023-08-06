import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import AntonymsPromptware  # noqa


class TestSentimentClassifierPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = AntonymsPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software = AntonymsPromptware()
    #     input = {"text": "correct"}
    #     result = software.execute(input)
    #     self.assertEqual(result, "incorrect")
