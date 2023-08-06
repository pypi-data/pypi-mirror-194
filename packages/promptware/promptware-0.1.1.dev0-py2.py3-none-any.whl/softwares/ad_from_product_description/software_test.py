import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import AdFromProductDescriptionPromptware  # noqa


class TestAdFromProductDescriptionPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = AdFromProductDescriptionPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software = AdFromProductDescriptionPromptware()

    #     input = {
    #         "text": "Product: Learning Room is a virtual environment "
    #         "to help students from kindergarten to high school excel in school."
    #     }
    #     result = software.execute(input)
    #     print(result)
