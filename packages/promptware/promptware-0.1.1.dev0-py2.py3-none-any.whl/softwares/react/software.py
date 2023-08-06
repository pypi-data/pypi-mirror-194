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


class ReactPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to answer a question"
            " that involves multiple step reasoning with"
            " chain-of-thought method.",
            creator="Promptware Authors",
            homepage="https://github.com/expressai/promptware",
            reference="",
            codebase_url="https://github.com/expressai/promptware/tree/main/softwares",
            license=LicenseType.apache_2_0,
            research_tasks=[TaskType.qa_open_domain],
            application_categories=[ApplicationCategory.conversation],
            application_subcategories=[ApplicationSubcategory.question_answering],
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
            )
        }

    def _software_configs(self):
        return {
            "multi_hop_qa": PromptConfig(
                name="multi_hop_qa",
                description="This promptware is used to answer a question"
                " that involves multiple step reasoning with"
                " react method.",
                instruction="",
                demonstration=[
                    "Question: What is the elevation range for the area that the "
                    "eastern sector of the Colorado orogeny extends into? \n"
                    "Thought 1: I need to search Colorado orogeny, find the area that "
                    "the eastern sector of the Colorado orogeny extends into, "
                    "then find the elevation range of the area.\n"
                    "Action 1: Search[Colorado orogeny]\n"
                    "Observation 1: The Colorado orogeny was an episode of mountain "
                    "building (an orogeny) in Colorado and surrounding areas.\n"
                    "Thought 2: It does not mention the eastern sector. So I need to "
                    "look up eastern sector."
                    "Action 2: Lookup[eastern sector]"
                    "Observation 2: (Result 1 / 1) The eastern sector extends into "
                    "the High Plains and is called the Central Plains orogeny.\n"
                    ""
                ],
                prompt_template=lambda input: f"Question: {input['question']}",
                task=TaskType.qa_open_domain,
            )
        }

    def execute(self, input):
        kernel = self.kernel_configs["openai"].to_kernel()
        code = self.get_code(input, self.default_software_config)
        output = kernel.execute(code)
        result = self.normalize_output(output["text"])

        return result

    def _example(self):
        return {
            "input": {
                "question": "What government position was held by the"
                " woman who portrayed Corliss Archer in the"
                " film Kiss and Tell ?"
            },
            "output": "Chief of Protocol",
        }
