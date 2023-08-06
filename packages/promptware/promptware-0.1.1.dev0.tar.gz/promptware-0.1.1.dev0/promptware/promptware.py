from __future__ import annotations

from collections.abc import Callable
import dataclasses
from dataclasses import dataclass
from typing import Any, Optional

import numpy as np

from promptware.constants.tasks import TaskType
from promptware.dataset import DatasetConfig
from promptware.info import SoftwareInfo
from promptware.kernels.plm import PLMKernelConfig
from promptware.software import Software, SoftwareConfig
from promptware.utils.naming import camelcase_to_snakecase
from promptware.utils.prompt_utils import get_template


@dataclass
class PromptConfig(SoftwareConfig):
    # Name
    name: str
    # Describe what the promptware is designed for
    description: str
    # Instruction text of promptware
    instruction: str | Callable[[Any], str]
    # Demonstration of promptware
    demonstration: Optional[list[str]]
    # Prompt template defines how a user's input will be formatted
    prompt_template: Callable[[Any], str]
    # The most appropriate tasks that the promptware could be applied to
    task: Optional[TaskType] = None

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "instruction": self.instruction
            if not callable(self.instruction)
            else get_template(self.instruction),
            "demonstration": self.demonstration,
            "prompt_template": get_template(self.prompt_template),
            "task": self.task,
        }

    @classmethod
    def from_dict(cls, data_dict: dict) -> PromptConfig:
        field_names = set(f.name for f in dataclasses.fields(cls))
        return cls(**{k: v for k, v in data_dict.items() if k in field_names})


class Promptware(Software):
    def __init__(
        self,
        config_name: Optional[str] = None,
    ):

        self.config_name = config_name or "default"
        self.info = self._info()

        self.kernel_configs = self._kernel_configs()
        self.software_configs = self._software_configs()
        self.default_software_config = self._default_software_config()
        self.dataset_configs = self._dataset_configs()
        self.example = self._example()
        self.example_prompt = self._example_prompt()
        # Set other values for info
        self.info.module_name = camelcase_to_snakecase(self.__class__.__name__)
        self.info.config_name = self.config_name
        self.info.kernel_configs = self.kernel_configs
        self.info.software_configs = self.software_configs
        self.info.dataset_configs = self._dataset_configs()
        self.info.example = self._example()
        self.info.example_prompt = self._example_prompt()

    def _info(self) -> SoftwareInfo:
        raise NotImplementedError

    def _default_software_config(self):
        return list(self.software_configs.values())[0]

    def _kernel_configs(self) -> dict[str, PLMKernelConfig]:
        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="text-curie-001",
                max_tokens=64,
                temperature=0,
            )
        }

    def normalize_output(self, output: str) -> str:
        return output.strip()

    def _software_configs(self) -> dict[str, SoftwareConfig]:
        raise NotImplementedError

    def _dataset_configs(self) -> dict[str, DatasetConfig] | None:
        return None

    def update_kernel(self, kernel_name: str, kernel_info: dict) -> PLMKernelConfig:
        """Update the kernel with the given name and info."""
        if kernel_name not in self.kernel_configs:
            raise ValueError(f"Unknown kernel: {kernel_name}")
        for k, v in kernel_info.items():
            if hasattr(self.kernel_configs[kernel_name], k):
                setattr(self.kernel_configs[kernel_name], k, v)
        return self.kernel_configs[kernel_name]

    def update_prompt(self, prompt_name: str, prompt_info: dict) -> SoftwareConfig:
        """Update the prompt with the given name and info."""
        if prompt_name not in self.software_configs:
            raise ValueError(f"Unknown prompt: {prompt_name}")
        for k, v in prompt_info.items():
            if hasattr(self.software_configs[prompt_name], k):
                setattr(self.software_configs[prompt_name], k, v)
        return self.software_configs[prompt_name]

    def update_demonstration(self, name: str, demonstrations: list) -> SoftwareConfig:

        setattr(self.software_configs[name], "demonstration", demonstrations)
        return self.software_configs[name]

    def extend_demonstration(self, name: str, demonstrations: list) -> SoftwareConfig:

        ori_demonstrations = getattr(self.software_configs[name], "demonstration")
        setattr(
            self.software_configs[name],
            "demonstration",
            ori_demonstrations + demonstrations,
        )
        return self.software_configs[name]

    def _example(self) -> dict[Any, Any] | None:
        return None

    def get_instantiated_instruction(
        self, input: dict, instruction: str | Callable[[Any], str]
    ) -> str:
        return instruction if not callable(instruction) else instruction(input)

    def get_instantiated_prompt(self, input: dict, prompt: Callable[[Any], str]) -> str:
        """

        Args:
            input: the input with the original format that software need to process

        Returns:
            the input with format specified by prompt_template

        """

        return prompt(input)

    def get_code(self, input: dict, software_config) -> str:
        """

        Args:
            input: the input with the original format that software need to process

        Returns:
            the combined information of promptware's instruction, prompted input
             and demonstration

        """
        delimiter = "\n"
        instantiated_instruction = (
            self.get_instantiated_instruction(input, software_config.instruction)
            + delimiter
            if software_config.instruction != ""
            else ""
        )

        demonstration = (
            "\n".join(software_config.demonstration) + delimiter
            if software_config.demonstration is not None
            else ""
        )

        instantiated_prompt = self.get_instantiated_prompt(
            input, software_config.prompt_template
        )

        result = (
            instantiated_instruction + demonstration + instantiated_prompt + delimiter
        )
        return result

    def evaluate(self, dataset_config: DatasetConfig) -> dict:
        ...

    def execute(self, input):
        if self.default_software_config.task == "scoring":
            # take the first value of the dict as input
            kernel = list(self.kernel_configs.values())[0].to_kernel()
            code = self.get_code(input, self.default_software_config)
            output = kernel.execute(code)
            return np.mean(output["prompt_token_probs"])
        else:
            kernel = self.kernel_configs["openai"].to_kernel()
            code = self.get_code(input, self.default_software_config)
            output = kernel.execute(code)
            result = self.normalize_output(output["text"])

            return result

    def pricing_without_input(self, input) -> float:
        return len(input)

    def pricing_with_input(self, input) -> float:
        return len(input)

    def to_prompt(self, input) -> str:
        prompt = self.get_code(input, self.default_software_config)
        return prompt

    def _example_prompt(self) -> str:
        if self.example is None:
            raise ValueError(
                "You need to specify an example for your software,"
                " which is a dictionary with the keys: input and output."
                " For example, for sentiment classifier"
                " software, an example could be:"
                " {'input':{'text':'I love this movie'}, "
                "'output':'positive'}"
            )
        prompt = self.get_code(self.example["input"], self.default_software_config)
        return prompt

    def infer_batch_samples(self, samples: list[dict]):
        """

        Args:
            samples: evaluated samples

        Returns:
            predictions

        """
        predictions = []
        # Create a promptware
        for sample in samples:
            result = self.execute(sample)
            predictions.append(result)
        return predictions
