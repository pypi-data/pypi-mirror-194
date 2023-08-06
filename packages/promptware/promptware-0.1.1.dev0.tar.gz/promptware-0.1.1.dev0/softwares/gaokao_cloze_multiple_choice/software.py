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


gaokao_cloze_multiple_choice = PromptConfig(
    name="gaokao_cloze_multiple_choice",
    description="Gaokao English Cloze Multiple Choice",
    instruction="",
    demonstration=[
        "If anyone had told me three years ago that I would be spending"
        " most of my weekends camping. I would have laughed heartily. Campers,"
        " in my eyes, were people who enjoyed insects bites, ill-cooked meals,"
        " and uncomfortable sleeping bags. They had nothing in common with"
        " me. <Q36> The friends who introduced me to camping thought that it"
        " meant to be a pioneer. <Q37> We sleep in a tent, cooked over an open"
        " fire, and walked a long distance to take the shower and use the"
        " bathroom. This brief visit with Mother Nature cost me two days off"
        " from work, recovering from a bad case of sunburn and the doctor's bill"
        " for my son's food poisoning. I was, nevertheless, talked into going"
        " on another fun-filled holiday in the wilderness. <Q38> Instead,"
        " we had a pop-up camper with comfortable beds and an air conditioner."
        " My nature-loving friends had remembered to bring all the necessities"
        " of life. <Q39> We have done a lot of it since. Recently, we bought a"
        " twenty-eight-foot travel trailer complete with a bathroom and a"
        " built-in TV set. There is a separate bedroom, a modern kitchen"
        " with a refrigerator. The trailer even has matching carpet and"
        " curtains. <Q40> It must be true that sooner or later, everyone"
        " finds his or her way back to nature. I recommend that you find"
        " your way in style. \nWhat should be filled in at the <Q36>"
        ' position? "This time there was no tent.", "Things are going'
        ' to be improved.", "The trip they took me on was a rough'
        ' one.", "I was to learn a lot about camping since then,'
        ' however.", "I must say that I have certainly come to enjoy'
        ' camping.", "After the trip, my family became quite interested'
        ' in camping." or "There was no shade as the trees were no more'
        ' than 3 feet tall."?\nI was to learn a lot about camping since'
        " then, however.\n",
        "If anyone had told me three years ago that I would be spending most"
        " of my weekends camping. I would have laughed heartily. Campers, in my"
        " eyes, were people who enjoyed insects bites, ill-cooked meals, and"
        " uncomfortable sleeping bags. They had nothing in common with me. I"
        " was to learn a lot about camping since then, however. The friends"
        " who introduced me to camping thought that it meant to be a pioneer."
        " The trip they took me on was a rough one. We sleep in a tent, cooked"
        " over an open fire, and walked a long distance to take the shower and"
        " use the bathroom. This brief visit with Mother Nature cost me two "
        "days off from work, recovering from a bad case of sunburn and the"
        " doctor's bill for my son's food poisoning. I was, nevertheless,"
        " talked into going on another fun-filled holiday in the wilderness."
        " <Q38> Instead, we had a pop-up camper with comfortable beds and"
        " an air conditioner. My nature-loving friends had remembered to"
        " bring all the necessities of life. <Q39> We have done a lot of"
        " it since. Recently, we bought a twenty-eight-foot travel trailer"
        " complete with a bathroom and a built-in TV set. There is a separate"
        " bedroom, a modern kitchen with a refrigerator. The trailer even has"
        " matching carpet and curtains. <Q40> It must be true that sooner or"
        " later, everyone finds his or her way back to nature. I recommend that"
        " you find your way in style. \nWhat should be filled in at the <Q38>"
        ' position? "This time there was no tent.", "Things are going to'
        ' be improved.", "The trip they took me on was a rough one.", "I'
        ' was to learn a lot about camping since then, however.", "I must'
        ' say that I have certainly come to enjoy camping.", "After the'
        ' trip, my family became quite interested in camping." or "There'
        ' was no shade as the trees were no more than 3 feet tall."?\nThis'
        " time there was no tent.\n",
    ],
    prompt_template=lambda input: f"{normalize_text(input['context'])}\n"
    f"What should be filled in at the "
    f"{input['question_mark']} position? {preprocess_options(input['options'])}?\n",
    task=TaskType.cloze_mutiple_choice,
)


class GaokaoClozeMultipleChoicePromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="gaokao_cloze_multiple_choice",
            creator="Promptware Authors",
            homepage="https://github.com/expressai/promptware",
            reference="",
            codebase_url="https://github.com/expressai/promptware/tree/main/softwares",
            license=LicenseType.apache_2_0,
            research_tasks=[TaskType.cloze_mutiple_choice],
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
                model_name="text-davinci-002",
                max_tokens=40,
                temperature=0.0,
            )
        }

    def _software_configs(self):
        return {"gaokao_cloze_multiple_choice": gaokao_cloze_multiple_choice}

    def _example(self):
        return {
            "input": {
                "context": "Color is fundamental in home design — something"
                " you'll always have in every room. A grasp of how"
                " to manage color in your spaces is one of the"
                " first steps to creating rooms you'll love to live"
                " in. Do you want a room that's full of life?"
                " Professional? Or are you just looking for a place"
                " to relax after a long day? <Q36>, color is the key"
                " to making a room feel the way you want it to feel."
                "\n\nOver the years, there have been a number of"
                " different techniques to help designers approach"
                " this important point. <Q37>, they can get a little"
                " complex. But good news is that there're really only"
                " three kinds of decisions you need to make about"
                " color in your home: the small ones, the medium"
                " ones, and the large ones.\n\n<Q38>. They're the"
                " little spots of color like throw pillows, mirrors"
                " and baskets that most of us use to add visual"
                " interest to our rooms. Less tiring than painting"
                " your walls and less expensive than buying a"
                " colorful sofa, small color choices bring with them"
                " the significant benefit of being easily changeable."
                "\n\nMedium color choices are generally furniture"
                " pieces such as sofas, dinner tables or bookshelves."
                " <Q39>. They require a bigger commitment than smaller"
                " ones, and they have a more powerful effect on the"
                " feeling of a space.\n\nThe large color decisions"
                " in your rooms concern the walls, ceilings, and"
                " floors. Whether you're looking at wallpaper or"
                " paint, the time, effort and relative expense put"
                " into it are significant. <Q40>.",
                "options": [
                    "While all of them are useful",
                    "Whatever you're looking for",
                    "If you're experimenting with a color",
                    "Small color choices are the ones we're most" " familiar with",
                    "It's not really a good idea"
                    " to use too many small color"
                    " pieces",
                    "So it pays to be sure, because you want to"
                    " get it right the first time",
                    "Color choices in this range are a step up"
                    " from the small ones in two major ways",
                ],
                "question_mark": "<Q36>",
                "answers": {"text": "Whatever you're looking for", "option_index": 1},
            },
            "output": "Small color choices are the ones we're most familiar with.",
        }
