import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import NaturalLanguageToStripeAPIPromptware  # noqa


class TestNaturalLanguageToStripeAPIPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = NaturalLanguageToStripeAPIPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software = NaturalLanguageToStripeAPIPromptware()

    #     input = {
    #         "text": 'import util\n"""\n'
    #         "Create a Stripe token using the users credit card:"
    #         " 5555-4444-3333-2222, expiration date 12 / 28,"
    #         ' cvc 521\n"""'
    #     }
    #     result = software.execute(input)
    #     print(result)
