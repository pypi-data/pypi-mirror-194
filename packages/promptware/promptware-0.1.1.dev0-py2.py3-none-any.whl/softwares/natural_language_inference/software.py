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


class NaturalLanguageInferencePromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to identify the semantic"
            " relationship between",
            creator="Promptware Authors",
            homepage="https://github.com/expressai/promptware",
            reference="",
            codebase_url="https://github.com/expressai/promptware/tree/main/softwares",
            license=LicenseType.apache_2_0,
            research_tasks=[TaskType.text_pair_classification],
            application_categories=[ApplicationCategory.classification],
            application_subcategories=[ApplicationSubcategory.general_classification],
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
            "sentiment_classification": PromptConfig(
                name="natural_language_inference",
                description="This promptware is used to identify the semantic"
                " relationship between"
                " two sentences",
                instruction="Give two sentences, predict which of the following"
                " categories their"
                " relationship falls into: entailment, contradiction, neutral",
                demonstration=[
                    "A person on a horse jumps over a broken down airplane.\t"
                    "A person is training his horse for a competition.\nneutral",
                    "A person on a horse jumps over a broken down airplane.\t"
                    "A person is outdoors, on a horse.\nentailment",
                    "Children smiling and waving at camera\tThe kids are"
                    " frowning.\ncontradiction",
                ],
                prompt_template=lambda input: f"{input['text1']}\t{input['text2']}",
                task=TaskType.text_pair_classification,
            )
        }

    def _example(self):
        return {
            "input": {
                "text1": "A boy is jumping on skateboard in the"
                " middle of a red bridge.",
                "text2": "The boy does a skateboarding trick.",
            },
            "output": "neutral",
        }
