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


class CreateStudyNotesPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to "
            "provide a topic and get study notes.",
            creator="OpenAI",
            homepage="https://beta.openai.com/examples/",
            reference="",
            codebase_url="https://beta.openai.com/examples/",
            license=LicenseType.no_license,
            research_tasks=[TaskType.conditional_generation],
            application_categories=[ApplicationCategory.generation],
            application_subcategories=[ApplicationSubcategory.text_generation],
            original_platform=PlatformType.gpt3,
            design_pattern=DesignPatternType.standalone,
            source_language=LanguageType.en,
            target_language=LanguageType.en,
        )

    def _kernel_configs(self):
        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="text-davinci-003",
                max_tokens=150,
                temperature=0.3,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
        }

    def _software_configs(self):
        return {
            "create_study_notes": PromptConfig(
                name="create_study_notes",
                description="This promptware is used to "
                "provide a topic and get study notes.",
                instruction="",
                demonstration=[],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {
                "text": "What are 5 key points I should"
                " know when studying Ancient Rome?"
            },
            "output": "1. The Roman Republic: This was the period of Ancient"
            " Rome from 509 BC to 27 BC, when it was ruled by a"
            " senate and two consuls.\n\n2. The Roman Empire: This was"
            " the period of Ancient Rome from 27 BC to 476 AD, when it"
            " was ruled by an emperor.\n\n3. Roman Law: This was the"
            " system of laws that governed the Roman Republic and Empire."
            " It was based on the Twelve Tables, a set of laws written"
            " in the 5th century BC.\n\n4. Roman Religion: This was the"
            " religion of Ancient Rome, which was polytheistic and focused"
            " on the worship of gods and goddesses.\n\n5. Roman"
            " Architecture: This was the style of architecture",
        }
