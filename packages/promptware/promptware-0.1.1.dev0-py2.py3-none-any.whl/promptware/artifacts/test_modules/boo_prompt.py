from promptware.promptware import Promptware

from .xyz import abc  # noqa


class BooPromptware(Promptware):
    def __init__(self):
        self.fool = "fool"

    def fool(self) -> str:
        return "fool"


class Dummy1:
    pass
