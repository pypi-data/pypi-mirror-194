import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import MicroHorrorStoryCreatorPromptware  # noqa


class TestMicroHorrorStoryCreatorPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = MicroHorrorStoryCreatorPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software =MicroHorrorStoryCreatorPromptware()

    #     input={"text": "Topic: Wind\nTwo-Sentence Horror Story:"}
    #     result = software.execute(input)
    #     print(result)
