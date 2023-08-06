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


class SpreadsheetCreatorPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to "
            "create spreadsheets of various kinds of data. "
            "It's a long prompt but very versatile. "
            "Output can be copy+pasted into a text file "
            "and saved as a .csv with pipe separators.",
            creator="OpenAI",
            homepage="https://beta.openai.com/examples/",
            reference="",
            codebase_url="https://beta.openai.com/examples/",
            license=LicenseType.no_license,
            research_tasks=[TaskType.conditional_generation],
            application_categories=[ApplicationCategory.generation],
            application_subcategories=[ApplicationSubcategory.data_generation],
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
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
        }

    def _software_configs(self):
        return {
            "spreadsheet_creator": PromptConfig(
                name="spreadsheet_creator",
                description="This promptware is used to "
                "create spreadsheets of various kinds of data. "
                "It's a long prompt but very versatile. "
                "Output can be copy+pasted into a text file "
                "and saved as a .csv with pipe separators.",
                instruction="",
                demonstration=[],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {
                "text": "A two-column spreadsheet "
                "of top science fiction movies and the year of "
                "release:\n\n"
                "Title |  Year of release"
            },
            "output": "----------------------------\nBlade Runner  | 1982\nThe Matrix "
            "| 1999\nAlien | 1979\nThe Terminator | 1984\nBack to the "
            "Future | 1985\nStar Wars | 1977\nE.T. the Extra-Terrestrial | "
            "1982\n2001: A Space Odyssey | 1968\nThe Day the Earth St",
        }
