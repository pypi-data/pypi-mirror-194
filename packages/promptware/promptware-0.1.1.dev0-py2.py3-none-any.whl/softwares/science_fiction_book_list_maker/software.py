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


class ScienceFictionBookListMakerPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to "
            "make a list of science fiction books "
            "and stop when it reaches #10.",
            creator="OpenAI",
            homepage="https://beta.openai.com/examples/",
            reference="",
            codebase_url="https://beta.openai.com/examples/",
            license=LicenseType.no_license,
            research_tasks=[TaskType.conditional_generation],
            application_categories=[ApplicationCategory.brainstorming],
            application_subcategories=[ApplicationSubcategory.recommendation],
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
                max_tokens=200,
                temperature=0.5,
                top_p=1.0,
                frequency_penalty=0.52,
                presence_penalty=0.5,
                stop=["11."],
            )
        }

    def _software_configs(self):
        return {
            "science_fiction_book_list_maker": PromptConfig(
                name="science_fiction_book_list_maker",
                description="This promptware is used to "
                "make a list of science fiction books "
                "and stop when it reaches #10.",
                instruction="",
                demonstration=[],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {"text": "List 10 science fiction books:"},
            "output": "1. 1984 by George Orwell\n2. Dune by Frank Herbert\n3. The "
            "Hitchhiker's Guide to the Galaxy by Douglas Adams\n4. The War "
            "of the Worlds by H.G. Wells\n5. Brave New World by Aldous "
            "Huxley\n6. Ender's Game by Orson Scott Card\n7. The Martian "
            "Chronicles by Ray Bradbury\n8. Do Androids Dream of Electric "
            "Sheep? By Philip K Dick \n9. Snow Crash by Neal Stephenson "
            "\n10. Neuromancer by William Gibson",
        }
