import os
import sys
import unittest

from datalabs import load_dataset

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import GaokaoReadingComprehensionPromptware  # noqa


class TestGaokaoReadingComprehensionPromptware(unittest.TestCase):
    dataset = load_dataset("gaokao2018_np1", "reading-multiple-choice")
    sample = dataset["test"][0]

    def test_write_to_directory(self):
        software = GaokaoReadingComprehensionPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software = GaokaoReadingComprehensionPromptware()
    #     input = self.sample
    # result = software.execute(input)
    # print(result)
    # self.assertEqual(result, "Cherry Blossom Bike Tour in Washington, D. C.")
