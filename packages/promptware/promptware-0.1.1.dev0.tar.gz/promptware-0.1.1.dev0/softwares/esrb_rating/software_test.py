import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import ESRBRatingsPromptware  # noqa


class TestESRBRatingsPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = ESRBRatingsPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

        # def test_execute(self):
        #     software =ESRBRatingsPromptware()

        # input = {
        #     "text": "\"i'm going to blow your brains"
        #     " out with my ray gun then stomp on your "
        #     'guts."\n\nESRB rating:'
        # }

    #     result = software.execute(input)
    #     print(result)
