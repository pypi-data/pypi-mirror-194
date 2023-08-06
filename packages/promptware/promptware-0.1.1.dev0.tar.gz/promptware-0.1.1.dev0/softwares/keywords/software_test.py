import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import KeywordsPromptware  # noqa


class TestKeywordsPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = KeywordsPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software =KeywordsPromptware()

    #     input={"text": "Black-on-black ware is a 20th- "
    #     "and 21st-century pottery tradition developed "
    #     "by the Puebloan Native American ceramic artists "
    #     "in Northern New Mexico. "
    #     "Traditional reduction-fired blackware has been "
    #     "made for centuries by pueblo artists. "
    #     "Black-on-black ware of the past century is produced "
    #     "with a smooth surface, with the designs applied "
    #     "through selective burnishing or the application of "
    #     "refractory slip. Another style involves carving "
    #     "or incising designs and selectively polishing the raised areas. "
    #     "For generations several families from "
    #     "Kha'po Owingeh and P'ohwhóge Owingeh pueblos have been "
    #     "making black-on-black ware with the techniques "
    #     "passed down from matriarch potters. "
    #     "Artists from other pueblos have also produced "
    #     "black-on-black ware. Several contemporary artists "
    #     "have created works honoring the pottery of their ancestors."}
    #     result = software.execute(input)
    #     print(result)
