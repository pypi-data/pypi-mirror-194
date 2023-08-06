import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import MultiHopQAPromptware  # noqa


class TestMultiHopQAPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = MultiHopQAPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software = MultiHopQAPromptware()
    #     input = {"question": "Who is Bill Gates?"}
    #     # print complete prompt info for a given example
    #     # print(software.to_code(input))
    #     result = software.execute(input)
    #     self.assertEqual(result, "positive")
