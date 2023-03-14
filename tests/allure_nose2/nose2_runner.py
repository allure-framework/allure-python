import importlib.machinery
import importlib.util
from doctest import script_from_examples
from nose2 import main
from pytest import FixtureRequest, Pytester
from tests.e2e import AllureFrameworkRunner


class AllureNose2Runner(AllureFrameworkRunner):
    LOGGER_PATH = "allure_nose2.plugin.AllureFileLogger"

    def __init__(self, request: FixtureRequest, pytester: Pytester):
        super().__init__(request, pytester, AllureNose2Runner.LOGGER_PATH)

    def run_docstring(self):
        docstring = self._find_docstring()
        example_code = script_from_examples(docstring)
        spec = importlib.machinery.ModuleSpec(self.request.node.name, None)
        module = importlib.util.module_from_spec(spec)
        return self._run(module, example_code)

    def _run_framework(self, module, example):
        # We execute the example here because the _run_framework runs in a
        # nested allure context. Otherwise, all allure decorators used in the
        # example would affect allure results of the testing system itself.
        exec(example, module.__dict__)
        main(
            module=module,
            argv=["nose2", "--allure"],
            plugins=["allure_nose2.plugin"],
            exit=False
        )


__all__ = ["AllureNose2Runner"]
