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


class AntonymsPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to identify the relationship"
            " between two words",
            creator="Promptware Authors",
            homepage="https://github.com/expressai/promptware",
            reference="",
            codebase_url="https://github.com/expressai/promptware/tree/main/softwares",
            license=LicenseType.apache_2_0,
            research_tasks=[TaskType.antonym_identification],
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
                model_name="text-curie-001",
                max_tokens=64,
                temperature=0,
            )
        }

    def _software_configs(self):
        return {
            "antonyms": PromptConfig(
                name="antonyms",
                description="This promptware is used to identify the  relationship"
                " between two words",
                instruction="take the inputted word and pair it with its antonym",
                demonstration=[
                    "Informed\n" "Uninformed\n\n.",
                    "shout\n" "whisper\n\n",
                    "harmony\ndissonance\n\n",
                ],
                prompt_template=lambda input: f"{input['text']}",
                task=[
                    TaskType.conditional_generation.value,
                ],
            )
        }

    def _example(self):
        return {
            "input": {"text": "correct"},
            "output": "incorrect",
        }
