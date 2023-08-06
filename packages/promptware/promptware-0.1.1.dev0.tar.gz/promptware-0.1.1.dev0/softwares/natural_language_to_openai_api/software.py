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


class NaturalLanguageToOpenAIAPIPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to "
            "convert natural lanugage to OpenAI API.",
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
            source_language=LanguageType.en,
            target_language=LanguageType.python,
        )

    def _kernel_configs(self):

        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="code-davinci-002",  # "text-curie-001",
                max_tokens=64,
                top_p=1.0,
                temperature=0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=['"""'],
            )
        }

    def _software_configs(self):
        return {
            "natural_language_to_openai_api": PromptConfig(
                name="natural_lanugage_to_openai_api",
                description="This promptware is used to "
                "convert natural lanugage to OpenAI API.",
                instruction='"""\nUtil exposes the following:\n'
                "util.openai() -> authenticates & returns the openai "
                "module, which has the following functions:\n"
                'openai.Completion.create(\n    prompt="<my prompt>", '
                "# The prompt to start completing from\n    "
                "max_tokens=123, # The max number of tokens to generate\n    "
                "temperature=1.0 # A measure of randomness\n    "
                "echo=True, # Whether to return the prompt"
                " in addition to the generated completion\n)\n",
                demonstration=[],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {
                "text": '"""\nimport util\n"""\n'
                "Create an OpenAI completion starting from the "
                'prompt "Once upon an AI", no more than 5 tokens. '
                'Does not include the prompt.\n"""\n',
            },
            "output": "def completion_example():\n    openai = util.openai()"
            "\n    completion ="
            ' openai.Completion.create(\n        prompt="Once upon an AI",'
            "\n        max_tokens=5,\n        temperature=1.0,"
            "\n        echo=False,\n    )",
        }
