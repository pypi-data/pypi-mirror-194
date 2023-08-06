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


class ProductNameGeneratorPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to "
            "create product names from examples words.",
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
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
        }

    def _software_configs(self):
        return {
            "product_name_generator": PromptConfig(
                name="product_name_generator",
                description="This promptware is used to "
                "create product names from examples words.",
                instruction="",
                demonstration=[
                    "Product description: A home milkshake maker\n"
                    "Seed words: fast, healthy, compact.\n"
                    "Product names: HomeShaker, Fit Shaker, QuickShake,"
                    " Shake Maker\n\n",
                ],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {
                "text": "Product description: "
                "A pair of shoes that can fit any foot size.\n"
                "Seed words: adaptable, fit, omni-fit."
            },
            "output": "Product names: AdaptFits, OmniShoes, FitAlls, FootFits.",
        }
