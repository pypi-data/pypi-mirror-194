"""Interface of Huggingface's transformers library."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import warnings

import torch
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import (
    BeamSearchDecoderOnlyOutput,
    GreedySearchDecoderOnlyOutput,
    SampleDecoderOnlyOutput,
)

DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"


@dataclass
class HFConfig:
    name: str
    model: AutoModelForCausalLM
    config: AutoConfig
    tokenizer: AutoTokenizer


def load_hf_model(name: str) -> HFConfig:
    config = AutoConfig.from_pretrained(name)
    tokenizer = AutoTokenizer.from_pretrained(name, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(name, from_tf=False, config=config)
    model.to(DEVICE)

    return HFConfig(name, model, config, tokenizer)


def prepare_output_for_one_sequence(
    text: str,
    input_length: int,
    stop_sequences: str | None,
    tokenizer: AutoTokenizer,
    idx: int,
    sequences: torch.Tensor,
    scores: torch.Tensor,
    prompt_vocab_probs: list[torch.Tensor],
    prompt_token_probs: list[torch.Tensor],
) -> dict[str, Any]:
    """Prepare the output for one sequence.
    Args:
        text (str): The text to be generated.
        input_length (int): The length of the prompt.
        stop_sequences (str): The stop sequences.
        tokenizer (AutoTokenizer): The tokenizer.
        idx (int): The index of the sequence.
        sequences (torch.Tensor): The generated sequences.
        scores (torch.Tensor): The scores of the generated sequences.
        prompt_vocab_probs (list[torch.Tensor]): The vocab probabilities of the prompt.
        prompt_token_probs (list[torch.Tensor]): The token probabilities of the prompt.
    Returns:
        dict[str, Any]: The output for one sequence.
    """
    output_sequence = sequences[idx]

    # Get the generation probability
    token_probs: list[list[float]] = []
    generated_token_probs: list[float] = []

    for i in range(len(output_sequence[input_length:])):
        curr_token_prob = scores[i][idx]
        token_probs.append(curr_token_prob.cpu().detach().numpy().tolist())
        generated_token_probs.append(
            curr_token_prob[output_sequence[input_length + i]].item()
        )

    # Decode text, only decode the generated part
    out: str = tokenizer.decode(
        output_sequence[input_length:], clean_up_tokenization_spaces=True
    )
    # Decode prompt tokens
    prompt_tokens: list[str] = tokenizer.convert_ids_to_tokens(
        output_sequence[:input_length]
    )

    num_tokens = len(output_sequence[input_length:])

    # Truncate at stop sequences
    if stop_sequences is not None:
        stop_sequence_list = stop_sequences.split(",")
        shortest_out_before_stop_sequence = None
        for stop_sequence in stop_sequence_list:
            curr_out_before_stop_sequence = out.split(stop_sequence)[0]
            if shortest_out_before_stop_sequence is None:
                shortest_out_before_stop_sequence = curr_out_before_stop_sequence
            elif len(curr_out_before_stop_sequence) < len(
                shortest_out_before_stop_sequence
            ):
                shortest_out_before_stop_sequence = curr_out_before_stop_sequence
        if shortest_out_before_stop_sequence is None:
            raise ValueError(
                f"Stop sequence {stop_sequences} not found in output {out}"
            )
        out = shortest_out_before_stop_sequence
        num_tokens = len(tokenizer(out)["input_ids"]) - 1  # minus 1 means

    return {
        "prompt": text,
        "generation": out.replace(text, ""),
        "logprobs": {
            "prompt_tokens": prompt_tokens,
            "prompt_token_probs": prompt_token_probs,
            "prompt_vocab_probs": prompt_vocab_probs,
            "generation_token_probs": generated_token_probs[:num_tokens],
            "generation_vocab_probs": token_probs[:num_tokens],
        },
    }


def generate(
    hf_config: HFConfig,
    prompt: str,
    max_length: int = 256,
    do_sample: bool = False,
    num_beams: int = 1,
    no_repeat_ngram_size: int = 3,
    temperature: float = 1.0,
    top_k: int = 1,
    top_p: float = 0.8,
    repetition_penalty: float = 1.0,
    num_return_sequences: int = 1,
    stop_sequences: str | None = None,
):
    """Generate text using Huggingface's transformers library.
    Args:
        model_name_or_path (str): The name of the model to use.
        prompt (str): The text to use as input.
        max_tokens (int): The maximum length of the output.
        do_sample (bool): Whether to use sampling or not.
        num_beams (int): The number of beams to use.
        no_repeat_ngram_size (int): The maximum size of ngrams to not repeat.
        temperature (float): The temperature to use for sampling.
        top_k (int): The number of top tokens to sample from.
        top_p (float): The probability to sample from the top tokens.
        repetition_penalty (float): The penalty to apply for repeating tokens.
        best_of (int): The number of times to run the model and return the best result.
        stop_sequences (list[str]): The sequences to stop on.
    Returns:

    """

    # Load model and tokenizer
    config = hf_config.config
    tokenizer = hf_config.tokenizer
    model = hf_config.model

    model.eval()

    encoded = tokenizer(
        prompt,
        add_special_tokens=False,
        return_tensors="pt",
    )
    input_length = encoded["input_ids"].shape[1]
    output_max_lenth = input_length + max_length

    assert num_return_sequences > 0, "You have to return at least one sequence"

    # Length check
    if input_length > config.max_position_embeddings:
        warnings.warn(
            f"Input has reached max position embedding "
            f"{config.max_position_embeddings}, "
            f"will return None. Consider truncate the input text."
        )
    if input_length + max_length > config.max_position_embeddings:
        output_max_lenth = config.max_position_embeddings
        warnings.warn(
            f"Input + output has reached max position embedding "
            f"{config.max_position_embeddings}, "
            f"will use {config.max_position_embeddings - input_length}"
            f" as max output length instead"
        )

    if not do_sample:
        assert num_return_sequences <= num_beams, (
            f"You cannot return "
            f"{num_return_sequences} sequences "
            f"with a beam size"
            f" {num_beams}."
        )

    # Calculate the prompt probability
    encoded_text = encoded["input_ids"].to(DEVICE)
    attention_mask = encoded["attention_mask"].to(DEVICE)
    labels = encoded_text.clone().detach()
    outputs = model(
        input_ids=encoded_text, attention_mask=attention_mask, labels=labels
    )

    prompt_vocab_probs = []
    prompt_token_probs = []

    prompt_logits = outputs.logits.view(-1, model.config.vocab_size)
    prompt_logits = prompt_logits.log_softmax(dim=-1)
    for i in range(len(prompt_logits)):
        curr_token_prob = prompt_logits[i]
        prompt_vocab_probs.append(curr_token_prob.cpu().detach().numpy().tolist())
        prompt_token_probs.append(curr_token_prob[encoded_text[0][i]].item())

    if do_sample:
        output = model.generate(
            input_ids=encoded_text,
            max_length=output_max_lenth,
            no_repeat_ngram_size=no_repeat_ngram_size,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            do_sample=do_sample,
            repetition_penalty=repetition_penalty,
            num_return_sequences=num_return_sequences,
            output_scores=True,
            renormalize_logits=True,
            return_dict_in_generate=True,
        )
    else:
        output = model.generate(
            input_ids=encoded_text,
            max_length=output_max_lenth,
            num_beams=num_beams,
            no_repeat_ngram_size=no_repeat_ngram_size,
            repetition_penalty=repetition_penalty,
            num_return_sequences=num_beams,
            # We gather all the sequences for selection
            output_scores=True,
            renormalize_logits=True,
            return_dict_in_generate=True,
        )

    if isinstance(output, GreedySearchDecoderOnlyOutput):
        # num_beams=1, greedy=True, num_return_sequences=1
        return [
            prepare_output_for_one_sequence(
                text=prompt,
                input_length=input_length,
                stop_sequences=stop_sequences,
                tokenizer=tokenizer,
                idx=0,
                sequences=output.sequences,
                scores=output.scores,
                prompt_token_probs=prompt_token_probs,
                prompt_vocab_probs=prompt_vocab_probs,
            )
        ]

    elif isinstance(output, BeamSearchDecoderOnlyOutput):
        best_idxs = torch.topk(output.sequences_scores, k=num_return_sequences)[
            1
        ]  # We take the indices
        res = []
        for best_idx in best_idxs:
            res.append(
                prepare_output_for_one_sequence(
                    text=prompt,
                    input_length=input_length,
                    stop_sequences=stop_sequences,
                    tokenizer=tokenizer,
                    idx=best_idx,
                    sequences=output.sequences,
                    scores=output.scores,
                    prompt_token_probs=prompt_token_probs,
                    prompt_vocab_probs=prompt_vocab_probs,
                )
            )
        return res

    elif isinstance(output, SampleDecoderOnlyOutput):
        res = []
        for idx in range(num_return_sequences):
            res.append(
                prepare_output_for_one_sequence(
                    text=prompt,
                    input_length=input_length,
                    stop_sequences=stop_sequences,
                    tokenizer=tokenizer,
                    idx=idx,
                    sequences=output.sequences,
                    scores=output.scores,
                    prompt_token_probs=prompt_token_probs,
                    prompt_vocab_probs=prompt_vocab_probs,
                )
            )
        return res
    else:
        print(f"output: {output}")
        raise NotImplementedError
