import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import QuestionAnswerPromptware  # noqa


class TestQuestionAnswerPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = QuestionAnswerPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    """
    def test_execute_default(self):
         software = QuestionAnswerPromptware(config_name="default")
         input = {"question": "Where is the Valley of Kings?"}
         result = software.execute(input)
         print(result)
         self.assertGreater(len(result), 0)

    def test_execute_ml_ai(self):
         software = QuestionAnswerPromptware(config_name="ml_ai")
         input = {"question": "What is a neural network?"}
         result = software.execute(input)
         print(result)
         self.assertGreater(len(result), 0)

    def test_execute_java_script_helper(self):
         software = QuestionAnswerPromptware(config_name="java_script_helper")
         input = {"question": "How do I sort arrays?"}
         result = software.execute(input)
         print(result)
         self.assertGreater(len(result), 0)

    def test_execute_factual(self):
         software = QuestionAnswerPromptware(config_name="factual")
         input = {"question": "What's a language model?"}
         result = software.execute(input)
         print(result)
         self.assertGreater(len(result), 0)
    """
