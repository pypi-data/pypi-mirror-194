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

machine_translation_zhen = PromptConfig(
    name="machine_translation_zhen",
    description="Machine translation from Chinese to English.",
    instruction="Translate this into English:",
    demonstration=[
        "他知道如何操纵媒体。他完全知道如何登上头条新闻，做了杰克逊 10 "
        "年保镖的菲德斯说道。脸上戴上口罩，或者用胶带粘在手上，或者用"
        "胶带粘在鼻子上"
        "（这个他最喜欢做），在 90% 的情况下，这种方法很奏效。他会说，"
        "他希望自己的一生成为全球最大的谜。”\n",
        "He knew how to manipulate the media. He knew exactly"
        " how to get the"
        " front page, Fiddes, who was Jackson's bodyguard for 10 years, "
        'said. "90 per cent of the time it worked, by putting'
        " a mask on his face,"
        " or sticky tape on his hands - or tape on his nose"
        " was a favourite one."
        " He would say he wanted his life to be the greatest"
        " mystery on Earth.\n"
        "该国还正在开发历史遗迹，如有着数百年历史的玛甸沙勒，这里是与建造约旦佩特"
        "拉城的同一文明遗留下来的砂岩陵墓所在地。\n",
        "The country is also developing historic sites such as"
        " the  centuries-old"
        " Mada'in Saleh, home to sandstone tombs of the same"
        " civilisation which"
        " built the Jordanian city of Petra.\n",
    ],
    prompt_template=lambda input: f"{input['translation']['zh']}",
    task=TaskType.machine_translation,
)


class MachineTranslationPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="Machine translation from English to Chinese.",
            creator="Promptware Authors",
            homepage="https://github.com/expressai/promptware",
            reference="",
            codebase_url="https://github.com/expressai/promptware/tree/main/softwares",
            license=LicenseType.apache_2_0,
            research_tasks=[TaskType.machine_translation],
            application_categories=[ApplicationCategory.transformation],
            application_subcategories=[ApplicationSubcategory.translation],
            original_platform=PlatformType.gpt3,
            design_pattern=DesignPatternType.standalone,
            source_language=LanguageType.en,
            target_language=LanguageType.zh,
        )

    def _kernel_configs(self):
        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="text-curie-001",
                max_tokens=64,
                temperature=0,
            )
        }

    def _software_configs(self):
        return {"machine_translation_zhen": machine_translation_zhen}

    def execute(self, input):
        openai_kernel = self.kernel_configs["openai"].to_kernel()
        code = self.get_code(input, self.software_configs["machine_translation_zhen"])
        return self.normalize_output(openai_kernel.execute(code)["text"])

    def _example(self):

        sample = {
            "translation": {
                "en": "Matt Fiddes, now a property developer and owner of a martial"
                " arts/dance chain, told Metro that Jackson believed the "
                "fascination"
                ' around his persona would stop if he ceased to be a "mystery"'
                " in the public eye.",
                "zh": "现为房地产开发商兼武术/舞蹈连锁店所有者的马特·菲德斯向"
                "《大都市报》爆料称，杰克逊认为，如果他不再是公众眼中的“谜”，"
                "对他个人的迷恋就会戛然而止。\n",
            }
        }

        return {
            "input": sample,
            "output": "Morton Fiddes, the owner of Morton's, a martial "
            "arts/dance chain that is also the owner of Michael "
            "Jackson, has spilled the beans to the newspaper that "
            'Jackson believes if he were no longer the "mystery" of the '
            "public, his love for himself would stop.",
        }
