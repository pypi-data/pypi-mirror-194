import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import ThirdPersonConverterPromptware  # noqa


class TestThirdPersonConverterPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = ThirdPersonConverterPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software =ThirdPersonConverterPromptware()

    #     input={"text": "I decided to make a movie about Ada Lovelace."}
    #     result = software.execute(input)
    #     print(result)
