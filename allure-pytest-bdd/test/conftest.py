import pytest
import mock
from contextlib import contextmanager
import allure_commons
from allure_commons_test.report import AllureReport
from allure_commons.logger import AllureFileLogger
from .pytest_bdd_steps import *  # noqa F401 F403
from .report_steps import * # noqa F401 F403


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

    def run_with_allure(self):
        logger = AllureFileLogger(self.testdir.tmpdir.strpath)
        with fake_logger("allure_pytest_bdd.plugin.AllureFileLogger", logger):
            a = self.testdir.runpytest("-s", "-v", "--alluredir", self.testdir.tmpdir)
            print(a.stdout.lines)
            print(a.stderr.lines)
            self.allure_report = AllureReport(self.testdir.tmpdir.strpath)


@pytest.fixture
def allured_testdir(testdir, request):
    return AlluredTestdir(testdir, request)
