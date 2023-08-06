import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import SpreadsheetCreatorPromptware  # noqa


class TestSpreadsheetCreatorPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = SpreadsheetCreatorPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software =SpreadsheetCreatorPromptware()

    #     input={"text": "A two-column spreadsheet "
    #     "of top science fiction movies and the year of release:\n\n"
    #     "Title |  Year of release"}
    #     result = software.execute(input)
    #     print(result)
