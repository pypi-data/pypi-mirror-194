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

grammar_correction = PromptConfig(
    name="grammar_correction",
    description="Corrects sentences into standard English.",
    instruction="Correct this to standard English:",
    demonstration=[],
    prompt_template=lambda input: f"{input['text']}\n",
    task=TaskType.conditional_generation,
)


class GrammarCorrectionPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="Corrects sentences into standard English.",
            creator="OpenAI",
            homepage="https://beta.openai.com/examples/default-grammar",
            reference="",
            codebase_url="https://beta.openai.com/examples/default-grammar",
            license=LicenseType.no_license,
            research_tasks=[TaskType.conditional_generation],
            application_categories=[ApplicationCategory.transformation],
            application_subcategories=[ApplicationSubcategory.rewriting],
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
                max_tokens=60,
                temperature=0,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            ),
        }

    def _software_configs(self):
        return {"grammar_correction": grammar_correction}

    def _example(self):
        return {
            "input": {"text": "She no went to the market."},
            "output": "She didn't go to the market.",
        }
