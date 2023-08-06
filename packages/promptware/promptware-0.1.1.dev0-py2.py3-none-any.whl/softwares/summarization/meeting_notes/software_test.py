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

    # def test_execute_meeting_notes(self):
    #     software = SummarizationPromptware()
    #     input = {"text": "Tom: Profits up 50%\n"
    #              "Jane: New servers are online\n"
    #              "Kjel: Need more time to fix software\n"
    #              "Jane: Happy to help\n"
    #              "Parkman: Beta testing almost done\n"}
    #     result = software.execute(input)
    #     print(result)
    #     self.assertGreater(len(result), 0)
