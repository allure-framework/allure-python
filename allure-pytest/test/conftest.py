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


def _runner(allure_dir, module, *extra_params):
    FNULL = open(os.devnull, 'w')
    extra_params = ' '.join(extra_params)
    cmd = shlex.split('pytest --alluredir=%s %s %s' % (allure_dir, extra_params, module))
    subprocess.call(cmd, stdout=FNULL, stderr=FNULL)


@pytest.fixture(scope='module')
def allure_report_with_params(request, tmpdir_factory):
    module = request.module.__file__
    tmpdir = tmpdir_factory.mktemp('data')

    def run_with_params(*params):
        key = '{module}{param}'.format(module=module, param=''.join(params))
        if not request.config.cache.get(key, False):
            _runner(tmpdir.strpath, module, *params)
            request.config.cache.set(key, True)

            def clear_cache():
                request.config.cache.set(key, False)
            request.addfinalizer(clear_cache)

        return AllureReport(tmpdir)
    return run_with_params


@pytest.fixture(scope='module')
def allure_report(request, tmpdir_factory):
    module = request.module.__file__
    tmpdir = tmpdir_factory.mktemp('data')
    _runner(tmpdir.strpath, module)
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
