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
from promptware.utils.logprobs_utils import average_logprobs


class ScoringPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This software is used to calculate the average"
            " log probability of a text",
            creator="Promptware Authors",
            homepage="https://github.com/expressai/promptware",
            reference="",
            codebase_url="https://github.com/expressai/promptware/tree/main/softwares",
            license=LicenseType.apache_2_0,
            research_tasks=[TaskType.others],
            application_categories=[ApplicationCategory.others],
            application_subcategories=[ApplicationSubcategory.others],
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
                max_tokens=0,
                temperature=0,
                logprobs=1,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                n=1,
                echo=True,
            )
        }

    def _software_configs(self):
        return {
            "scoring": PromptConfig(
                name="scoring",
                description="Given a text, generate the average of its log"
                " probabilities",
                instruction="",
                demonstration=None,
                prompt_template=lambda text: f"{text}",
                task=TaskType.others,
            )
        }

    def execute(self, input):

        kernel = self.kernel_configs["openai"].to_kernel()
        code = self.get_code(input, self.software_configs["scoring"])
        output = kernel.execute(code)
        # print(output)
        # Skip the first token: None
        score = average_logprobs(
            token_logprobs=output["token_logprobs"][1:], tokens=output["tokens"][1:]
        )
        return score

    def _example(self):
        return {
            "input": "I love this movie",
            "output": -3.8613948799999998,
        }
