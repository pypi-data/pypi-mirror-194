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


class NaturalLanguageToStripeAPIPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to "
            "convert natural lanugage to Stripe API.",
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
            source_language=LanguageType.en,
            target_language=LanguageType.javascript,
        )

    def _kernel_configs(self):
        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="code-davinci-002",  # "text-curie-001",
                max_tokens=100,
                top_p=1.0,
                temperature=0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=['"""'],
            )
        }

    def _software_configs(self):
        return {
            "natural_language_to_stripe_api": PromptConfig(
                name="natural_lanugage_to_stripe_api",
                description="This promptware is used to "
                "convert natural lanugage to Stripe API.",
                instruction='"""\nUtil exposes the following:\n\n'
                "util.stripe() -> authenticates "
                "& returns the stripe module; "
                'usable as stripe.Charge.create etc\n"""\n',
                demonstration=[],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {
                "text": 'import util\n"""\n'
                "Create a Stripe token using the users credit card:"
                " 5555-4444-3333-2222, expiration date 12 / 28,"
                ' cvc 521\n"""'
            },
            "output": 'token = stripe.Token.create(\n    card={\n        "number": '
            '"5555-4444-3333-2222",\n        "exp_month": 12,\n        '
            '"exp_year": 28,\n        "cvc": "521"\n    },\n)',
        }
