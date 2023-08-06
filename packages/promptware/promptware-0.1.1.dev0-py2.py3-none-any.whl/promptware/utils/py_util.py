from __future__ import annotations

from hashlib import sha256
import logging
import os
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def generate_format_func(pattern: str):
    """
    Generate a format function for a string with patter {}
    Args:
        pattern: a string with curly brackets, e.g., "[Query]:{query}\n[Documents]:{
        documents}\n[URL]:{url}"

    Returns:
    a function that takes an dictionary and returns a formatted string
    """

    arguments = re.findall(r"\{([^}]+)\}", pattern)

    if len(arguments) == 0:
        logger.warning(
            f"No arguments found in pattern: {pattern}, your input sample should be a "
            f"string, which will be regarded as the input"
        )
        return lambda d: d

    def format_func(input: dict[str, str]) -> str:
        """
        Generate a formatted string from the given dictionary.
        Args:
            input: a dictionary, for example
            input = {
                "query": "query",
                "documents": "documents",
                "url": "url"
            }
        Returns:
        a formatted string. for example: "[Query]:query\n[Documents]:documents\n[
        URL]:url"
        """

        result = pattern
        for arg in arguments:
            if arg not in input:
                raise KeyError(f"{arg} is not in your input sample")
            result = result.replace("{" + arg + "}", input[arg])

        return result

    return format_func


def hash_url_to_filename(url, etag=None):
    """
    Convert `url` into a hashed filename in a repeatable way.
    If `etag` is specified, append its hash to the url's, delimited
    by a period.
    If the url ends with .h5 (Keras HDF5 weights) adds '.h5' to the name
    so that TF 2.0 can identify it as a HDF5 file
    (see https://github.com/tensorflow/tensorflow/blob/00fad90125b18b80f
    e054de1055770cfb8fe4ba3/tensorflow/python/keras/engine/network.py#L1380)
    """
    url_bytes = url.encode("utf-8")
    url_hash = sha256(url_bytes)
    filename = url_hash.hexdigest()

    if etag:
        etag_bytes = etag.encode("utf-8")
        etag_hash = sha256(etag_bytes)
        filename += "." + etag_hash.hexdigest()

    if url.endswith(".py"):
        filename += ".py"

    return filename


def _hash_python_lines(lines: list[str]) -> str:
    filtered_lines = []
    for line in lines:
        line = re.sub(r"#.*", "", line)  # remove comments
        if line:
            filtered_lines.append(line)
    full_str = "\n".join(filtered_lines)

    # Make a hash from all this code
    full_bytes = full_str.encode("utf-8")
    return sha256(full_bytes).hexdigest()


def get_files_from_directory(path_directory: str):
    """
    Get all files in a directory recursively
    Args:
        path_directory: a directory

    Returns:
        a list of files
    """

    files = []
    for root, _, filenames in os.walk(path_directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files


def get_software_path_from_directory(path_directory):
    """
    Get all files in a directory recursively
    Args:
        path_directory: a directory

    Returns:
        a list of files
    """

    return [
        file_name
        for file_name in get_files_from_directory(path_directory)
        if file_name.split("/")[-1] in ["software.json", "software.py"]
    ]
