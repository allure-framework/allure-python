import pytest
import mock
import shutil
import runpy
from doctest import script_from_examples
from contextlib import contextmanager
from typing import Sequence

import allure_commons
from allure_commons_test.report import AllureReport
from allure_commons.logger import AllureMemoryLogger

pytest_plugins = "pytester"


def pytest_configure(config: pytest.Config):
    config.addinivalue_line(
        "markers", "real_logger: mark test to run with a real allure logger"
    )


@contextmanager
def fake_logger():
    blocked_plugins = []
    for name, plugin in allure_commons.plugin_manager.list_name_plugin():
        allure_commons.plugin_manager.unregister(plugin=plugin, name=name)
        blocked_plugins.append(plugin)

    with mock.patch("allure_commons.logger.AllureFileLogger") as ReporterMock:
        ReporterMock.return_value = AllureMemoryLogger()
        yield ReporterMock.return_value

    for plugin in blocked_plugins:
        allure_commons.plugin_manager.register(plugin)


def get_path_from_docstring(request: pytest.FixtureRequest):
    return request.config.rootpath.joinpath(
        (
            request.node.function.__doc__ or
                request.node.module.__doc__
        ).strip()
    )

class AlluredTestdir:
    def __init__(self, pytester: pytest.Pytester, request: pytest.FixtureRequest):
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
def allured_testdir(pytester: pytest.Pytester, request: pytest.FixtureRequest):
    fixture = AlluredTestdir(pytester, request)
    return fixture


@pytest.fixture
def executed_docstring_source(allured_testdir: AlluredTestdir):
    allured_testdir.parse_docstring_source()
    allured_testdir.run_with_allure()
    return allured_testdir


@pytest.fixture
def executed_docstring_path(allured_testdir: AlluredTestdir):
    allured_testdir.parse_docstring_path()
    allured_testdir.run_with_allure()
    return allured_testdir


@pytest.fixture
def executed_docstring_directory(allured_testdir: AlluredTestdir):
    allured_testdir.copy_docstring_dir()
    allured_testdir.run_with_allure()
    return allured_testdir
