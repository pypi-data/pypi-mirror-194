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

question_answer_java_script_helper = PromptConfig(
    name="question_answer_java_script_helper",
    description="This is a message-style chatbot that can answer "
    "questions about using JavaScript. It uses a few examples "
    "to get the conversation started.",
    instruction="",
    demonstration=[
        "You: How do I combine arrays?\n"
        "JavaScript chatbot: You can use the concat() method.",
        "You: How do you make an alert appear after 10 seconds?\n"
        "JavaScript chatbot: You can use the setTimeout() method.",
    ],
    prompt_template=lambda input: f"You: {input['question']}\nJavaScript chatbot:",
    task=TaskType.qa_open_domain,
)


class QuestionAnswerPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="Answer questions based on existing knowledge.",
            creator="OpenAI",
            homepage="https://beta.openai.com/examples/",
            reference="",
            codebase_url="https://beta.openai.com/examples/",
            license=LicenseType.no_license,
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
            "openai3": PLMKernelConfig(
                platform="openai",
                model_name="text-curie-001",
                max_tokens=60,
                temperature=0,
                top_p=1,
                frequency_penalty=0.5,
                presence_penalty=0.0,
            ),
        }

    def execute(self, input):
        openai_kernel3 = self.kernel_configs["openai3"].to_kernel()
        code = self.get_code(
            input, self.software_configs["question_answer_java_script_helper"]
        )
        return self.normalize_output(openai_kernel3.execute(code)["text"])

    def _software_configs(self):
        return {
            "question_answer_java_script_helper": question_answer_java_script_helper
        }

    def _example(self):
        return {
            "input": {"question": "Where is the Valley of Kings?"},
            "output": "The Valley of Kings is located in Egypt.",
        }
