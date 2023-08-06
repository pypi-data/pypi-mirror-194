import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import InterviewQuestionsPromptware  # noqa


class TestInterviewQuestionsPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = InterviewQuestionsPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software =InterviewQuestionsPromptware()

    #     input={"text": "Create a list of 8 questions "
    #     "for my interview with a science fiction author:"}
    #     result = software.execute(input)
    #     print(result)
