import unittest

from promptware.utils.py_util import generate_format_func


class TestPYUtils(unittest.TestCase):
    def test_generate_format_func(self):

        # convert a string to lambda function
        pattern = "[Query]:{query}\n[Documents]:{documents}\n[URL]:{url}"

        # f = lambda input: f"{input['query']} {input['documents']} {input['url']}"
        f = generate_format_func(pattern)

        input = {"query": "query", "documents": "documents", "url": "url"}
        # print(f(input))

        self.assertEqual(f(input), "[Query]:query\n[Documents]:documents\n[URL]:url")

    def test_generate_format_func_no_bracket(self):

        pattern = "Input:"
        f = generate_format_func(pattern)
        input = "I love this movie"
        self.assertEqual(f(input), input)

    # def test_get_files_from_directory(self):
    #     path = "/usr2/home/pliu3/data/expressAI/Davinci/softwares/summarization"
    #     files = get_files_from_directory(path)
    #     self.assertEqual(len(files), 6)
    #
    #
    # def test_get_software_path_from_directory(self):
    #     path = "/usr2/home/pliu3/data/expressAI/Davinci/softwares/summarization"
    #     files = get_software_path_from_directory(path)
    #     print("------------")
    #     for file in files:
    #         print(file)
    #     self.assertEqual(len(files), 2)
