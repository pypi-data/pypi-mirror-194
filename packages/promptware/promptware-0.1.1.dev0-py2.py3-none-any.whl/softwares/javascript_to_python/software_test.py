import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import JavaScriptToPythonPromptware  # noqa


class TestJavaScriptToPythonPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = JavaScriptToPythonPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software =JavaScriptToPythonPromptware()

    #     input={"text": "#JavaScript to Python:\nJavaScript: \n"
    #     'dogs = [\"bill\", \"joe\", \"carl\"]\n'
    #     'car = []\ndogs.forEach((dog) '
    #     "{\n    car.push(dog);\n});\n\nPython:"}
    #     result = software.execute(input)
    #     print(result)
