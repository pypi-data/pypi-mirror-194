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


class MultiHopQAPromptware(Promptware):
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
                " chain-of-thought method.",
                instruction="",
                demonstration=[
                    "Question: What is the elevation range for the area"
                    " that the eastern sector of the Colorado orogeny"
                    " extends into?\nThought: Let’s think step by step."
                    " The eastern sector of Colorado orogeny extends into"
                    " the High Plains. High Plains rise in elevation from"
                    " around 1,800 to 7,000 ft, so the answer is 1,800 to 7,000 ft."
                    " \nAnswer: 1,800 to 7,000 ft\n",
                    "Question: Musician and satirist Allie Goertz wrote"
                    ' a song about the "The Simpsons" character Milhouse,'
                    " who Matt Groening named after who? Thought: Let’s think"
                    " step by step. Milhouse was named after U.S. president"
                    " Richard Nixon, so the answer is Richard Nixon. \n"
                    "Answer: Richard Nixon\n",
                    "Question: Which documentary is about Finnish rock groups,"
                    " Adam Clayton Powell or The Saimaa Gesture? "
                    "Thought: Let’s think step by step. Adam Clayton "
                    "Powell (film) is a documentary about an African-American"
                    " politician, not Finnish rock groups. So the documentary"
                    " about Finnish rock groups must instead be The "
                    "Saimaa Gesture.\n "
                    "Answer: The Saimaa Gesture\n",
                    "Question: What profession does Nicholas Ray and Elia Kazan"
                    " have in common?\n "
                    "Thought: Let’s think step by step. Professions of Nicholas"
                    " Ray are director, screenwriter, and actor. Professions"
                    " of Elia Kazan are director, producer, screenwriter, and actor."
                    " So profession Nicholas Ray and Elia Kazan have in common is"
                    " director, screenwriter, and actor.\n Answer: director,"
                    " screenwriter, actor\n",
                    "Question: Which magazine was started first Arthur’s Magazine"
                    " or First for Women?\n Thought: Let’s think step by step."
                    " Arthur’s Magazine was started in 1844. First for Women was"
                    " started in 1989. 1844 (Arthur’s Magazine) < 1989"
                    " (First for Women), so Arthur’s Magazine was started first.\n "
                    "Answer: Arthur’s Magazine\n",
                    "Question: Were Pavel Urysohn and Leonid Levin known for the"
                    " same type of work?\n "
                    "Thought: Let’s think step by step. Pavel Urysohn is a "
                    "mathematician. Leonid Levin is a mathematician and computer"
                    " scientist. So Pavel Urysohn and Leonid Levin have the same"
                    " type of work.\n "
                    "Answer: Yes\n",
                ],
                prompt_template=lambda input: f"Question:"
                f" {input['question']}\n Thought: ",
                task=TaskType.qa_open_domain,
            )
        }

    def _example(self):
        return {
            "input": {
                "question": "What government position was held by the"
                " woman who portrayed Corliss Archer in the"
                " film Kiss and Tell ?"
            },
            "output": "Chief of Protocol",
        }
