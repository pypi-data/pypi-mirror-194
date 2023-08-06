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
from promptware.dataset import DatasetConfig
from promptware.info import SoftwareInfo
from promptware.kernels.plm import PLMKernelConfig
from promptware.promptware import PromptConfig, Promptware


class SentimentClassifierPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to identify the sentiment of a "
            "sentence (positive or negative) based on some learning",
            creator="Promptware Authors",
            homepage="https://github.com/expressai/promptware",
            reference="",
            codebase_url="https://github.com/expressai/promptware/tree/main/softwares",
            license=LicenseType.apache_2_0,
            research_tasks=[TaskType.text_classification],
            application_categories=[ApplicationCategory.classification],
            application_subcategories=[ApplicationSubcategory.sentiment_analysis],
            original_platform=PlatformType.gpt3,
            design_pattern=DesignPatternType.standalone,
            source_language=LanguageType.en,
            target_language=LanguageType.en,
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
        return {
            "sentiment_classification": PromptConfig(
                name="sentiment_classification",
                description="This promptware is used to identify the sentiment of a"
                " sentence (positive or negative) based on some learning"
                " samples from the sst2 dataset.",
                instruction="Give a sentence, classify the sentiment of it"
                " using negative and positive labels",
                demonstration=[
                    "I love this movie.\npositive",
                    "This movie is too boring.\nnegative",
                ],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.text_classification,
            )
        }

    def _dataset_configs(self):
        return {
            "sst2": DatasetConfig(
                dataset_name="sst2",
                sub_dataset=None,
                split_name="test",
                n_samples=10,
            )
        }

    def _example(self):
        return {"input": {"text": "I love this movie."}, "output": "positive"}

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
        references = [sample["label"] for sample in dataset]
        predictions = self.infer_batch_samples(dataset)

        metric = evaluate.load("rouge")
        results = metric.compute(
            predictions=predictions,
            references=references,
        )

        """Test Command
        from promptware import install
        software = install("./softwares/sentiment_classifier")
        software.evaluate(software.dataset_configs["sst2"])
        """

        return results
