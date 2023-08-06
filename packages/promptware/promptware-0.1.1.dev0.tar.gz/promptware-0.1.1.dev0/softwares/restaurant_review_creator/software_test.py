import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import RestaurantReviewCreatorPromptware  # noqa


class TestRestaurantReviewCreatorPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = RestaurantReviewCreatorPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software =RestaurantReviewCreatorPromptware()

    #     input={"text":"Name: The Blue Wharf\n"
    #     "Lobster great, noisy, service polite, prices good.\n\nReview:",}
    #     result = software.execute(input)
    #     print(result)
