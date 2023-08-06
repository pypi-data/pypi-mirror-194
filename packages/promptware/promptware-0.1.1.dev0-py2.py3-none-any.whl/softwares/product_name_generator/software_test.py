import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import ProductNameGeneratorPromptware  # noqa


class TestProductNameGeneratorPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = ProductNameGeneratorPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software = ProductNameGeneratorPromptware()

    #     input={"text": "Product description: "
    #                 "A pair of shoes that can fit any foot size.\n"
    #                 "Seed words: adaptable, fit, omni-fit."}
    #     result = software.execute(input)
    #     print(result)
