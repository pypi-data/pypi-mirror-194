import os
import sys
import unittest

from datalabs import load_dataset

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import GaokaoClozeHintPromptware  # noqa


class TestGaokaoClozeHintPromptware(unittest.TestCase):

    dataset = load_dataset("gaokao2018_np1", "cloze-hint")
    sample = dataset["test"][0]

    def test_write_to_directory(self):
        software = GaokaoClozeHintPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software = GaokaoClozeHintPromptware()
    #     input = self.sample
    #     result = software.execute(input)
    #     self.assertEqual(result, "longer")
