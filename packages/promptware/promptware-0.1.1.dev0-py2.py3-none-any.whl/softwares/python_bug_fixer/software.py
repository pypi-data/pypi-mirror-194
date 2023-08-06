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


class PythonBugFixerPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to "
            "structure the prompt for checking for bugs. "
            "Here we add a comment suggesting that source code is buggy, "
            "and then ask codex to generate a fixed code.",
            creator="OpenAI",
            homepage="https://beta.openai.com/examples/",
            reference="",
            codebase_url="https://beta.openai.com/examples/",
            license=LicenseType.no_license,
            research_tasks=[TaskType.conditional_generation],
            application_categories=[ApplicationCategory.transformation],
            application_subcategories=[ApplicationSubcategory.rewriting],
            original_platform=PlatformType.gpt3,
            design_pattern=DesignPatternType.standalone,
            source_language=LanguageType.python,
            target_language=LanguageType.python,
        )

    def _kernel_configs(self):
        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="text-davinci-003",
                max_tokens=182,
                temperature=0,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=["###"],
            )
        }

    def _software_configs(self):
        return {
            "python_bug_fixer": PromptConfig(
                name="python_bug_fixer",
                description="This promptware is used to "
                "structure the prompt for checking for bugs. "
                "Here we add a comment suggesting that source code is "
                "buggy, "
                "and then ask codex to generate a fixed code.",
                instruction="##### Fix bugs in the below function\n \n",
                demonstration=[],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {
                "text": "### Buggy Python\n"
                "import Random\na = random.randint(1,12)\n"
                "b = random.randint(1,12)\n"
                "for i in range(10):\n    "
                'question = "What is "+a+" x "+b+"? "\n    '
                "answer = input(question)\n    "
                "if answer = a*b\n        "
                "print (Well done!)\n    "
                "else:\n        "
                'print("No.")\n    \n'
                "### Fixed Python"
            },
            "output": "import random\na = random.randint(1,12)\nb = random.randint(1,"
            '12)\nfor i in range(10):\n    question = "What is "+str(a)+" x '
            '"+str(b)+"? "\n    answer = int(input(question))\n    if '
            'answer == a*b:\n        print ("Well done!")\n    else:\n      '
            '  print("No.")',
        }
