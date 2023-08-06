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


class EssayOutlinePromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to "
            "generate an outline for a research topic.",
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
            "essay_outline": PromptConfig(
                name="essay_outline",
                description="This promptware is used to "
                "generate an outline for a research topic.",
                instruction="",
                demonstration=[],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {
                "text": "Create an outline for an essay about Nikola Tesla"
                " and his contributions to technology:"
            },
            "output": "I. Introduction\nA. Definition of Nikola Tesla\n"
            "B. Overview of Tesla's life and accomplishments\n\n"
            "II. Early Life and Education\nA. Tesla's birthplace"
            " and family\nB. Tesla's education and early career\n\n"
            "III. Contributions to Technology\nA. Alternating current\n"
            "B. Radio and remote control\nC. Robotics and artificial"
            " intelligence\nD. X-rays and lasers\n\nIV. Legacy of Tesla\n"
            "A. Impact on modern technology\nB. Recognition of"
            " Tesla's work\n\n V. Conclusion\nA. Summary of Tesla's"
            " life and accomplishments\nB. Reflection on Tesla's legacy",
        }
