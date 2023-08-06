import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import NaturalLanguageToOpenAIAPIPromptware  # noqa


class TestNaturalLanguageToOpenAIAPIPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = NaturalLanguageToOpenAIAPIPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software = NaturalLanguageToOpenAIAPIPromptware()

    #     input = {
    #         "text": '"""\nimport util\n"""\n'
    #           "Create an OpenAI completion starting from the "
    #         'prompt "Once upon an AI", no more than 5 tokens. '
    #         'Does not include the prompt.\n"""\n',
    #     }
    #     result = software.execute(input)
    #     print(result)
