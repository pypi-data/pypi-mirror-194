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

question_answer_general = PromptConfig(
    name="question_answer_general",
    description="Answer questions based on existing knowledge.",
    instruction="I am a highly intelligent question answering bot. "
    "If you ask me a question that is rooted in truth, "
    "I will give you the answer. If you ask me a question "
    "that is nonsense, trickery, or has no clear answer, "
    'I will respond with "Unknown".',
    demonstration=[
        "Q: What is human life expectancy in the United States?\n"
        "A: Human life expectancy in the United States is 78 years.",
        "Q: Who was president of the United States in 1955?\n"
        "A: Dwight D. Eisenhower was president of the United States in 1955.",
        "Q: Which party did he belong to?\n" "A: He belonged to the Republican Party.",
        "Q: What is the square root of banana?\n" "A: Unknown",
        "Q: How does a telescope work?\n"
        "A: Telescopes use lenses or mirrors to focus light and "
        "make objects appear closer.",
        "Q: Where were the 1992 Olympics held?\n"
        "A: The 1992 Olympics were held in Barcelona, Spain.",
    ],
    prompt_template=lambda input: f"Q: {input['question']}\nA:",
    task=TaskType.qa_open_domain,
)

question_answer_ml_ai = PromptConfig(
    name="question_answer_ml_ai",
    description="This is a QA-style chatbot that answers questions "
    "about language models.",
    instruction="I am a highly intelligent question answering bot. "
    "If you ask me a question that is rooted in truth, I will give you the answer. "
    "If you ask me a question that is nonsense, trickery, "
    'or has no clear answer, I will respond with "Unknown".',
    demonstration=[
        "You: What is a language model?\n"
        "ML Tutor: A language model is a statistical model that "
        "describes the probability of a word given the previous words.",
        "You: What is a statistical model?\n"
        "ML Tutor: A statistical model is a model that "
        "describes the probability of an event occurring.",
    ],
    prompt_template=lambda input: f"You: {input['question']}\nML Tutor:",
    task=TaskType.qa_open_domain,
)

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
            "openai1": PLMKernelConfig(
                platform="openai",
                model_name="text-curie-001",
                max_tokens=100,
                temperature=0,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            ),
            "openai2": PLMKernelConfig(
                platform="openai",
                model_name="text-curie-001",
                max_tokens=60,
                temperature=0.3,
                top_p=1,
                frequency_penalty=0.5,
                presence_penalty=0,
            ),
            "openai3": PLMKernelConfig(
                platform="openai",
                model_name="text-curie-001",
                max_tokens=60,
                temperature=0,
                top_p=1,
                frequency_penalty=0.5,
                presence_penalty=0.0,
            ),
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
        openai_kernel1 = self.kernel_configs["openai1"].to_kernel()
        openai_kernel2 = self.kernel_configs["openai2"].to_kernel()
        openai_kernel3 = self.kernel_configs["openai3"].to_kernel()
        openai_kernel4 = self.kernel_configs["openai4"].to_kernel()
        if self.config_name == "default" or self.config_name == "general":
            code = self.get_code(
                input, self.software_configs["question_answer_general"]
            )
            return self.normalize_output(openai_kernel1.execute(code)["text"])
        elif self.config_name == "ml_ai":
            code = self.get_code(input, self.software_configs["question_answer_ml_ai"])
            return self.normalize_output(openai_kernel2.execute(code)["text"])
        elif self.config_name == "java_script_helper":
            code = self.get_code(
                input, self.software_configs["question_answer_java_script_helper"]
            )
            return self.normalize_output(openai_kernel3.execute(code)["text"])
        elif self.config_name == "factual":
            code = self.get_code(
                input, self.software_configs["question_answer_factual"]
            )
            return self.normalize_output(openai_kernel4.execute(code)["text"])
        else:
            raise ValueError("Unknown question answer type: {self.config_name}")

    def _software_configs(self):
        if self.config_name == "default" or self.config_name == "general":
            return {"question_answer_general": question_answer_general}
        elif self.config_name == "ml_ai":
            return {"question_answer_ml_ai": question_answer_ml_ai}
        elif self.config_name == "java_script_helper":
            return {
                "question_answer_java_script_helper": question_answer_java_script_helper
            }
        elif self.config_name == "factual":
            return {" question_answer_factual": question_answer_factual}
        else:
            raise ValueError("Unknown question answer type: {self.config_name}")

    def _example(self):
        return {
            "input": {"question": "Where is the Valley of Kings?"},
            "output": "The Valley of Kings is located in Egypt.",
        }
