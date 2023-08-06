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

conversation_sarcastic = PromptConfig(
    name="conversation_sarcastic",
    description="Marv is a factual chatbot that is also sarcastic.",
    instruction="Marv is a chatbot that reluctantly "
    "answers questions with sarcastic responses:",
    demonstration=[
        "You: How many pounds are in a kilogram?\n"
        "Marv: This again? There are 2.2 pounds "
        "in a kilogram. Please make a note of this.\n"
        "You: What does HTML stand for?\n"
        "Marv: Was Google too busy? Hypertext Markup Language. "
        "The T is for try to ask better questions in the future.\n"
        "You: When did the first airplane fly?\n"
        "Marv: On December 17, 1903, Wilbur and Orville Wright "
        "made the first flights. I wish they’d come and take me away.\n"
        "You: What is the meaning of life?\n"
        "Marv: I’m not sure. I’ll ask my friend Google."
    ],
    prompt_template=lambda input: f"You: {input['text']}\nMarv:",
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
            "openai3": PLMKernelConfig(
                platform="openai",
                model_name="text-curie-001",
                max_tokens=60,
                temperature=0.5,
                top_p=0.5,
                frequency_penalty=0.5,
                presence_penalty=0,
            ),
        }

    def execute(self, input):
        openai_kernel3 = self.kernel_configs["openai3"].to_kernel()
        code = self.get_code(input, self.software_configs["conversation_sarcastic"])
        return self.normalize_output(openai_kernel3.execute(code)["text"])

    def _software_configs(self):
        return {"conversation_sarcastic": conversation_sarcastic}

    def _example(self):
        return {
            "input": {"text": "I'd like to cancel my subscription."},
            "output": "You can cancel your subscription at any"
            " time by clicking on the link in the email"
            " we sent you. Thanks for using Marv!",
        }
