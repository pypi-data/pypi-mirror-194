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


class ExtractContactInformationPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to "
            "extract contact information from a block of text.",
            creator="OpenAI",
            homepage="https://beta.openai.com/examples/",
            reference="",
            codebase_url="https://beta.openai.com/examples/",
            license=LicenseType.no_license,
            research_tasks=[TaskType.conditional_generation],
            application_categories=[ApplicationCategory.transformation],
            application_subcategories=[ApplicationSubcategory.extraction],
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
                max_tokens=64,
                temperature=0,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
        }

    def _software_configs(self):
        return {
            "extract_contact_information": PromptConfig(
                name="extract_contact_information",
                description="This promptware is used to "
                "extract contact information from a block of text.",
                instruction="Extract the name and mailing address from this email:\n\n",
                demonstration=[],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {
                "text": "Dear Kelly,\n\n"
                "It was great to talk to you at the seminar. "
                "I thought Jane's talk was quite good.\n\n"
                "Thank you for the book. "
                "Here's my address 2111 Ash Lane, "
                "Crestview CA 92002\n\n"
                "Best,\n\nMaya\n\nName:"
            },
            "output": "Maya\nMailing Address:\n2111 Ash Lane, Crestview CA 92002",
        }
