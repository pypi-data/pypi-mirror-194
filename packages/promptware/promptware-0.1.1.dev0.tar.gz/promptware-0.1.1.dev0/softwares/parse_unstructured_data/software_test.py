import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import ParseUnstructuredDataPromptware  # noqa


class TestParseUnstructuredDataPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = ParseUnstructuredDataPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    """
    def test_execute(self):
        software = ParseUnstructuredDataPromptware(config_name="default")
        input = {"text": "There are many fruits that were found on the recently "
                 "discovered planet Goocrux. There are neoskizzles that grow there, "
                 "which are purple and taste like candy. There are also loheckles, "
                 "which are a grayish blue fruit and are very tart, a little bit like "
                 "a lemon. Pounits are a bright green color and are more savory "
                 "than sweet. There are also plenty of loopnovas which are a neon "
                 "pink flavor and taste like cotton candy. Finally, there are "
                 "fruits called glowls, which have a very sour and bitter taste "
                 "which is acidic and caustic, and a pale orange tinge to them.",
                 "head": "| Fruit | Color | Flavor |"}
        result = software.execute(input)
        print(result)
        self.assertGreater(len(result), 0)
     """
