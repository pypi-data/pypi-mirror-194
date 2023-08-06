from __future__ import annotations

import importlib
import inspect
import os
from unittest import TestCase

from promptware.artifacts.utils import test_artifacts_path
from promptware.load import (
    _download_additional_modules,
    convert_github_url,
    get_imports,
    HubSoftwareModuleFactory,
    import_main_class,
    init_ep_modules,
    install,
    LocalSoftwareModuleFactory,
    software_module_factory,
)
from promptware.module_test import FooPromptware
from promptware.promptware import PromptConfig, Promptware
from promptware.utils.file_utils import DownloadConfig


class TestLoad(TestCase):

    artifact_module_path = os.path.join(test_artifacts_path, "test_modules")

    def test_init_ep_modules(self):
        ep_modules_cache = init_ep_modules()
        # "/usr2/home/pliu3/.cache/expressai/modules"
        print(ep_modules_cache)

    def test_import_main_class(self):

        module_path = "promptware.module_test"
        module_main_cls = import_main_class(module_path, Promptware)
        self.assertEqual(module_main_cls, FooPromptware)

    def test_convert_github_url(self):

        url_path = "https://github.com/ExpressAI/Promptware"
        url_path_full, sub_directory = convert_github_url(url_path)
        self.assertEqual(
            url_path_full, "https://github.com/ExpressAI/Promptware/archive/main.zip"
        )

    def test_get_imports(self):

        file_path = os.path.join(self.artifact_module_path, "foo_prompt.py")
        result = get_imports(file_path)
        # print(result)
        imports = [
            (
                "library",
                "bleurt",
                "git+https://github.com/google-research/bleurt.git",
                None,
            ),
            ("library", "tensorflow", "tensorflow", None),
            ("library", "promptware", "promptware", None),
            (
                "external",
                "xyz2",
                "https://github.com/ExpressAI/DataLab/archive/main.zip",
                "DataLab-main",
            ),
            ("internal", "xyz", "xyz", None),
        ]
        self.assertEqual(result.sort(), imports.sort())

    def test_download_additional_modules(self):
        imports = [
            (
                "external",
                "xyz2",
                "https://github.com/ExpressAI/DataLab/archive/main.zip",
                "DataLab-main",
            )
        ]
        local_imports = _download_additional_modules(
            name="test",
            base_path="test",
            imports=imports,
            download_config=DownloadConfig(extract_compressed_file=True),
        )
        """
        Result:
        [('XYZ2', '/usr2/home/pliu3/.cache/expressai/evaluate/downloads/extracted/
        220d868651ffa386acbc3a59532ae19562f550515e5a2bb439a8ff14ba0876bc/DataLab-main'
        )]
        """
        print(local_imports)

    def test_local_software_module_factory(self):
        path = os.path.join(self.artifact_module_path, "boo_prompt.py")

        imported_module_config = LocalSoftwareModuleFactory(
            path=path,
            download_config=DownloadConfig(extract_compressed_file=True),
        ).get_module()
        # print(imported_module_config.module_path)
        self.assertEqual(
            imported_module_config.module_path.endswith("boo_prompt"),
            True,
        )

    def test_software_module_factory(self):
        path = os.path.join(self.artifact_module_path, "boo_prompt.py")

        imported_module_config = software_module_factory(
            path,
            download_config=DownloadConfig(extract_compressed_file=True),
        )
        self.assertEqual(
            imported_module_config.module_path.endswith("boo_prompt"),
            True,
        )

    def test_load(self):
        path = os.path.join(self.artifact_module_path, "boo_prompt.py")

        imported_cls = install(
            path,
            download_config=DownloadConfig(extract_compressed_file=True),
        )
        # print(imported_cls())
        self.assertEqual(True, isinstance(imported_cls, type))

    def test_hub_software_module_factory(self):

        imported_module_config = HubSoftwareModuleFactory(
            name="sentiment",
            download_config=DownloadConfig(extract_compressed_file=False),
        ).get_module()

        module = importlib.import_module(imported_module_config.module_path)

        # Find the main class in our imported module
        module_main_cls = None
        for name, obj in module.__dict__.items():
            # We only want to get the inheritance class of the `main_cls_type`
            if isinstance(obj, PromptConfig):
                if inspect.isabstract(obj):
                    continue
                module_main_cls = obj
                break

        print(module_main_cls)

        # promptware = Promptware(prompt_config=module_main_cls)
        # input = {"text": "I love this movie"}
        # result = promptware.execute(input)
        # print(result)
