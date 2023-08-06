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

summarization_general = PromptConfig(
    name="summarization_general",
    description="Translates difficult text into simpler concepts.",
    instruction="Summarize the following text into simpler concepts:",
    demonstration=[],
    prompt_template=lambda input: f"{input['text']}\n",
    task=TaskType.summarization,
)


class SummarizationPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="Summarize long text to short text for general domain.",
            creator="OpenAI",
            homepage="https://beta.openai.com/examples/",
            reference="",
            codebase_url="https://beta.openai.com/examples/",
            license=LicenseType.no_license,
            research_tasks=[TaskType.summarization],
            application_categories=[ApplicationCategory.transformation],
            application_subcategories=[ApplicationSubcategory.summarization],
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
                max_tokens=200,
                temperature=0.7,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            ),
        }

    def execute(self, input):
        openai_kernel1 = self.kernel_configs["openai1"].to_kernel()
        code = self.get_code(input, self.software_configs["summarization_general"])
        return self.normalize_output(openai_kernel1.execute(code)["text"])

    def _software_configs(self):
        return {"summarization_general": summarization_general}

    def _example(self):
        return {
            "input": {
                "text": "Jupiter is the fifth planet from the Sun "
                "and the largest in the Solar System. It is a gas "
                "giant with a mass one-thousandth that of the Sun, "
                "but two-and-a-half times that of all the other planets "
                "in the Solar System combined. Jupiter is one of the "
                "brightest objects visible to the naked eye in the night "
                "sky, "
                "and has been known to ancient civilizations since before "
                "recorded "
                "history. It is named after the Roman god Jupiter.[19] "
                "When viewed "
                "from Earth, Jupiter can be bright enough for its "
                "reflected light "
                "to cast visible shadows,[20] and is on average the "
                "third-brightest "
                "natural object in the night sky after the Moon and "
                "Venus."
            },
            "output": "Jupiter is a gas giant planet located fifth "
            "from the Sun, "
            "and is the largest planet in the solar system. It has a "
            "mass one thousandth that of the sun and is two and a half "
            "times that of all the other planets in the solar system "
            "combined. Jupiter is one of the brightest objects visible "
            "in the night sky, and has been known to ancient "
            "civilizations for centuries. It is named after the Roman "
            "god Jupiter. When viewed from Earth, it can cast shadows "
            "with its reflected light.",
        }
