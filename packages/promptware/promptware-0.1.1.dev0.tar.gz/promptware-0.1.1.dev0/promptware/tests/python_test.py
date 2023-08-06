"""Unittest for Python Kernel."""

import unittest

from promptware.kernels.python import PythonKernel


class TestUnittest(unittest.TestCase):
    def test_python(self):
        python = PythonKernel()
        input = "a=2; b=3; result = a + b"
        output = python.execute(input)
        self.assertEqual(
            output,
            {
                "a": 2,
                "b": 3,
                "result": 5,
            },
        )
