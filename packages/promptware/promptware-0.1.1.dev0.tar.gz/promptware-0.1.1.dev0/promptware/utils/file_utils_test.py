"""This script implements the unittest for file_utils.py"""

import os
from unittest import TestCase

from promptware.utils.file_utils import cached_path, get_from_cache


class TestFile_utils(TestCase):
    def test_get_from_cache(self):
        url = "https://datalab-hub.s3.amazonaws.com/sst2/test-SST2.tsv"
        # There are three newly-generated files will be generated:
        # (1) downloaded filed with the name of hash code, e.g. 012345
        # and download_file_path is the path of this file
        # (2) json file with the name of 012345.json that store the metadata info
        # (3) lock file with the name of 012345.lock
        download_file_path = get_from_cache(url)
        print(download_file_path)
        self.assertTrue(os.path.exists(download_file_path))

    def test_get_from_cache_zip_file(self):
        url = "https://nlp.stanford.edu/projects/snli/snli_1.0.zip"
        download_file_path = get_from_cache(url)
        self.assertTrue(os.path.exists(download_file_path))

    def test_cached_path(self):
        url = "https://datalab-hub.s3.amazonaws.com/sst2/test-SST2.tsv"
        cached_file_path = cached_path(url)
        self.assertTrue(os.path.exists(cached_file_path))

    def test_cached_path_zip_file(self):
        url = "https://nlp.stanford.edu/projects/snli/snli_1.0.zip"
        cached_file_path = cached_path(url)
        self.assertTrue(os.path.exists(cached_file_path))
