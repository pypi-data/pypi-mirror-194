from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
from typing import Optional

from promptware import config
from promptware.constants.applications import (
    ApplicationCategory,
    ApplicationSubcategory,
)
from promptware.constants.design_patterns import DesignPatternType
from promptware.constants.languages import LanguageType
from promptware.constants.platforms import PlatformType
from promptware.constants.tasks import TaskType


@dataclass
class SoftwareInfo:
    description: str
    creator: Optional[str] = None
    homepage: Optional[str] = None
    reference: Optional[str] = None
    codebase_url: Optional[str] = None
    # The license of the software
    license: Optional[str] = None
    task: Optional[TaskType] = None  # this will be removed later
    # Tasks defined by research community
    research_tasks: Optional[list[TaskType]] = None
    # The categories of applicable scenarios
    application_categories: Optional[list[ApplicationCategory]] = None
    # The subcategories of applicable scenarios
    application_subcategories: Optional[list[ApplicationSubcategory]] = None
    # The original platform that the software lives in
    original_platform: Optional[PlatformType] = None
    # The design pattern of the software
    design_pattern: Optional[DesignPatternType] = None
    # The language of the software's input (e.g., instruction)
    source_language: Optional[LanguageType] = None
    # The language of the software's output (e.g., response)
    target_language: Optional[LanguageType] = None
    # The human feedback of this software
    human_feedback: Optional[str] = None

    # Set later by the builder
    module_name: Optional[str] = None
    config_name: Optional[str] = None
    kernel_configs: Optional[dict] = None
    software_configs: Optional[dict] = None
    dataset_configs: Optional[dict] = None
    example: Optional[dict] = None
    example_prompt: str = ""

    def serialize(self):
        return {
            "description": self.description,
            "creator": self.creator,
            "homepage": self.homepage,
            "reference": self.reference,
            "codebase_url": self.codebase_url,
            "license": self.license,
            "task": self.task,
            "research_tasks": self.research_tasks,
            "application_categories": self.application_categories,
            "application_subcategories": self.application_subcategories,
            "original_platform": self.original_platform,
            "design_pattern": self.design_pattern,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "module_name": self.module_name,
            "config_name": self.config_name,
            "kernel_configs": {
                config_name: asdict(config)
                for config_name, config in self.kernel_configs.items()
            },
            "software_configs": {
                config_name: config.serialize()
                for config_name, config in self.software_configs.items()
            },
            "dataset_configs": {
                config_name: asdict(config)
                for config_name, config in self.dataset_configs.items()
            }
            if self.dataset_configs is not None
            else None,
            "example": self.example,
            "example_prompt": self.example_prompt,
        }

    def write_to_directory(
        self,
        path_directory,
        file_name: Optional[str] = None,
        overwrite: bool = True,
    ):

        software_info = self.serialize()

        file_name = (
            file_name if file_name is not None else config.SOFTWARE_INFO_FILENAME
        )
        file_path = os.path.join(path_directory, file_name)

        # Checks the directory.
        if os.path.exists(path_directory):
            if not os.path.isdir(path_directory):
                raise RuntimeError(f"Not a directory: {path_directory}")
        else:
            os.makedirs(path_directory)

        # Checks the file.
        if os.path.exists(file_path):
            if not os.path.isfile(file_path):
                raise RuntimeError(f"Not a file: {file_path}")
            if not overwrite:
                raise RuntimeError(
                    f"Attempted to overwrite the existing file: {file_path}"
                )

        with open(file_path, "w") as f:
            # save dict as json file
            json.dump(software_info, f, indent=4)

        return file_path
