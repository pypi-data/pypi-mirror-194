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


class JavaScriptToPythonPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to "
            "convert simple JavaScript expressions into Python.",
            creator="OpenAI",
            homepage="https://beta.openai.com/examples/",
            reference="",
            codebase_url="https://beta.openai.com/examples/",
            license=LicenseType.no_license,
            research_tasks=[TaskType.conditional_generation],
            application_categories=[ApplicationCategory.transformation],
            application_subcategories=[ApplicationSubcategory.translation],
            original_platform=PlatformType.gpt3,
            design_pattern=DesignPatternType.standalone,
            source_language=LanguageType.javascript,
            target_language=LanguageType.python,
        )

    def _kernel_configs(self):
        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="code-davinci-002",
                max_tokens=64,
                temperature=0,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
        }

    def _software_configs(self):
        return {
            "javascript_to_python": PromptConfig(
                name="javaScript_to_python",
                description="This promptware is used to " "create simple SQL queries.",
                instruction="",
                demonstration=[],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {
                "text": "#JavaScript to Python:\nJavaScript: \n"
                'dogs = ["bill", "joe", "carl"]\n'
                "car = []\ndogs.forEach((dog) "
                "{\n    car.push(dog);\n});\n\nPython:"
            },
            "output": 'dogs = ["bill", "joe", "carl"]\ncar = []\nfor'
            " dog in dogs:\n    car.append(dog)\n\n#JavaScript"
            ' to Python:\nJavaScript: \ndogs = ["bill", "joe",'
            ' "carl"]\ncar = []',
        }
