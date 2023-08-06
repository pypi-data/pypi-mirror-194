"""Definition of applications for software."""
from __future__ import annotations

from enum import Enum


class ApplicationCategory(str, Enum):
    """Application category available in this tool."""

    conversation = "conversation"
    classification = "classification"
    generation = "generation"
    brainstorming = "brainstorming"
    transformation = "transformation"
    interactivity = "interactivity"

    others = "others"

    @staticmethod
    def list() -> list[str]:
        """Obtains string representations of all values.

        Returns:
            List of all values in str.
        """
        return list(map(lambda c: c.value, ApplicationCategory))


class ApplicationSubcategory(str, Enum):
    """Sub Application category available in this tool."""

    # conversation
    question_answering = "question-answering"
    specialized_educational_dialogs = "specialized-educational-dialogs"
    open_ended_conversation = "open-ended-conversation"

    # classification
    general_classification = "general-classification"
    ordering = "ordering"
    sentiment_analysis = "sentiment-analysis"
    code_language_classification = "code-language-classification"

    # generation
    text_generation = "text-generation"
    code_generation = "code-generation"
    data_generation = "data-generation"

    # brainstorming
    advice_giving = "advice-giving"
    recommendation = "recommendation"
    how_to_generation = "how-to-generation"

    # transformation
    rewriting = "rewriting"
    extraction = "extraction"
    summarization = "summarization"
    explanation = "explanation"
    translation = "translation"

    # other
    value_judgment = "value-judgment"
    hack_identification = "hack-identification"
    internet_search = "internet-search"
    new_information = "new-information"
    others = "others"

    @staticmethod
    def list() -> list[str]:
        """Obtains string representations of all values.

        Returns:
            List of all values in str.
        """
        return list(map(lambda c: c.value, ApplicationSubcategory))
