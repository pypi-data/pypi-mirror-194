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


class InterviewQuestionsPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to " "create interview questions.",
            creator="OpenAI",
            homepage="https://beta.openai.com/examples/",
            reference="",
            codebase_url="https://beta.openai.com/examples/",
            license=LicenseType.no_license,
            research_tasks=[TaskType.conditional_generation],
            application_categories=[ApplicationCategory.brainstorming],
            application_subcategories=[ApplicationSubcategory.advice_giving],
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
                max_tokens=150,
                temperature=0.5,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
        }

    def _software_configs(self):
        return {
            "interview_questions": PromptConfig(
                name="interview_questions",
                description="This promptware is used to " "create interview questions.",
                instruction="",
                demonstration=[],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {
                "text": "Create a list of 8 questions for my interview"
                " with a science fiction author:"
            },
            "output": "1. What inspired you to write science fiction?\n2. How have"
            " you seen the genre of science fiction evolve over the years?"
            "\n3. What do you think are the most important elements for"
            " creating a successful science fiction story?\n4. What advice"
            " would you give to aspiring science fiction authors?\n"
            "5. What has been the most rewarding part of your writing career?"
            "\n6. What are some of the biggest challenges you have faced "
            "as a science fiction author?\n7. What is the most interesting"
            " thing you have learned while researching for"
            " your science fiction stories?\n8. What do you think the"
            " future of science fiction holds?",
        }
