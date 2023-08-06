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

conversation_general = PromptConfig(
    name="conversation_general",
    description="Open ended conversation with an AI assistant.",
    instruction="The following is a conversation with an AI assistant. "
    "The assistant is helpful, creative, clever, and very friendly.",
    demonstration=[
        "Human: Hello, who are you?\n"
        "AI: I am an AI created by OpenAI. How can I help you today?\n",
    ],
    prompt_template=lambda input: f"Human: {input['text']}\nAI:",
    task=TaskType.qa_open_domain,
)


class ConversationPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="Open ended conversation with an AI assistant.",
            creator="OpenAI",
            homepage="https://beta.openai.com/examples/",
            reference="",
            codebase_url="https://beta.openai.com/examples/",
            license=LicenseType.no_license,
            research_tasks=[TaskType.qa_open_domain],
            application_categories=[ApplicationCategory.conversation],
            application_subcategories=[ApplicationSubcategory.open_ended_conversation],
            original_platform=PlatformType.gpt3,
            design_pattern=DesignPatternType.standalone,
            source_language=LanguageType.en,
            target_language=LanguageType.en,
        )

    def _kernel_configs(self):
        return {
            "openai1": PLMKernelConfig(
                platform="openai",
                model_name="text-curie-001",
                max_tokens=150,
                temperature=0.9,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.6,
            ),
        }

    def execute(self, input):
        openai_kernel1 = self.kernel_configs["openai1"].to_kernel()
        code = self.get_code(input, self.software_configs["conversation_general"])
        return self.normalize_output(openai_kernel1.execute(code)["text"])

    def _software_configs(self):
        return {"conversation_general": conversation_general}

    def _example(self):
        return {
            "input": {"text": "I'd like to cancel my subscription."},
            "output": "Certainly, cancel your subscription anytime you"
            " like. We hope you enjoy using our services!",
        }
