import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import WriteAPythonDocstringPromptware  # noqa


class TestWriteAPythonDocstringPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = WriteAPythonDocstringPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software =WriteAPythonDocstringPromptware()

    #     input={"text": "# Python 3.7\n \n"
    #     "def randomly_split_dataset(folder, "
    #     "filename, split_ratio=[0.8, 0.2]):\n    "
    #     "df = pd.read_json(folder + filename, lines=True)\n    "
    #     "train_name, test_name = \"train.jsonl\", \"test.jsonl\"\n    "
    #     "df_train, df_test = train_test_split(df, "
    #     "test_size=split_ratio[1], random_state=42)\n    "
    #     "df_train.to_json(folder + train_name, "
    #     "orient='records', lines=True)\n    "
    #     "df_test.to_json(folder + test_name, "
    #     "orient='records', lines=True)\n"
    #     "randomly_split_dataset('finetune_data/', 'dataset.jsonl')\n"
    #     "    \n# An elaborate, "
    #     "high quality docstring for the above function:\n\"\"\""}
    #     result = software.execute(input)
    #     print(result)
