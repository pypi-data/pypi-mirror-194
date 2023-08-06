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

question_answer_factual = PromptConfig(
    name="question_answer_factual",
    description="Guide the model towards factual answering by showing "
    "it how to respond to questions that fall outside its knowledge base. "
    "Using a '?' to indicate a response to words and phrases that it doesn't "
    "know provides a natural response that seems to work better "
    "than more abstract replies.",
    instruction="",
    demonstration=[
        "Q: Who is Batman?\n" "A: Batman is a fictional comic book character.",
        "Q: What is torsalplexity?\n" "A: ?",
        "Q: What is Devz9?\n" "A: ?",
        "Q: Who is George Lucas?\n"
        "A: George Lucas is American film director and producer "
        "famous for creating Star Wars.",
        "Q: What is the capital of California?\n" "A: Sacramento.",
        "Q: What orbits the Earth?\n" "A: The Moon.",
        "Q: Who is Fred Rickerson?\n" "A: ?",
        "Q: What is an atom?\n"
        "A: An atom is a tiny particle that makes up everything.",
        "Q: Who is Alvan Muntz?\n" "A: ?",
        "Q: What is Kozar-09?\n" "A: ?:",
        "Q: How many moons does Mars have?\n" "A: Two, Phobos and Deimos.",
    ],
    prompt_template=lambda input: f"Q: {input['question']}\nA:",
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
            "openai4": PLMKernelConfig(
                platform="openai",
                model_name="text-curie-001",
                max_tokens=60,
                temperature=0,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            ),
        }

    def execute(self, input):
        openai_kernel4 = self.kernel_configs["openai4"].to_kernel()
        code = self.get_code(input, self.software_configs["question_answer_factual"])
        return self.normalize_output(openai_kernel4.execute(code)["text"])

    def _software_configs(self):
        return {" question_answer_factual": question_answer_factual}

    def _example(self):
        return {
            "input": {"question": "Where is the Valley of Kings?"},
            "output": "The Valley of Kings is located in Egypt.",
        }
