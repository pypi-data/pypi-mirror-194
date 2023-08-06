import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import TurnByTurnDirectionsPromptware  # noqa


class TestTurnByTurnDirectionsPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = TurnByTurnDirectionsPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

        # def test_execute(self):
        #     software =TurnByTurnDirectionsPromptware()

        # input = {
        #     "text": "Go south on 95 until you hit Sunrise "
        #     "boulevard then take it east to us 1 and head south. "
        #     "Tom Jenkins bbq will be on the left after several miles."
        # }

    #     result = software.execute(input)
    #     print(result)
