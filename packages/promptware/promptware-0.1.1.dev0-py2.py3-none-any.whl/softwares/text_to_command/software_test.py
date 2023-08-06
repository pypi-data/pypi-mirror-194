import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import TextToCommandPromptware  # noqa


class TestTextToCommandPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = TextToCommandPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software = TextToCommandPromptware()

    #     input = {
    #         "text": "Reach out to the ski store and "
    #         "figure out if I can get my skis fixed before I leave on Thursday\n"
    #     }

    #     result = software.execute(input)
    #     self.assertGreater(len(result), 0)
