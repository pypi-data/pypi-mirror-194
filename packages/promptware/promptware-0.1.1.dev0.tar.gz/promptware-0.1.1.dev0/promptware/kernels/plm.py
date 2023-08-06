from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from typing import Optional

import cohere
import openai

from promptware import config
from promptware.kernels.api import huggingface as hf
from promptware.kernels.kernel import Kernel, KernelConfig


@dataclass
class PLMKernelConfig(KernelConfig):
    platform: str = "openai"
    model_name: str = "text-curie-001"
    max_tokens: int = 64
    temperature: float = 0.7
    top_p: float = 1
    suffix: str = ""
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    logprobs: float = 1
    n: int = 1
    echo: bool = False
    stop: object = None

    def to_kernel(self) -> Kernel:
        return PLMKernel(self)

    @classmethod
    def from_dict(cls, data_dict: dict) -> PLMKernelConfig:
        field_names = set(f.name for f in dataclasses.fields(cls))
        return cls(**{k: v for k, v in data_dict.items() if k in field_names})


class PLMKernel(Kernel):
    def __init__(self, config: Optional[PLMKernelConfig] = None):

        self.config = (
            config
            if config is not None
            else PLMKernelConfig(
                platform="openai",
                model_name="text-curie-001",
                suffix="",
                temperature=0,
                max_tokens=10,
                logprobs=1,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                n=1,
                echo=False,
                stop=None,
            )
        )
        self.hf_config = hf.load_hf_model(self.config.model_name)

    def execute(self, code) -> dict[str, str]:

        if self.config.platform == "openai":
            openai.api_key = config.os_api_key
            response = openai.Completion.create(
                model=self.config.model_name,
                prompt=code,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                frequency_penalty=self.config.frequency_penalty,
                presence_penalty=self.config.presence_penalty,
                logprobs=self.config.logprobs,
                n=self.config.n,
                echo=self.config.echo,
                stop=self.config.stop,
            )

            out = {
                "text": response["choices"][0]["text"],
                "token_logprobs": response["choices"][0]["logprobs"]["token_logprobs"],
                "tokens": response["choices"][0]["logprobs"]["tokens"],
            }

        elif self.config.platform == "huggingface":
            response = hf.generate(
                self.hf_config,
                prompt=code,
                max_length=self.config.max_tokens,
                do_sample=False,
                num_beams=1,
                stop_sequences=self.config.stop,
            )
            out = {
                "text": response[0]["generation"],
                "prompt_tokens": response[0]["logprobs"]["prompt_tokens"],
                "prompt_token_probs": response[0]["logprobs"]["prompt_token_probs"],
            }

        elif self.config.platform == "cohere":
            co = cohere.Client(config.os_api_key)
            response = co.generate(
                model=self.config.model_name,
                prompt=code,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                k=0,
                p=0.75,
                frequency_penalty=self.config.frequency_penalty,
                presence_penalty=self.config.presence_penalty,
                stop_sequences=[],
                return_likelihoods="NONE",
            )
            out = {
                "text": response.generations[0].text,
                "token_logprobs": None,
                "tokens": None,
            }

        #
        # output = self.normalize_output(out)

        return out
