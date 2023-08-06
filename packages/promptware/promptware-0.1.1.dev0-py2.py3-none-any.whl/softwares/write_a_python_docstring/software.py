from __future__ import annotations

from promptware.constants import (
    ApplicationCategory,
    ApplicationSubcategory,
    DesignPatternType,
    LanguageType,
    LicenseType,
    PlatformType,
    TaskType,
)
from promptware.info import SoftwareInfo
from promptware.kernels.plm import PLMKernelConfig
from promptware.promptware import PromptConfig, Promptware


class WriteAPythonDocstringPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to "
            "create a docstring for a given Python function. "
            "We specify the Python version, paste in the code, "
            "and then ask within a comment for a docstring, "
            'and give a characteristic beginning of a docstring (""").',
            creator="OpenAI",
            homepage="https://beta.openai.com/examples/",
            reference="",
            codebase_url="https://beta.openai.com/examples/",
            license=LicenseType.no_license,
            research_tasks=[TaskType.conditional_generation],
            application_categories=[ApplicationCategory.transformation],
            application_subcategories=[ApplicationSubcategory.explanation],
            original_platform=PlatformType.gpt3,
            design_pattern=DesignPatternType.standalone,
            source_language=LanguageType.python,
            target_language=LanguageType.en,
        )

    def _kernel_configs(self):
        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="text-davinci-003",
                max_tokens=150,
                temperature=0,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=["#", '"""'],
            )
        }

    def _software_configs(self):
        return {
            "write_a_python_docstring": PromptConfig(
                name="write_a_python_docstring",
                description="This promptware is used to "
                "create a docstring for a given Python function. "
                "We specify the Python version, paste in the code, "
                "and then ask within a comment for a docstring, "
                'and give a characteristic beginning of a docstring (""").',
                instruction="",
                demonstration=[],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {
                "text": "# Python 3.7\n \n"
                "def randomly_split_dataset(folder, "
                "filename, split_ratio=[0.8, 0.2]):\n    "
                "df = pd.read_json(folder + filename, lines=True)\n    "
                'train_name, test_name = "train.jsonl", '
                '"test.jsonl"\n    '
                "df_train, df_test = train_test_split(df, "
                "test_size=split_ratio[1], random_state=42)\n    "
                "df_train.to_json(folder + train_name, "
                "orient='records', lines=True)\n    "
                "df_test.to_json(folder + test_name, "
                "orient='records', lines=True)\n"
                "randomly_split_dataset('finetune_data/', "
                "'dataset.jsonl')\n"
                "    \n# An elaborate, "
                'high quality docstring for the above function:\n"""'
            },
            "output": "This function randomly splits a dataset into two parts, "
            "a training set and a test set, and saves them as separate "
            "files.\n\nParameters:\n    folder (str): The path to the "
            "folder containing the dataset file.\n    filename (str): The "
            "name of the dataset file.\n    split_ratio (list): A list of "
            "two floats representing the ratio of the training set and the "
            "test set.\n\nReturns:\n    None",
        }
