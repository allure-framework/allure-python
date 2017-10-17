import pytest
import os
import subprocess
import shlex
from inspect import getmembers, isfunction
from allure_commons_test.report import AllureReport
from allure_commons.utils import thread_tag


@pytest.fixture(scope='function', autouse=True)
def inject_matchers(doctest_namespace):
    import hamcrest
    for name, function in getmembers(hamcrest, isfunction):
            doctest_namespace[name] = function

    from allure_commons_test import container, label, report, result
    for module in [container, label, report, result]:
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
        key = '{thread}{module}{param}'.format(thread=thread_tag(), module=module, param=''.join(params))
        if not request.config.cache.get(key, False):
            _runner(tmpdir.strpath, module, *params)
            request.config.cache.set(key, True)

            def clear_cache():
                request.config.cache.set(key, False)
            request.addfinalizer(clear_cache)

        return AllureReport(tmpdir.strpath)
    return run_with_params


@pytest.fixture(scope='module')
def allure_report(request, tmpdir_factory):
    module = request.module.__file__
    tmpdir = tmpdir_factory.mktemp('data')
    _runner(tmpdir.strpath, module)
    return AllureReport(tmpdir.strpath)


def pytest_collection_modifyitems(items, config):
    if config.option.doctestmodules:
        items[:] = [item for item in items if item.__class__.__name__ == 'DoctestItem']