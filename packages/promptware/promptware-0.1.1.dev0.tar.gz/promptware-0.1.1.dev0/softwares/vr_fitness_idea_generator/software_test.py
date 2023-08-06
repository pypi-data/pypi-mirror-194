import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import VRFitnessIdeaGeneratorePromptware  # noqa


class TestVRFitnessIdeaGeneratorePromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = VRFitnessIdeaGeneratorePromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software = VRFitnessIdeaGeneratorePromptware()

    #     input = {"text": "Brainstorm some ideas combining VR and fitness:"}
    #     result = software.execute(input)
    #     print(result)
