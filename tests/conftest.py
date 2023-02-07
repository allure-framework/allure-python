import pytest
import mock
import shutil
import runpy
import warnings
import docutils.nodes
import docutils.parsers.rst
import docutils.utils
import docutils.frontend
from pathlib import Path
from doctest import script_from_examples
from contextlib import contextmanager
from typing import Mapping, Tuple, TypeVar
from pytest import FixtureRequest, Pytester

import allure_commons
from allure_commons_test.report import AllureReport
from allure_commons.logger import AllureMemoryLogger

pytest_plugins = "pytester"


def pytest_configure(config: pytest.Config):
    config.addinivalue_line(
        "markers", "real_logger: mark test to run with a real allure logger"
    )


@contextmanager
def fake_logger(path :str = None) -> None:
    if path is None:
        path = "allure_commons.logger.AllureFileLogger"
    blocked_plugins = []
    for name, plugin in allure_commons.plugin_manager.list_name_plugin():
        allure_commons.plugin_manager.unregister(plugin=plugin, name=name)
        blocked_plugins.append(plugin)

    with mock.patch(path) as ReporterMock:
        ReporterMock.return_value = AllureMemoryLogger()
        yield ReporterMock.return_value

    for plugin in blocked_plugins:
        allure_commons.plugin_manager.register(plugin)


def get_docstring(node: pytest.Item) -> str:
    if isinstance(node, pytest.Function):
        return node.function.__doc__
    elif isinstance(node, pytest.Class):
        return node.cls.__doc__
    elif isinstance(node, pytest.Module):
        return node.module.__doc__
    elif isinstance(node, pytest.Package):
        return node.obj.__doc__
    return None


def get_path_from_docstring(request: FixtureRequest) -> Path:
    return request.config.rootpath.joinpath(
        get_docstring(request.node).strip()
    )

RstExampleTableT = TypeVar("RstExampleTableT", bound="RstExampleTable")
class RstExampleTable:

    STASH_KEY = pytest.StashKey()

    def __init__(self, filepath: str|Path) -> None:
        self.source = filepath
        self.examples = self.load_examples(filepath)

    def __getitem__(self, name: str) -> str:
        if name not in self.examples:
            raise KeyError(f"Code block {name!r} not found in {self.source}")
        return self.examples[name]

    @staticmethod
    def find_examples(request: FixtureRequest) -> RstExampleTableT:
        """Loads code examples, associated with the test node or one of its
        parents.

        Arguments:
            request (FixtureRequest): the request fixture

        Returns (RstExampleTable): A table containing the examples, indexed by
            their names from the .rst document

        Notes:
            It first finds a docstring defined on the function, class, module or
            package associated with the node. If multiple docstrings exist,
            the one defined on a lower level wins.

            The docstring content is used then as the path to the
            reStructuredText document. The document is parsed and all its code
            blocks are combined in a dictionary mapping their names to the code
            blocks themselves. The mapping can be accessed through the returned
            instance of RstExampleTable class.

            The table is then cached in a stash of the same node from which the
            original docstring was loaded. This prevents from parsing the same
            document several times if multiple tests from the same module/package
            (or parametrizations of the same metafunc) are testing the examples
            from the same document.
        """

        node, docstring = RstExampleTable.find_node_with_docstring_or_throw(
            request
        )
        examples = RstExampleTable.__get_from_cache(node)
        if examples is None:
            examples = RstExampleTable.__create_and_cache(node, docstring)
        return examples

    @staticmethod
    def find_node_with_docstring(
        request: FixtureRequest
    ) -> Tuple[pytest.Item, str]:
        node = request.node
        while node:
            docstring = get_docstring(node)
            if docstring:
                break
            node = node.parent
        return node, docstring

    @staticmethod
    def find_node_with_docstring_or_throw(
        request: FixtureRequest
    ) -> Tuple[pytest.Item, str]:
        node, docstring = RstExampleTable.find_node_with_docstring(request)
        if node is None:
            nodeid = request.node.nodeid
            raise ValueError(f"Unable to get docstring for node {nodeid}")
        return node, docstring

    @staticmethod
    def load_examples(filepath: str|Path) -> Mapping[str, str]:
        document = RstExampleTable.parse_rst(filepath)
        return {
            name: code_block.astext()
            for code_block in document.findall(
                RstExampleTable.__filter
            ) for name in code_block["names"]
        }

    @staticmethod
    def parse_rst(filepath: str|Path) -> docutils.nodes.document:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            parser = docutils.parsers.rst.Parser()
            components = (docutils.parsers.rst.Parser,)
            settings = docutils.frontend.OptionParser(
                components=components
            ).get_default_values()
            document = docutils.utils.new_document(
                str(filepath),
                settings=settings
            )
            with open(filepath, encoding="utf-8") as f:
                content = f.read()
            parser.parse(content, document)
            return document

    @staticmethod
    def __get_from_cache(node):
        if RstExampleTable.STASH_KEY in node.stash:
            return node.stash[RstExampleTable.STASH_KEY]

    @staticmethod
    def __create_and_cache(node, path):
        filepath = node.config.rootpath.joinpath(path.strip())
        if not filepath.exists() or filepath.is_dir():
            raise ValueError(
                f"Document, referred by {node.nodeid}, "
                f"doesn't exist at {filepath}"
            )
        examples = RstExampleTable.load_examples(filepath)
        node.stash[RstExampleTable.STASH_KEY] = examples
        return examples

    @staticmethod
    def __filter(node):
        return isinstance(
            node,
            docutils.nodes.literal_block
        ) and "code" in node["classes"] and node["names"]


