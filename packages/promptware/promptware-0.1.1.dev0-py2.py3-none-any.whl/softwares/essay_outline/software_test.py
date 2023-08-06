import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import EssayOutlinePromptware  # noqa


class TestEssayOutlinePromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = EssayOutlinePromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software =EssayOutlinePromptware()

    #     input={"text": "Create an outline for "
    #     "an essay about Nikola Tesla and his "
    #     "contributions to technology:"}
    #     result = software.execute(input)
    #     print(result)
