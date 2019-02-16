import pytest

from attr import asdict
from allure_commons import hookimpl
import six


class AllureMemoryLogger(object):
    def __init__(self):
        self.test_cases = []
        self.test_containers = []
        self.attachments = {}

    @hookimpl
    def report_result(self, result):
        data = asdict(result, filter=lambda attr, value: not (type(value) != bool and not bool(value)))
        self.test_cases.append(data)

    @hookimpl
    def report_container(self, container):
        data = asdict(container, filter=lambda attr, value: not (type(value) != bool and not bool(value)))
        self.test_containers.append(data)

    @hookimpl
    def report_attached_file(self, source, file_name):
        pass

    @hookimpl
    def report_attached_data(self, body, file_name):
        self.attachments[file_name] = body


import mock
import allure_commons
from contextlib import contextmanager


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


from doctest import script_from_examples


class AlluredTestdir(object):
    def __init__(self, testdir):
        self.testdir = testdir
        self.allure_report = AllureMemoryLogger()

    def parse_docstring_source(self, request):
        docstring = request.node.function.__doc__ or request.node.module.__doc__
        source = script_from_examples(docstring).replace('#\n', '\n')
        if six.PY2:
            self.testdir.makepyfile("# -*- coding: utf-8 -*-\n%s" % source)
        else:
            self.testdir.makepyfile(source)

    def parse_docstring_path(self, request):
        doc_file = request.node.function.__doc__ or request.node.module.__doc__
        example_dir = request.config.rootdir.join(doc_file.strip())

        if six.PY2:
            with open(str(example_dir)) as f:
                content = "# -*- coding: utf-8 -*-\n%s" % f.read()
                source = script_from_examples(content)
                self.testdir.makepyfile(source)
        else:
            with open(example_dir, encoding='utf-8') as f:

                content = f.read()
                source = script_from_examples(content)
                self.testdir.makepyfile(source)

    def run_with_allure(self, *args, **kwargs):
        with fake_logger('allure_pytest.plugin.AllureFileLogger', self.allure_report):
            self.testdir.runpytest("--alluredir", self.testdir.tmpdir, *args, **kwargs)

        return self.allure_report


@pytest.fixture
def allured_testdir(testdir):
    return AlluredTestdir(testdir)


@pytest.fixture
def executed_docstring_source(allured_testdir, request):
    allured_testdir.parse_docstring_source(request)
    allured_testdir.run_with_allure()
    return allured_testdir


@pytest.fixture
def executed_docstring_path(allured_testdir, request):
    allured_testdir.parse_docstring_path(request)
    allured_testdir.run_with_allure()
    return allured_testdir
