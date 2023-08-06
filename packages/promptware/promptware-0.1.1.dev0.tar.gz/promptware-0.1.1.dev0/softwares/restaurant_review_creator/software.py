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


class RestaurantReviewCreatorPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to "
            "turn a few words into a restaurant review.",
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
                max_tokens=64,
                temperature=0.5,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
        }

    def _software_configs(self):
        return {
            "restaurant_review_creator": PromptConfig(
                name="restaurant_review_creator",
                description="This promptware is used to "
                "turn a few words into a restaurant review.",
                instruction="Write a restaurant review based on these notes:\n\n",
                demonstration=[],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {
                "text": "Name: The Blue Wharf\n"
                "Lobster great, noisy, service polite, prices "
                "good.\n\nReview:",
            },
            "output": "I recently visited The Blue Wharf for dinner and had a great "
            "experience. The lobster was especially delicious - definitely "
            "the highlight of the meal. The only downside was that it was a "
            "bit noisy, but the polite service more than made up for it. "
            "Prices were also very reasonable, making it a great value "
            "overall.",
        }
