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

prompt_config = PromptConfig(
    name="gaokao_essay_writing",
    description="Gaokao English essay writing",
    instruction="",
    demonstration=[
        "Suppose you are Li Hua, teaching your English friend Leslie Chinese."
        " Please write an email with your plans for the next class. The"
        " contents include: 1. Time and place; 2. Content: learning Tang"
        " poetry; 3. Preparation before class: briefly understand the history"
        " of the Tang Dynasty. Here are some requirements: 1. The number of"
        " words is about 100; 2. Details can be added appropriately to make"
        " the writing coherent.\nDear Leslie, I am very happy"
        " that you have made"
        " great progress in learning Chinese and you are interested in Chinese"
        " culture. Now I'll tell you the next learning programme. On July 20,"
        " we are going to learn poems of the Tang Dymasty which"
        " you are interested"
        " in in the Lecture Hall. As a foreign learner, it is difficult for you"
        " to understand the true meaning and the culture of them. Therefore,"
        " before class, you can read some books related to the history of the"
        " Tang Dynasty to better appreciate the poems. Be sure to go to the"
        " Lecture Hall on time. You cannot miss the wonderful poems. Best"
        " wishes. Yours, Li Hua\n",
        "Suppose you are Li Hua, and you want to invite Henry, a"
        " foreign teacher,"
        " to visit the Chinese paper-cutting art exhibition."
        " Please write him an"
        " email, including: 1. Exhibition time and location;"
        " 2. Exhibition content."
        " Here are some requirements: 1. The number of words is about 100; 2."
        " Details can be added appropriately to make the writing"
        " coherent.\nDear"
        " Henry, I'm Li Hua, one of your students in your cultural class. I"
        " know you're interested in one of Chinese traditional"
        " art forms papercutting."
        " So I invite you to attend an exhibition of it. It'll"
        " be held from June 10"
        " to July 10 this year and the opening time is from"
        " 9:00 am to 7:00 pm from"
        " Monday to Saturday and the place of the exhibition"
        " is at the City Gallery,"
        " which is located at 118, Jian Guo Road, Hai Dian District."
        " Shall we go"
        " there together this Friday afternoon? I will meet you at 2:00 pm at"
        " the teaching building gate if you like. You know we Chinese have a"
        " lot of traditional art forms, of which papercutting is one of the"
        " most popular. In the exhibition, you will enjoy many special kinds"
        " of papercuttings. Maybe you can learn one or two"
        " skills of the cutting. Looking forward to your early reply."
        " Regards, Li Hua",
    ],
    prompt_template=lambda input: f"{input['source']}",
    task=TaskType.conditional_generation,
)


class GaokaoEssayWritingPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="gaokao_essay_writing",
            creator="Promptware Authors",
            homepage="https://github.com/expressai/promptware",
            reference="",
            codebase_url="https://github.com/expressai/promptware/tree/main/softwares",
            license=LicenseType.apache_2_0,
            research_tasks=[TaskType.conditional_generation],
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
                max_tokens=300,
                temperature=0.0,
            )
        }

    def _software_configs(self):
        return {"gaokao_essay_writing": prompt_config}

    def _example(self):
        return {
            "input": {
                "source": "Assuming you are Li Hua, your New Zealand friend"
                " Terry will be visiting a Chinese friend's house"
                " and emailing you about customs. Please reply to"
                " the email, including: 1. Arrival time;"
                " 2. Appropriate gifts; 3. Table manners."
                " Here are some requirements: 1. The number of words"
                " is about 100; 2. Details can be added appropriately"
                " to make the writing coherent.",
                "reference": "Dear Terry, How are you doing? In your last"
                " letter, you asked me about being a guest to a"
                " Chinese friend's home. Now, I am writing to"
                " inform you of some relevant details. To"
                " begin with, according to our tradition, you"
                " are supposed to arrive early, so that you can"
                " help the family prepare the dinner, which is"
                " meaningful and interesting. Besides, you'd"
                " better bring some gifts, like a book or a"
                " Chinese knot. What's more, when you are enjoying"
                " the meal, you need to avoid making noises while"
                " chewing food. Hopefully, these suggestions"
                " would be helpful"
                " for you. I have the confidence that you will have"
                " a great time. Best wishes! Yours, Li Hua",
            },
            "output": "Dear Terry, Thank you for your email. I am glad to hear"
            " that you will be visiting a Chinese friend's house. Here are"
            " some suggestions: 1. It is better to arrive on time or"
            " a little earlier. If you are late, it may cause inconvenience"
            " to your host. 2. It is customary to bring a small gift"
            " when visiting someone's home in China. Something like"
            " fruit or flowers is appropriate. 3. When eating at a Chinese"
            " home, it is polite to wait for the host to start eating before"
            " you begin. Also, try to finish everything on your plate,"
            " as it is considered rude to"
            " leave food uneaten. I hope you have a great time."
            " Best wishes, Li Hua",
        }
