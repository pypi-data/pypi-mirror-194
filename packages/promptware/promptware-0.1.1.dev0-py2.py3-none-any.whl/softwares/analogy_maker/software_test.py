import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import AnalogyMakerPromptware  # noqa


class TestAnalogyMakerPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = AnalogyMakerPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software =AnalogyMakerPromptware()

    #     input={"text": "Questions are arrows in that:"}
    #     result = software.execute(input)
    #     print(result)
