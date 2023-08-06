from __future__ import annotations

import re

from nltk import sent_tokenize

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


def truncate(text, num=512):
    """Keep text length around 512 by default"""
    text_tokens = text.split(" ")
    if len(text_tokens) <= num:
        return text
    total = 0
    sents = sent_tokenize(text)
    final_sents = []
    for i in range(len(sents)):
        if total < num:
            final_sents.append(sents[i])
            total += len(sents[i].split(" "))
        else:
            break
    return " ".join(final_sents)


def normalize_text(text):
    text = re.sub("\n+", " ", text)
    text = re.sub("\t", " ", text)
    text = re.sub(" +", " ", text)
    text = text.encode("ascii", "ignore").decode()
    text = text.strip()
    if len(text) == 0:
        return None
    return text


def preprocess_context(context):
    cont = context.replace("W:", "The woman said:").replace("M:", "The man said:")
    return truncate(normalize_text(cont), 600)


def preprocess_options(options: list[str]):
    options = [f'"{o}"' for o in options]
    return ", ".join(options[:-1]) + " or " + options[-1]


gaokao_cloze_hint = PromptConfig(
    name="gaokao_cloze_hint",
    description="Gaokao English Cloze Hint",
    instruction="",
    demonstration=[
        "There has been a recent trend in the food service industry toward"
        " lower fat content and less salt. This trend, which was started by"
        " the medical community <Q61> a method of fighting heart disease, has"
        " had some unintended side <Q62> such as overweight and heart disease"
        " the very thing the medical community was trying to fight. Fat and"
        " salt are very important parts of a diet. They are required <Q63> the"
        " food that we eat, to recover from injury and for several other bodily"
        " functions. When fat and salt <Q64> from food, the food tastes as if"
        " is missing something. As <Q65> result, people will eat more food to try"
        " to make up for that something missing. Even <Q66>, the amount of fast"
        " food that people eat goes up. Fast food <Q67> full of fat and salt;"
        " by <Q68> more fast food people will get more salt and fat than they"
        " need in their diet. Having enough fat and salt in your meals will reduce"
        " the urge to snack between meals and will improve the taste of your food."
        " However, be <Q69> not to go to extremes. Like anything, it is possible"
        " to have too much of both, <Q70> is not good for the health.\nWhat should"
        " be filled in at the <Q61> position?\nas\n",
        "There has been a recent trend in the food service industry toward"
        " lower fat content and less salt. This trend, which was started by"
        " the medical community as a method of fighting heart disease, has had"
        " some unintended side effects such as overweight and heart disease the"
        " very thing the medical community was trying to fight. Fat and salt"
        " are very important parts of a diet. They are required to process the"
        " food that we eat, to recover from injury and for several other bodily"
        " functions. When fat and salt <Q64> from food, the food tastes as if"
        " is missing something. As <Q65> result, people will eat more food to"
        " try to make up for that something missing. Even <Q66>, the amount of"
        " fast food that people eat goes up. Fast food <Q67> full of fat and"
        " salt; by <Q68> more fast food people will get more salt and fat than they"
        " need in their diet. Having enough fat and salt in your meals will reduce"
        " the urge to snack between meals and will improve the taste of your food."
        " However, be <Q69> not to go to extremes. Like anything, it is possible "
        "to have too much of both, <Q70> is not good for the health.\nWhat should"
        ' be filled in at the <Q64> position given the hint "remove"?\nare removed',
    ],
    prompt_template=lambda input: f"{normalize_text(input['context'])}\n"
    f"What should be filled in at the "
    f"{input['question_mark']} position? given the hint \"{input['hint']}\"?\n",
    task=TaskType.cloze_generative,
)


class GaokaoClozeHintPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="Gaokao English Cloze Hint",
            creator="Promptware Authors",
            homepage="https://github.com/expressai/promptware",
            reference="",
            codebase_url="https://github.com/expressai/promptware/tree/main/softwares",
            license=LicenseType.apache_2_0,
            research_tasks=[TaskType.cloze_generative],
            application_categories=[ApplicationCategory.generation],
            application_subcategories=[ApplicationSubcategory.text_generation],
            original_platform=PlatformType.gpt3,
            design_pattern=DesignPatternType.standalone,
            source_language=LanguageType.en,
            target_language=LanguageType.en,
        )

    def _kernel_configs(self):
        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="text-davinci-002",
                max_tokens=40,
                temperature=0.0,
            )
        }

    def _software_configs(self):
        return {"gaokao_cloze_hint": gaokao_cloze_hint}

    def _example(self):
        return {
            "input": {
                "context": "According to a review of evidence in a medical"
                " journal, runners live three years <Q61> than"
                " non-runners. You don't have to run fast or"
                " for long <Q62> the benefit. You may drink, smoke,"
                " be overweight and still reduce your risk of <Q63>"
                " early by running.\n\nWhile running regularly"
                " can't make you live forever, the review says it"
                " <Q64> more effective at lengthening life <Q65>"
                " walking, cycling or swimming. Two of the authors"
                " of the review also made a study published in 2014"
                " <Q66> showed a mere five to 10 minutes a day of"
                " running reduced the risk of heart disease and"
                " early deaths from all <Q67>.\nThe best exercise"
                " is one that you enjoy and will do. But otherwise"
                " it's probably running. To avoid knee pain, you"
                " can run on soft surfaces, do exercises to <Q68>"
                " your leg muscles, avoid hills and get good running"
                " shoes. Running is cheap, easy and it's always"
                " <Q69>. If you are time poor, you need run for"
                " only half the time to get the same benefits"
                " as other sports, so perhaps we should all give"
                " <Q70> a try.",
                "hint": "long",
                "question_mark": "<Q61>",
                "answers": ["longer"],
            },
            "output": "longer",
        }
