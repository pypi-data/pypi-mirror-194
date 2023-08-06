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


class MicroHorrorStoryCreatorPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to "
            "creates two to three sentence short "
            "horror stories from a topic input.",
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
                max_tokens=60,
                temperature=0.8,
                top_p=1.0,
                frequency_penalty=0.5,
                presence_penalty=0.0,
            )
        }

    def _software_configs(self):
        return {
            "micro_horror_story_creator_test": PromptConfig(
                name="micro_horror_story_creator_test",
                description="This promptware is used to "
                "creates two to three sentence short "
                "horror stories from a topic input.",
                instruction="",
                demonstration=[
                    "Topic: Breakfast\n"
                    "Two-Sentence Horror Story: He always stops crying "
                    "when I pour the milk on his cereal. "
                    "I just have to remember not to "
                    "let him see his face on the carton.\n    \n"
                ],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {"text": "Topic: Wind\nTwo-Sentence Horror Story:"},
            "output": "The wind howled as if it was crying for help."
            " I could feel icy fingers brushing against my skin,"
            " beckoning me to follow them.",
        }
