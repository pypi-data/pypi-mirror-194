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


class SQLTranslatePromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to "
            "translate natural language to SQL queries.",
            creator="OpenAI",
            homepage="https://beta.openai.com/examples/",
            reference="",
            codebase_url="https://beta.openai.com/examples/",
            license=LicenseType.no_license,
            research_tasks=[TaskType.conditional_generation],
            application_categories=[ApplicationCategory.transformation],
            application_subcategories=[ApplicationSubcategory.translation],
            original_platform=PlatformType.gpt3,
            design_pattern=DesignPatternType.standalone,
            source_language=LanguageType.en,
            target_language=LanguageType.sql,
        )

    def _kernel_configs(self):
        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="code-davinci-002",
                max_tokens=150,
                temperature=0,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=["#", ";"],
            )
        }

    def _software_configs(self):
        return {
            "sql_translate": PromptConfig(
                name="sql_translate",
                description="This promptware is used to "
                "translate natural language to SQL queries.",
                instruction="### Postgres SQL tables, with their properties:\n#\n# "
                "Employee(id, name, department_id)\n"
                "# Department(id, name, address)\n"
                "# Salary_Payments(id, employee_id, amount, date)\n#\n### ",
                demonstration=[],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.conditional_generation,
            )
        }

    def _example(self):
        return {
            "input": {
                "text": "A query to list the names of the departments "
                "which employed more than 10 employees in the last 3 "
                "months\nSELECT"
            },
            "output": "d.name\nFROM\n    Department d\n    INNER JOIN Employee e ON "
            "d.id = e.department_id\n    INNER JOIN Salary_Payments sp ON "
            "e.id = sp.employee_id\nWHERE\n    sp.date >= DATE_SUB(CURDATE("
            "), INTERVAL 3 MONTH)\nGROUP BY\n    d.name\nHAVING\n    COUNT("
            "e.id) > 10",
        }
