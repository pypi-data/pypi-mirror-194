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


class RecipeCreatorPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to "
            "create a recipe from a list of ingredients.",
            creator="OpenAI",
            homepage="https://beta.openai.com/examples/",
            reference="",
            codebase_url="https://beta.openai.com/examples/",
            license=LicenseType.no_license,
            research_tasks=[TaskType.conditional_generation],
            application_categories=[ApplicationCategory.brainstorming],
            application_subcategories=[ApplicationSubcategory.how_to_generation],
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
                max_tokens=120,
                temperature=0.3,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
        }

    def _software_configs(self):
        return {
            "recipe_creator": PromptConfig(
                name="recipe_creator",
                description="This promptware is used to "
                "create a recipe from a list of ingredients.",
                instruction="Write a recipe based on these "
                "ingredients and instructions:\n\n",
                demonstration=[],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {
                "text": "Frito Pie\n\nIngredients:\n"
                "Fritos\nChili\nShredded cheddar cheese\n"
                "Sweet white or red onions, diced small\n"
                "Sour cream\n\nInstructions:"
            },
            "output": "1. Preheat oven to 350 degrees F.\n\n"
            "2. Spread a layer of Fritos in the bottom of a 9x13 inch "
            "baking dish.\n\n3. Top with chili and spread evenly.\n\n4. "
            "Sprinkle shredded cheese over chili.\n\n5. Add diced onions "
            "over cheese.\n\n6."
            " Bake in preheated oven for 20 minutes.\n\n"
            "7. Remove from oven and top with a dollop of sour "
            "cream.\n\n8. Serve and enjoy!",
        }
