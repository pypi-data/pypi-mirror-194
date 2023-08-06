import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import PythonBugFixerPromptware  # noqa


class TestPythonBugFixerPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = PythonBugFixerPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software =PythonBugFixerPromptware()

    #     input={"text": "### Buggy Python\n"
    #     "import Random\na = random.randint(1,12)\n"
    #     "b = random.randint(1,12)\n"
    #     "for i in range(10):\n    "
    #     "question = \"What is \"+a+\" x \"+b+\"? \"\n    "
    #     "answer = input(question)\n    "
    #     "if answer = a*b\n        "
    #     "print (Well done!)\n    "
    #     "else:\n        "
    #     "print(\"No.\")\n    \n"
    #     "### Fixed Python"}
    #     result = software.execute(input)
    #     print(result)
