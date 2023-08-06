from __future__ import annotations

from datalabs import load_dataset, load_dataset_builder

from promptware.constants import (
    ApplicationCategory,
    ApplicationSubcategory,
    DesignPatternType,
    LanguageType,
    LicenseType,
    PlatformType,
    TaskType,
)
from promptware.dataset import DatasetConfig
from promptware.info import SoftwareInfo
from promptware.kernels.plm import PLMKernelConfig
from promptware.promptware import PromptConfig, Promptware

_REFERENCE = """\
@inproceedings{wang2022super,
  title={Super-naturalinstructions: generalization via declarative instructions on
  1600+ tasks},
  author={Wang, Yizhong and Mishra, Swaroop and Alipoormolabashi, Pegah and Kordi,
  Yeganeh and Mirzaei, Amirreza and Arunkumar, Anjana and Ashok, Arjun and
  Dhanasekaran, Arut Selvan and Naik, Atharva and Stap, David and others},
  year={2022},
  organization={EMNLP}
}
"""


def get_config_names(dataset_name):
    dataset_builder = load_dataset_builder(dataset_name)
    config_names = (
        [None]
        if len(dataset_builder.builder_configs) == 0
        else [x for x in dataset_builder.builder_configs]
    )
    return config_names


# count_words_containing_letter
dataset_name = "natural_instruction"
split_name = "test"


# task_names = get_config_names(dataset_name)

# prompt_configs = {}
# for task_name in task_names:
#     dataset = load_dataset(dataset_name, task_name, split=split_name)
#     prompt_configs[task_name] = PromptConfig(
#         name=task_name,
#         description=task_name.replace("_", " ") + " (zero-shot)",
#         instruction=dataset[0]["definition"],
#         demonstration=[],
#         prompt_template=lambda input: f"Input:{input['text']}\nOutput:",
#         task=TaskType.conditional_generation,
#     )


class NaturalInstructionPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="Manipulate input based on a given instruction",
            creator="OpenAI",
            homepage="https://instructions.apps.allenai.org/",
            reference="",
            codebase_url="_REFERENCE",
            license=LicenseType.apache_2_0,
            research_tasks=[TaskType.conditional_generation],
            application_categories=[ApplicationCategory.transformation],
            application_subcategories=[ApplicationSubcategory.rewriting],
            original_platform=PlatformType.gpt3,
            design_pattern=DesignPatternType.standalone,
            source_language=LanguageType.en,
            target_language=LanguageType.en,
        )

    def _kernel_configs(self):
        return {
            "general": PLMKernelConfig(
                platform="openai",
                model_name="text-curie-001",
                max_tokens=200,
                temperature=0.7,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
        }

    def execute(self, input):
        openai_general = self.kernel_configs["general"].to_kernel()

        software_config = self._software_configs()[self.config_name]
        code = self.get_code(input, software_config)
        output = openai_general.execute(code)
        result = self.normalize_output(output["text"])

        return result

    def _software_configs(self):
        dataset = load_dataset(dataset_name, self.config_name, split=split_name)
        prompt_config = PromptConfig(
            name=self.config_name,
            description=self.config_name.replace("_", " ") + " (zero-shot)",
            instruction=dataset[0]["definition"],
            demonstration=[],
            prompt_template=lambda input: f"Input:{input['inputs']}\nOutput:",
            task=TaskType.conditional_generation,
        )

        if self.config_name == "default":
            # raise ValueError(f"Choose a default sub software name from: {task_names}")
            raise ValueError(f"Invalid subname of software: {self.config_name}")
        return {self.config_name: prompt_config}

    def _dataset_configs(self):
        return {
            self.config_name: DatasetConfig(
                dataset_name=dataset_name,
                sub_dataset=self.config_name,
                split_name="test",
                n_samples=3,
            )
        }

    def evaluate(self, dataset_config: DatasetConfig) -> dict:
        # generate dataset from its config
        from datalabs import load_dataset
        from datalabs.utils.postprocess import recover_labels
        import evaluate

        dataset = load_dataset(
            dataset_config.dataset_name,
            dataset_config.sub_dataset,
            split=dataset_config.split_name,
        )
        dataset = recover_labels(dataset.select(range(dataset_config.n_samples)))

        # evaluation
        references = [sample["targets"] for sample in dataset]
        predictions = self.infer_batch_samples(dataset)

        metric = evaluate.load("rouge")
        results = metric.compute(
            predictions=predictions,
            references=references,
        )

        """Test Command
        from promptware import install
        sub_name = "mwsc_question_generation"
        software = install("./softwares/natural_instruction", sub_name)
        res = software.evaluate(software.dataset_configs[sub_name])
        print(res)
        """

        return results

    def _example(self):
        return {
            "input": {"inputs": "I will go to New York to see a great movie on Sunday"},
            "output": "_I will go to New York to see a great movie on Sunday._\n\n_I "
            "will go to New York to see a new movie._",
        }
