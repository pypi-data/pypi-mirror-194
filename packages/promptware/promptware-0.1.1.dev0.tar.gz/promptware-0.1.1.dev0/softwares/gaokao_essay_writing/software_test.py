import os
import sys
import unittest

from datalabs import load_dataset

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import GaokaoEssayWritingPromptware  # noqa


class TestGaokaoEssayWritingPromptware(unittest.TestCase):

    dataset = load_dataset("gaokao2018_np1", "writing-essay")
    sample = dataset["test"][0]

    def test_write_to_directory(self):
        software = GaokaoEssayWritingPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software = GaokaoEssayWritingPromptware()
    #     input = self.sample
    # result = software.execute(input)
    #
    # print(result)
    # self.assertGreater(len(result), 0)
