"""Definition of task for prompt."""
from __future__ import annotations

from enum import Enum


class TaskType(str, Enum):
    """Task types available in this tool."""

    text_classification = "text-classification"
    named_entity_recognition = "named-entity-recognition"
    qa_extractive = "qa-extractive"
    summarization = "summarization"
    machine_translation = "machine-translation"
    text_pair_classification = "text-pair-classification"
    aspect_based_sentiment_classification = "aspect-based-sentiment-classification"
    kg_link_tail_prediction = "kg-link-tail-prediction"
    qa_multiple_choice = "qa-multiple-choice"
    qa_open_domain = "qa-open-domain"
    qa_tat = "qa-tat"
    conditional_generation = "conditional-generation"
    word_segmentation = "word-segmentation"
    language_modeling = "language-modeling"
    chunking = "chunking"
    cloze_mutiple_choice = "cloze-multiple-choice"
    cloze_generative = "cloze-generative"
    grammatical_error_correction = "grammatical-error-correction"
    meta_evaluation_wmt_da = "meta-evaluation-wmt-da"
    tabular_regression = "tabular-regression"
    tabular_classification = "tabular-classification"
    argument_pair_extraction = "argument-pair-extraction"
    ranking_with_context = "ranking-with-context"
    argument_pair_identification = "argument-pair-identification"
    meta_evaluation_nlg = "meta-evaluation-nlg"

    # unsupported by explainaboard
    antonym_identification = "antonym-identification"
    others = "others"

    @staticmethod
    def list() -> list[str]:
        """Obtains string representations of all values.

        Returns:
            List of all values in str.
        """
        return list(map(lambda c: c.value, TaskType))
