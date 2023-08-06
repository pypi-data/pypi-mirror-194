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


class KeywordsPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to "
            "extract keywords from a block of text. "
            "At a lower temperature it picks keywords from the text. "
            "At a higher temperature it will generate related keywords "
            "which can be helpful for creating search indexes.",
            creator="OpenAI",
            homepage="https://beta.openai.com/examples/",
            reference="",
            codebase_url="https://beta.openai.com/examples/",
            license=LicenseType.no_license,
            research_tasks=[TaskType.conditional_generation],
            application_categories=[ApplicationCategory.transformation],
            application_subcategories=[ApplicationSubcategory.extraction],
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
                max_tokens=60,
                temperature=0.5,
                top_p=1.0,
                frequency_penalty=0.8,
                presence_penalty=0.0,
            )
        }

    def _software_configs(self):
        return {
            "keywords": PromptConfig(
                name="keywords",
                description="This promptware is used to "
                "extract keywords from a block of text. "
                "At a lower temperature it picks keywords from the text. "
                "At a higher temperature it will generate related keywords "
                "which can be helpful for creating search indexes.",
                instruction="Extract keywords from this text:\n\n",
                demonstration=[],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {
                "text": "Black-on-black ware is a 20th- "
                "and 21st-century pottery tradition developed "
                "by the Puebloan Native American ceramic artists "
                "in Northern New Mexico. "
                "Traditional reduction-fired blackware has been "
                "made for centuries by pueblo artists. "
                "Black-on-black ware of the past century is produced "
                "with a smooth surface, with the designs applied "
                "through selective burnishing or the application of "
                "refractory slip. Another style involves carving "
                "or incising designs and selectively polishing the raised areas. "
                "For generations several families from "
                "Kha'po Owingeh and P'ohwhóge Owingeh pueblos have been "
                "making black-on-black ware with the techniques "
                "passed down from matriarch potters. "
                "Artists from other pueblos have also produced "
                "black-on-black ware. Several contemporary artists "
                "have created works honoring the pottery of their ancestors."
            },
            "output": "Keywords: black-on-black ware, 20th century, 21st century,"
            " Puebloan Native American, ceramic artists,"
            " Northern New Mexico, reduction-fired blackware,"
            " pueblo artists, burnishing/"
            " slip/carving/incising designs/polishing",
        }
