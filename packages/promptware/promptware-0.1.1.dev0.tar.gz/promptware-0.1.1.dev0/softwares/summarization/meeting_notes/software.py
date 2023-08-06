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

summarization_meeting_notes = PromptConfig(
    name="summarization_meeting_notes",
    description="Turn meeting notes into a summary.",
    instruction="Convert my short hand into a first-hand account of the meeting: ",
    demonstration=[],
    prompt_template=lambda input: f"{input['text']}\n",
    task=TaskType.summarization,
)


class SummarizationPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="Summarize long text to short text for meeting notes",
            creator="OpenAI",
            homepage="https://beta.openai.com/examples/",
            reference="",
            codebase_url="https://beta.openai.com/examples/",
            license=LicenseType.no_license,
            research_tasks=[TaskType.summarization],
            application_categories=[ApplicationCategory.transformation],
            application_subcategories=[ApplicationSubcategory.summarization],
            original_platform=PlatformType.gpt3,
            design_pattern=DesignPatternType.standalone,
            source_language=LanguageType.en,
            target_language=LanguageType.en,
        )

    def _kernel_configs(self):
        return {
            "openai2": PLMKernelConfig(
                platform="openai",
                model_name="text-curie-001",
                max_tokens=100,
                temperature=0,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            ),
        }

    def execute(self, input):
        openai_kernel2 = self.kernel_configs["openai2"].to_kernel()
        code = self.get_code(
            input, self.software_configs["summarization_meeting_notes"]
        )
        return self.normalize_output(openai_kernel2.execute(code)["text"])

    def _software_configs(self):
        return {"summarization_meeting_notes": summarization_meeting_notes}

    def _example(self):
        return {
            "input": {
                "text": "Tom: Profits up 50%\n"
                "Jane: New servers are online\n"
                "Kjel: Need more time to fix software\n"
                "Jane: Happy to help\n"
                "Parkman: Beta testing almost done\n"
            },
            "output": "Tom announced that profits were up 50%. Jane mentioned "
            "that new servers were online. Kjel mentioned that they "
            "needed more time to fix the software. Jane offered to "
            "help. Parkman announced that beta testing was almost done.",
        }
