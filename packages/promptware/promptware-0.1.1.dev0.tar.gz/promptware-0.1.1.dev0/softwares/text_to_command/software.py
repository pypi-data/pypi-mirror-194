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


class TextToCommandPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to "
            "convert the text to a programmatic command.",
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
            target_language=LanguageType.en,
        )

    def _kernel_configs(self):
        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="text-curie-001",
                max_tokens=64,
                temperature=0,
            )
        }

    def _software_configs(self):
        return {
            "text_to_command": PromptConfig(
                name="text_to_command",
                description="This promptware is used to "
                "convert the text to a programmatic command.",
                instruction="Convert this text to a programmatic command:",
                demonstration=[
                    "Ask Constance if we need some bread\n"
                    "send-msg `find constance` Do we need some bread?\n\n"
                ],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {
                "text": "Reach out to the ski store and "
                "figure out if I can get my skis fixed before I leave on "
                "Thursday\n"
            },
            "output": "send-msg `find ski store` Can you tell me if you have any skis "
            "in stock that I can use before I leave on Thursday?",
        }
