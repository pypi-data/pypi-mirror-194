import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import SQLTranslatePromptware  # noqa


class TestSQLTranslatePromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = SQLTranslatePromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software =SQLTranslatePromptware()

    #     input={"text": "A query to list the names of the departments "
    #             "which employed more than 10 employees in the last 3 months\nSELECT"}
    #     result = software.execute(input)
    #     print(result)
