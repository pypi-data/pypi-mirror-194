import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import RecipeCreatorPromptware  # noqa


class TestRecipeCreatorPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = RecipeCreatorPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software =RecipeCreatorPromptware()

    #     input={"text": "Frito Pie\n\nIngredients:\n"
    #     "Fritos\nChili\nShredded cheddar cheese\n"
    #     "Sweet white or red onions, diced small\n"
    #     "Sour cream\n\nInstructions:"}
    #     result = software.execute(input)
    #     print(result)
