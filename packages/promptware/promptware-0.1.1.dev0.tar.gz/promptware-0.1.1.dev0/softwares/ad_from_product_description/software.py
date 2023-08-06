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


class AdFromProductDescriptionPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to "
            "turn a product description into ad copy.",
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
                model_name="text-curie-001",
                max_tokens=100,
                temperature=0.5,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
        }

    def _software_configs(self):
        return {
            "ad_from_product_description": PromptConfig(
                name="ad_from_product_description",
                description="This promptware is used to "
                "turn a product description into ad copy.",
                instruction="Write a creative ad for the following "
                "product to run on Facebook aimed at parents:\n\n",
                demonstration=[],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {
                "text": "Product: Learning Room is a virtual environment to help"
                " students from kindergarten to high school excel in"
                " school."
            },
            "output": "Learning Room is the perfect virtual environment for"
            " parents to help their children excel in school."
            " With Learning Room,"
            " parents can help their children learn at their own pace,"
            " in a safe and secure environment.",
        }
