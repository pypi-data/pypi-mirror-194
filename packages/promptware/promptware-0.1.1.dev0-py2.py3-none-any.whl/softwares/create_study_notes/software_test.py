import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import CreateStudyNotesPromptware  # noqa


class TestCreateStudyNotesPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = CreateStudyNotesPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software =CreateStudyNotesPromptware()

    # input={"text": "What are 5 key points "
    # "I should know when studying Ancient Rome?"}
    #     result = software.execute(input)
    #     print(result)
