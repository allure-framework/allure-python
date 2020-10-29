import sys
import types
from importlib import util
from doctest import script_from_examples
from nose2 import events


class CurrentExample(events.Plugin):
    commandLineSwitch = (None, "current-example", "Method docstring to module")

    def __init__(self, *args, **kwargs):
        super(CurrentExample, self).__init__(*args, **kwargs)
        self._current_docstring = ""

    def startTest(self, event):
        if hasattr(event.test, "_testFunc"):
            self._current_docstring = event.test._testFunc.__doc__
        else:
            self._current_docstring = event.test._testMethodDoc

    def get_example_module(self):
        module = types.ModuleType("stub")
        if self._current_docstring:
            code = script_from_examples(self._current_docstring)
            spec = util.spec_from_loader("example_module", origin="example_module", loader=None)
            module = util.module_from_spec(spec)
            exec(code, module.__dict__)
        sys.modules['example_module'] = module
        return module
