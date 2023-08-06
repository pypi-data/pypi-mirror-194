import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import ScoringPromptware  # noqa


class TestScoringPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = ScoringPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software = ScoringPromptware()
    #     text = "I love this movie"
    #     result = software.execute(text)
    #     self.assertAlmostEqual(result, -3.8613948, 3)
