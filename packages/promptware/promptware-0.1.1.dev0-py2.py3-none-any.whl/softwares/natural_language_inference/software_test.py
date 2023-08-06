import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import NaturalLanguageInferencePromptware  # noqa


class TestNaturalLanguageInferencePromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = NaturalLanguageInferencePromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software = NaturalLanguageInferencePromptware()
    #     input = {
    #         "text1": "A boy is jumping on skateboard
    #         in the middle of a red bridge.",
    #         "text2": "The boy does a skateboarding trick.",
    #     }
    #     result = software.execute(input)
    #     self.assertEqual(result, "neutral")
