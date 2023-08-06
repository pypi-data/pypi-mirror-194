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

conversation_friend = PromptConfig(
    name="conversation_friend",
    description="Emulate a text message conversation.",
    instruction="",
    demonstration=[
        "You: What have you been up to?\n"
        "Friend: Watching old movies.\n"
        "You: Did you watch anything interesting?\n"
        "Friend: Yes, I watched The Omen and Troy.",
    ],
    prompt_template=lambda input: f"You: {input['text']}\nFriend:",
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
            "openai2": PLMKernelConfig(
                platform="openai",
                model_name="text-curie-001",
                max_tokens=60,
                temperature=0.5,
                top_p=1,
                frequency_penalty=0.5,
                presence_penalty=0,
            ),
        }

    def execute(self, input):

        openai_kernel2 = self.kernel_configs["openai2"].to_kernel()
        code = self.get_code(input, self.software_configs["conversation_friend"])
        return self.normalize_output(openai_kernel2.execute(code)["text"])

    def _software_configs(self):
        return {"conversation_friend": conversation_friend}

    def _example(self):
        return {
            "input": {"text": "I'd like to cancel my subscription."},
            "output": "No problem!",
        }
