import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import PromptEngineerPromptware  # noqa


class TestPromptEngineerPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = PromptEngineerPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software = PromptEngineerPromptware()
    #     input = [
    #         ("aperiodic", "periodic"),
    #         ("unsent", "sent"),
    #     ]
    #     result = software.execute(input)
    #
    #     self.assertEqual(result["text"], "the antonym of the word.")
    #     self.assertAlmostEqual(
    #         result["score"],
    #         -0.166913920455,
    #         1,
    #     )
