import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import MathCalculationPromptware  # noqa


class TestMathCalculationPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = MathCalculationPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software = MathCalculationPromptware()
    #     input = {"question": "what's the result of 1 + 3?"}
    #   # input = {"question": "what's the result of 16 * 333?"}
    #     result = software.execute(input)
    #     print(result)
    #     self.assertEqual(result, "4")
