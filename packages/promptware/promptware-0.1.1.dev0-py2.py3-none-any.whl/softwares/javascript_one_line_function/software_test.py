import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import JavascriptOneLineFunctionPromptware  # noqa


class TestJavascriptOneLineFunctionPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = JavascriptOneLineFunctionPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software =JavascriptOneLineFunctionPromptware()

    #     input={"text":"dogs.forEach((dog) => {\n    car.push(dog);\n});"
    #     "\n\nJavaScript one line version:"}
    #     result = software.execute(input)
    #     print(result)
