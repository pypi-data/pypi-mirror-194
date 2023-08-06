import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import SQLRequestPromptware  # noqa


class TestSQLRequestPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = SQLRequestPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software =SQLRequestPromptware()

    #     input={"text": "Create a SQL request to "
    #     "find all users who live in California and have over 1000 credits:"}
    #     result = software.execute(input)
    #     print(result)
