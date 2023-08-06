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


class TranslateProgrammingLanguagesPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to "
            "translate from one programming language "
            "to another we can use the comments "
            "to specify the source and target languages.",
            creator="OpenAI",
            homepage="https://beta.openai.com/examples/",
            reference="",
            codebase_url="https://beta.openai.com/examples/",
            license=LicenseType.no_license,
            research_tasks=[TaskType.conditional_generation],
            application_categories=[ApplicationCategory.transformation],
            application_subcategories=[ApplicationSubcategory.translation],
            original_platform=PlatformType.gpt3,
            design_pattern=DesignPatternType.standalone,
            source_language=LanguageType.python,
            target_language=LanguageType.haskell,
        )

    def _kernel_configs(self):
        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="code-davinci-002",
                max_tokens=54,
                temperature=0,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=["###"],
            )
        }

    def _software_configs(self):
        return {
            "translate_programming_languages": PromptConfig(
                name="translate_programming_languages",
                description="This promptware is used to "
                "translate from one programming language "
                "to another we can use the comments "
                "to specify the source and target languages.",
                instruction="",
                demonstration=[],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {
                "text": "##### Translate this function "
                "from Python into Haskell\n"
                "### Python\n    \n    "
                "def predict_proba(X: Iterable[str]):\n        "
                "return np.array([predict_one_probas(tweet) for tweet in X])"
                "\n    \n### Haskell"
            },
            "output": "```haskell\npredictProba :: [String] -> [Double]\n"
            "predictProba xs = map predictOneProbas xs\n```",
        }