class AlluredTestdir:
    def __init__(self, pytester: Pytester, request: FixtureRequest):
        self.testdir = pytester
        self.request = request
        self.allure_report = None
        self.plugins = ["allure_pytest", "allure_pytest_bdd"]
        self.enabled_plugins = {"allure_pytest"}

    def select_plugins(self, *plugins: str):
        self.enabled_plugins = set(plugins)

    def get_plugin_args(self):
        for plugin_package in self.plugins:
            yield "-p"
            if plugin_package in self.enabled_plugins:
                yield plugin_package
            else:
                yield f"no:{plugin_package}"

    def parse_docstring_source(self):
        docstring = self.request.node.function.__doc__ or self.request.node.module.__doc__
        source = script_from_examples(docstring).replace("#\n", "\n")
        return self.testdir.makepyfile(source)

    def parse_docstring_path(self):
        example_file = self.__get_example_path()
        with open(example_file, encoding="utf-8") as f:
            content = f.read()
            source = script_from_examples(content)
            return self.testdir.makepyfile(source)

    def copy_docstring_dir(self):
        example_dir = get_path_from_docstring(self.request)
        return shutil.copytree(
            example_dir,
            self.testdir.path,
            symlinks=True,
            dirs_exist_ok=True
        )

    def run_with_allure(self, *args: str, **kwargs: str):
        pytest_args = [
            "--alluredir",
            self.testdir.path,
            *self.get_plugin_args(),
            *args
        ]
        if self.request.node.get_closest_marker("real_logger"):
            self.testdir.runpytest(*pytest_args, **kwargs)
            self.allure_report = AllureReport(self.testdir.path)
        else:
            with fake_logger() as logger:
                self.allure_report = logger
                self.testdir.runpytest(*pytest_args, **kwargs)

        return self.allure_report

    def __get_example_path(self):
        return self.request.config.rootdir.join(
            (
                self.request.node.function.__doc__ or
                    self.request.node.module.__doc__
            ).strip()
        )


class AllureIntegrationRunner:
    def __init__(self, module: str, entry_point :str = "main") -> None:
        self.__module_name = module
        self.__entry_point = entry_point

    def run_allure_integration(self, *args, **kwargs):
        with fake_logger() as allure_results:
            module = runpy.run_module(self.__module_name)
            return_value = module[self.__entry_point](*args, **kwargs)
            return {
                "allure-results": allure_results,
                "return-value": return_value
            }


@pytest.fixture
def allured_testdir(
    pytester: Pytester,
    request: FixtureRequest
) -> AlluredTestdir:
    fixture = AlluredTestdir(pytester, request)
    return fixture


@pytest.fixture
def executed_docstring_source(
    allured_testdir: AlluredTestdir
) -> AlluredTestdir:
    allured_testdir.parse_docstring_source()
    allured_testdir.run_with_allure()
    return allured_testdir


@pytest.fixture
def executed_docstring_path(
    allured_testdir: AlluredTestdir
) -> AlluredTestdir:
    allured_testdir.parse_docstring_path()
    allured_testdir.run_with_allure()
    return allured_testdir


@pytest.fixture
def executed_docstring_directory(
    allured_testdir: AlluredTestdir
) -> AlluredTestdir:
    allured_testdir.copy_docstring_dir()
    allured_testdir.run_with_allure()
    return allured_testdir


@pytest.fixture
def rst_examples(request: FixtureRequest) -> RstExampleTable:
    return RstExampleTable.find_examples(request)