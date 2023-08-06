import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import ExtractContactInformationPromptware  # noqa


class TestExtractContactInformationPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = ExtractContactInformationPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software =ExtractContactInformationPromptware()

    #     input={"text": "Dear Kelly,\n\n"
    #     "It was great to talk to you at the seminar. "
    #     "I thought Jane's talk was quite good.\n\n"
    #     "Thank you for the book. "
    #     "Here's my address 2111 Ash Lane, "
    #     "Crestview CA 92002\n\n"
    #     "Best,\n\nMaya\n\nName:"}
    #     result = software.execute(input)
    #     print(result)
