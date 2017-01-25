import pytest
import os
import subprocess
import shlex
import json
from inspect import getmembers, isfunction


class AllureReport(object):
    def __init__(self, report):
        self._report = report
        self.report_dir = report.strpath
        self.test_cases = self._read_item('*testcase.json')
        self.test_groups = self._read_item('*testgroup.json')

    def _read_item(self, glob):
        ret = list()
        for local_path in self._report.listdir(glob):
            with open(local_path.strpath) as json_file:
                item = json.load(json_file)
                ret.append(item)
        return ret


@pytest.fixture(scope='function', autouse=True)
def inject_matchers(doctest_namespace):
    import hamcrest
    for name, function in getmembers(hamcrest, isfunction):
            doctest_namespace[name] = function

    from test.matchers import fixture, group, item, label, report
    for module in [fixture, group, item, label, report]:
        for name, function in getmembers(module, isfunction):
            doctest_namespace[name] = function


@pytest.fixture(scope='module')
def allure_report(request, tmpdir_factory):
    module = request.module.__file__
    tmpdir = tmpdir_factory.mktemp('data')
    FNULL = open(os.devnull, 'w')
    subprocess.call(shlex.split('pytest --alluredir=%s %s' % (tmpdir.strpath, module)), stdout=FNULL, stderr=FNULL)
    return AllureReport(tmpdir)


def pytest_collection_modifyitems(items, config):
    if config.option.doctestmodules:
        items[:] = [item for item in items if item.__class__.__name__ == 'DoctestItem']


def pytest_configure(config):
    config.pluginmanager.register(Dummy())


class Dummy(object):

    def step(*args, **kwargs):
        def dummy_step(*args, **kwargs):
            pass
        return dummy_step

    @pytest.hookimpl()
    def pytest_namespace(self):
        return {'allure': self}
