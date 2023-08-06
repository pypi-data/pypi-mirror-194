import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import TranslateProgrammingLanguagesPromptware  # noqa


class TestTranslateProgrammingLanguagesPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = TranslateProgrammingLanguagesPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

        # def test_execute(self):
        #     software =TranslateProgrammingLanguagesPromptware()

        # input = {
        #     "text": "##### Translate this function "
        #     "from Python into Haskell\n"
        #     "### Python\n    \n    "
        #     "def predict_proba(X: Iterable[str]):\n        "
        #     "return np.array([predict_one_probas(tweet) for tweet in X])"
        #     "\n    \n### Haskell"
        # }
        # result = software.execute(input)
        # print(result)
