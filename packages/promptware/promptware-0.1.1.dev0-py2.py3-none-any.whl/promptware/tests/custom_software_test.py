import os
import unittest

from promptware import install
from promptware.artifacts.utils import test_artifacts_path


class CustomSoftwareTest(unittest.TestCase):
    artifact_module_path = os.path.join(test_artifacts_path, "software")

    def test_custom_software(self):
        prompt = "Text: I love this movie\nLabel: Positive\n"
        formatter = "Text:{text}\nLabel:"
        software = install(prompt=prompt, formatter=formatter)
        # input = {"text": "I don't like this movie"}
        # output = software.execute(input)
        # self.assertEqual(output, "Negative")

        self.assertEqual(
            software.example_prompt,
            "Text: I love this movie\nLabel: " "Positive\n\nText:text\nLabel:",
        )

    def test_custom_software_from_json(self):
        file_path = os.path.join(self.artifact_module_path, "custom.json")

        software = install(file_path)

        self.assertEqual(
            software.example_prompt,
            "Text: I love this movie\nLabel: " "Positive\n\nText:text\nLabel:",
        )


if __name__ == "__main__":
    unittest.main()
