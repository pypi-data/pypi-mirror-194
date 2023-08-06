import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import ExplainCodePromptware  # noqa


class TestExplainCodePromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = ExplainCodePromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    '''
    def test_execute_general(self):
        software = ExplainCodePromptware(config_name="default")
        input = {"code": """class Log:
def __init__(self, path):
    dirname = os.path.dirname(path)
    os.makedirs(dirname, exist_ok=True)
    f = open(path, "a+")

    # Check that the file is newline-terminated
    size = os.path.getsize(path)
    if size > 0:
        f.seek(size - 1)
        end = f.read(1)
        if end != "\n":
            f.write("\n")
    self.f = f
    self.path = path

def log(self, event):
    event["_event_id"] = str(uuid.uuid4())
    json.dump(event, self.f)
    self.f.write("\n")

def state(self):
    state = {"complete": set(), "last": None}
    for line in open(self.path):
        event = json.loads(line)
        if event["type"] == "submit" and event["success"]:
            state["complete"].add(event["id"])
            state["last"] = event
    return state"""}
        result = software.execute(input)
        print(result)
        self.assertGreater(len(result), 0)

    def test_execute_python(self):
        software = ExplainCodePromptware(config_name="python")
        input = {"code": """# Python 3
def remove_common_prefix(x, prefix, ws_prefix):
    x["completion"] = x["completion"].str[len(prefix) :]
    if ws_prefix:
        # keep the single whitespace as prefix
        x["completion"] = " " + x["completion"]
return x """}
        result = software.execute(input)
        print(result)
        self.assertGreater(len(result), 0)
    '''
