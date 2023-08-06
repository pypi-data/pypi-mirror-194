import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import LinguisticAcceptabilityClassificationPromptware  # noqa


class TestLinguisticAcceptabilityClassificationPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = LinguisticAcceptabilityClassificationPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software = LinguisticAcceptabilityClassificationPromptware()
    #     input = {"text": "Bill pushed Harry off the sofa."}
    #     result = software.execute(input)
    #     self.assertEqual(result, "yes")
