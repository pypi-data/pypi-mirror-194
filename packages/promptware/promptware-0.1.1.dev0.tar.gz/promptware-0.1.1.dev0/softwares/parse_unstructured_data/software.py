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

parse_unstructured_data = PromptConfig(
    name="parse_unstructured_data",
    description="Create tables from long form text by specifying "
    "a structure and supplying some examples.",
    instruction="A table summarizing the following text.",
    demonstration=[],
    prompt_template=lambda input: f"{input['text']}\n{input['head']}\n",
    task=TaskType.conditional_generation,
)


class ParseUnstructuredDataPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="Answer questions based on existing knowledge.",
            creator="OpenAI",
            homepage="https://beta.openai.com/examples/default-parse-data",
            reference="",
            codebase_url="https://beta.openai.com/examples/default-parse-data",
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
                model_name="text-curie-001",
                max_tokens=100,
                temperature=0,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            ),
        }

    def _software_configs(self):
        return {"parse_unstructured_data": parse_unstructured_data}

    def _example(self):
        return {
            "input": {
                "text": "There are many fruits that were found on the recently "
                "discovered planet Goocrux. There are neoskizzles that "
                "grow there, "
                "which are purple and taste like candy. There are also "
                "loheckles, "
                "which are a grayish blue fruit and are very tart, "
                "a little bit like "
                "a lemon. Pounits are a bright green color and are more "
                "savory "
                "than sweet. There are also plenty of loopnovas which "
                "are a neon "
                "pink flavor and taste like cotton candy. Finally, "
                "there are "
                "fruits called glowls, which have a very sour and "
                "bitter taste "
                "which is acidic and caustic, and a pale orange tinge "
                "to them.",
                "head": "| Fruit | Color | Flavor |",
            },
            "output": "There are many fruits that were found on the recently "
            "discovered planet Goocrux. There are neoskizzles that grow "
            "there, which are purple and taste like candy. There are also "
            "loheckles, which are a grayish blue fruit and are very tart, "
            "a little bit like a lemon. Pounits are a bright green color "
            "and are more savory than sweet. There are also plenty of "
            "loopnovas which are a neon pink flavor and taste like cotton "
            "candy",
        }
