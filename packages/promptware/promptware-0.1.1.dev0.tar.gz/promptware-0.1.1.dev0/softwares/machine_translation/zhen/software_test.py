import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import MachineTranslationPromptware  # noqa


class TestMachineTranslationPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = MachineTranslationPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #
    #     input = {
    #         "translation": {
    #             "en": "Matt Fiddes, now a property developer and owner of a martial"
    #             " arts/dance chain, told Metro that Jackson believed the fascination"
    #             ' around his persona would stop if he ceased to be a "mystery"'
    #             " in the public eye.",
    #             "zh": "现为房地产开发商兼武术/舞蹈连锁店所有者的马特·菲德斯向"
    #             "《大都市报》爆料称，杰克逊认为，如果他不再是公众眼中的“谜”，"
    #             "对他个人的迷恋就会戛然而止。\n",
    #         }
    #     }
    #     software = MachineTranslationPromptware()
    #     result = software.execute(input)
    #     self.assertGreater(len(result), 0)
