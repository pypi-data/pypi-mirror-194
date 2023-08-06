import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import SummarizationPromptware  # noqa


class TestSummarizationPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = SummarizationPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute_default(self):
    #     software = SummarizationPromptware()
    #     input = {
    #         "text": "Jupiter is the fifth planet from the Sun "
    #         "and the largest in the Solar System. It is a gas "
    #         "giant with a mass one-thousandth that of the Sun, "
    #         "but two-and-a-half times that of all the other planets "
    #         "in the Solar System combined. Jupiter is one of the "
    #         "brightest objects visible to the naked eye in the night sky, "
    #         "and has been known to ancient civilizations since before recorded "
    #         "history. It is named after the Roman god Jupiter.[19] When viewed "
    #         "from Earth, Jupiter can be bright enough for its reflected light "
    #         "to cast visible shadows,[20] and is on average the third-brightest "
    #         "natural object in the night sky after the Moon and Venus."
    #     }
    #     result = software.execute(input)
    #     print(result)
    #     self.assertGreater(len(result), 0)
