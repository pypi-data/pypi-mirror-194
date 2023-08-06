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


class VRFitnessIdeaGeneratorePromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to "
            "create ideas for fitness and virtual reality games.",
            creator="OpenAI",
            homepage="https://beta.openai.com/examples/",
            reference="",
            codebase_url="https://beta.openai.com/examples/",
            license=LicenseType.no_license,
            research_tasks=[TaskType.conditional_generation],
            application_categories=[ApplicationCategory.brainstorming],
            application_subcategories=[ApplicationSubcategory.advice_giving],
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
                max_tokens=150,
                temperature=0.6,
                top_p=1.0,
                frequency_penalty=1,
                presence_penalty=1,
            )
        }

    def _software_configs(self):
        return {
            "vr_fitness_idea_generator": PromptConfig(
                name="vr_fitness_idea_generator",
                description="This promptware is used to "
                "create ideas for fitness and virtual reality games.",
                instruction="",
                demonstration=[],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {"text": "Brainstorm some ideas combining VR and fitness:"},
            "output": "1. Virtual reality exercise classes \n2. Virtual reality "
            "running and cycling simulations \n3. Interactive virtual "
            "fitness challenges \n4. Immersive yoga experiences in a "
            "virtual environment \n5. Virtual strength training with "
            "personalized feedback from trainers  \n6. VR-based aerobic "
            "workouts for home use  \n7. Gamified weightlifting activities "
            "using motion tracking controllers  \n8. Tracking progress of "
            "physical activity through 3D avatars",
        }
