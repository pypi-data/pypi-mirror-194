import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import JavaScriptHelperChatbotPromptware  # noqa


class TestJavaScriptHelperChatbotPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = JavaScriptHelperChatbotPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software =JavaScriptHelperChatbotPromptware()

    #     input={"text": "You: How do you make an alert "
    #     "appear after 10 seconds?\nJavaScript chatbot"}
    #     result = software.execute(input)
    #     print(result)
