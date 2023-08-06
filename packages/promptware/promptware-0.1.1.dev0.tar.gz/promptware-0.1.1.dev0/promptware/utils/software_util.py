"""Utils for Software."""
import numpy as np

from promptware.info import SoftwareInfo
from promptware.kernels.plm import PLMKernelConfig
from promptware.promptware import PromptConfig, Promptware


def develop_custom_software_from_prompt(
    prompt: str,
    format_func,
    example: dict,
    config_name=None,
    kernel_config: dict = None,
    task: str = None,
):
    """Develop custom software from prompt."""

    class CustomSoftware(Promptware):
        def _info(self) -> SoftwareInfo:
            return SoftwareInfo(
                description="custom software",
            )

        def _example(self):
            return example

        def _kernel_configs(self):
            return (
                {
                    "openai": PLMKernelConfig(
                        platform="openai",
                        model_name="text-curie-001",
                        max_tokens=64,
                        temperature=0,
                    )
                }
                if kernel_config is None
                else {"openai": PLMKernelConfig.from_dict(kernel_config)}
            )

        def _software_configs(self):
            return {
                config_name: PromptConfig(
                    name=config_name,
                    description="This is custom software",
                    instruction="not defined",
                    demonstration=[],
                    prompt_template=format_func,
                    task=task,
                )
            }

        def get_code(self, input: dict, software_config) -> str:
            delimiter = "\n"

            instantiated_input = self.get_instantiated_prompt(
                input, software_config.prompt_template
            )

            code = prompt + delimiter + instantiated_input

            return code

        def execute(self, input):
            if task == "scoring":
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

    return CustomSoftware(
        config_name=config_name,
    )
