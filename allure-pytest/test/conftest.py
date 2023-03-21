import pytest
import six
from allure_commons_test.report import AllureReport
from doctest import script_from_examples
import mock
import allure_commons
from contextlib import contextmanager
from allure_commons.logger import AllureMemoryLogger


@contextmanager
def fake_logger(path, logger):
    blocked_plugins = []
    for name, plugin in allure_commons.plugin_manager.list_name_plugin():
        allure_commons.plugin_manager.unregister(plugin=plugin, name=name)
        blocked_plugins.append(plugin)

    with mock.patch(path) as ReporterMock:
        ReporterMock.return_value = logger
        yield

    for plugin in blocked_plugins:
        allure_commons.plugin_manager.register(plugin)


class AlluredTestdir(object):
    def __init__(self, testdir, request):
        self.testdir = testdir
        self.request = request
        self.allure_report = None

    def parse_docstring_source(self):
        docstring = self.request.node.function.__doc__ or self.request.node.module.__doc__
        source = script_from_examples(docstring).replace("#\n", "\n")
        if six.PY2:
            self.testdir.makepyfile("# -*- coding: utf-8 -*-\n%s" % source)
        else:
            self.testdir.makepyfile(source)

    def parse_docstring_path(self):
        doc_file = self.request.node.function.__doc__ or self.request.node.module.__doc__
        example_dir = self.request.config.rootdir.join(doc_file.strip())

        if six.PY2:
            with open(str(example_dir)) as f:
                content = "# -*- coding: utf-8 -*-\n%s" % f.read()
                source = script_from_examples(content)
                self.testdir.makepyfile(source)
        else:
            with open(example_dir, encoding="utf-8") as f:

                content = f.read()
                source = script_from_examples(content)
                self.testdir.makepyfile(source)

    def run_with_allure(self, *args, **kwargs):
        if self.request.node.get_closest_marker("real_logger"):
            self.testdir.runpytest("--alluredir", self.testdir.tmpdir, *args, **kwargs)
            self.allure_report = AllureReport(self.testdir.tmpdir.strpath)
        else:
            self.allure_report = AllureMemoryLogger()
            with fake_logger("allure_pytest.plugin.AllureFileLogger", self.allure_report):
                self.testdir.runpytest("--alluredir", self.testdir.tmpdir, *args, **kwargs)

        return self.allure_report


@pytest.fixture
def allured_testdir(testdir, request):
    return AlluredTestdir(testdir, request)


@pytest.fixture
def executed_docstring_source(allured_testdir):
    allured_testdir.parse_docstring_source()
    allured_testdir.run_with_allure()
    return allured_testdir


@pytest.fixture
def executed_docstring_path(allured_testdir):
    allured_testdir.parse_docstring_path()
    allured_testdir.run_with_allure()
    return allured_testdir
