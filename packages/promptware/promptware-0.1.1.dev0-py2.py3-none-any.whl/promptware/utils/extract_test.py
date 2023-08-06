"""This script implements unittest for extract.py"""

import os
from unittest import TestCase

from promptware.utils.extract import ExtractManager
from promptware.utils.file_utils import get_from_cache


class TestExtractManager(TestCase):
    def test_extract_manager(self):
        url = "https://nlp.stanford.edu/projects/snli/snli_1.0.zip"
        download_file_path = get_from_cache(url)
        self.extracted_file_path = ExtractManager().extract(download_file_path)
        """
        Example of extracted_file_path:
        /usr2/home/pliu3/.cache/huggingface/evaluate/downloads/
        extracted/05084283f5c55052de5fee6cd91f903f1c8b990dae49bf86d4107028488c217d
        where following files are included:
        * snli_1.0
        """
        self.assertTrue(os.path.exists(self.extracted_file_path))
