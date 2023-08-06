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


class QueryDocMatchingPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This software is to identify if a query semantically "
            "relevant to a document.",
            creator="Promptware Authors",
            homepage="https://github.com/expressai/promptware",
            reference="",
            codebase_url="https://github.com/expressai/promptware/tree/main/softwares",
            license=LicenseType.apache_2_0,
            research_tasks=[TaskType.text_pair_classification],
            application_categories=[ApplicationCategory.classification],
            application_subcategories=[ApplicationSubcategory.general_classification],
            original_platform=PlatformType.gpt3,
            design_pattern=DesignPatternType.standalone,
            source_language=LanguageType.en,
            target_language=LanguageType.en,
        )

    def _kernel_configs(self):
        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="text-davinci-002",
                max_tokens=64,
                temperature=0,
            )
        }

    def _software_configs(self):
        return {
            "query_doc_matching": PromptConfig(
                name="query_doc_matching",
                description="This software is to identify if a query semantically "
                "relevant to a document.",
                instruction="Decide whether the documents are relevant to the given "
                "search query:\n",
                demonstration=[
                    "Query: Jackie Chan's birthday\nDocuments: "
                    "https://en.wikipedia.org/wiki/Jackie_Chan|Jackie Chan - "
                    "Wikipedia|Fang Shilong (born 7 April 1954), known professionally "
                    "in English as Jackie Chan and in Chinese as Cheng Long, is a Hong"
                    " Kong actor, filmmaker, "
                    "martial artist, and stuntman known for his slapstick acrobatic "
                    "fighting style, comic timing, and innovative stunts, which he "
                    "typically performs himself. Chan has been acting since the "
                    "1960s, performing in more than 150 films. He is one of the most "
                    "popular action film stars of all time.\nResult: Relevant\n",
                    "Query:Pengfei Liu in "
                    "NLP\nDocuments:https://scholar.google.com/citations?user"
                    "=oIz_CYEAAAAJ&hl=en|‪Pengfei Liu‬ - ‪Google Scholar|Carnegie "
                    "Mellon University -‪Natural Language Processing‬ - ‪Text "
                    "Summarization‬ - ‪Diagnosis for NLP Models‬ - "
                    "‪Multi-task/Transfer\nResult: Relevant\n‬",
                    "Query: Chinese New Year 2023\nDocuments: "
                    "https://en.wikipedia.org/wiki/Tang_dynasty|Tang dynasty - "
                    "Wikipedia| The Tang dynasty, or Tang Empire, was an imperial "
                    "dynasty of China that ruled from 618 to 907 AD, with an "
                    "interregnum between 690 and 705. It was preceded by the Sui "
                    "dynasty and followed by the Five Dynasties and Ten Kingdoms "
                    "period.\nResult:Not relevant\n",
                ],
                prompt_template=lambda input: f"Query: {input['query']}\nDocuments:"
                f"{input['document']['link']} | "
                f"{input['document']['title']}"
                f" | {input['document']['document']}"
                f"\nResult: ",
                task=TaskType.text_pair_classification,
            )
        }

    def _example(self):
        return {
            "input": {
                "query": "Zhiyuan Liu address",
                "document": {
                    "title": "Zhiyuan Liu",
                    "link": "https://nlp.csai.tsinghua.edu.cn/~lzy/",
                    "document": " I'm an associate professor at Tsinghua "
                    "University. I am "
                    "always looking for highly-motivated post-docs "
                    "and "
                    "visiting scholars to work together on natural "
                    "language "
                    "processing, knowledge graphs, and social "
                    "computing. "
                    "Please read the Natural Language Processing. "
                    "Language: "
                    "English. The degree course of CS graduate "
                    "students ("
                    "specially for the Master Program of Advanced "
                    "Programming) at Tsinghua University. [ "
                    "Foundations of "
                    "Object-Oriented Programming. Language: Chinese. "
                    "The "
                    "compulsory course of CS undergraduate students "
                    "at "
                    "Tsinghua University.",
                },
            },
            "output": "",
        }
