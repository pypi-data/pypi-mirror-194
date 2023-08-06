from bleurt import score  # From: git+https://github.com/google-research/bleurt.git
import tensorflow

from promptware.promptware import Promptware

from .xyz2 import abc2  # From: https://github.com/ExpressAI/DataLab # noqa
from .xyz import abc  # noqa


class FooPromptware(Promptware):
    def __init__(self):
        self.fool = "fool"

    def fool(self) -> str:
        print(score)
        print(tensorflow)
        return "fool"


class Dummy1:
    pass
