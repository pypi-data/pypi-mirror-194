from promptware.promptware import Promptware


class FooPromptware(Promptware):
    def __init__(self):
        self.fool = "fool"

    def fool(self) -> str:
        return "fool"


class Dummy1:
    pass
