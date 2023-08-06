import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import GrammarCorrectionPromptware  # noqa


class TestGrammarCorrectionPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = GrammarCorrectionPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    """
    def test_execute(self):
        software = GrammarCorrectionPromptware(config_name="default")
        input = {"text": "She no went to the market."}
        result = software.execute(input)
        print(result)
        self.assertGreater(len(result), 0)
    """
