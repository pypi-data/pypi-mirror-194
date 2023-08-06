import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import ScienceFictionBookListMakerPromptware  # noqa


class TestScienceFictionBookListMakerPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = ScienceFictionBookListMakerPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software =ScienceFictionBookListMakerPromptware()

    #     input={"text": "List 10 science fiction books:"}
    #     result = software.execute(input)
    #     print(result)
