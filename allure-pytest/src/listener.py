import pytest

from allure.utils import now
from allure.utils import md5
from allure.utils import uuid4
from allure.logger import AllureLogger
from allure.model2 import TestStepResult, TestResult, TestBeforeResult, TestAfterResult
from allure.model2 import TestResultContainer
from allure.model2 import StatusDetails
from allure.model2 import Parameter
from allure.model2 import Label, Link
from allure.model2 import Status

from allure_pytest.utils import allure_parameters
from allure_pytest.utils import allure_labels, allure_links
from allure_pytest.utils import allure_full_name, allure_package


class AllureListener(object):

    def __init__(self, config):
        self.config = config
        self.allure_logger = AllureLogger(config.option.allure_report_dir)
        self._cache = ItemCache()

    @pytest.hookimpl
    def pytest_allure_before_step(self, uuid, title, params):
        parameters = [Parameter(name=name, value=value) for name, value in params]
        step = TestStepResult(name=title, start=now(), parameters=parameters)
        self.allure_logger.start_step(None, uuid, step)

    @pytest.hookimpl
    def pytest_allure_after_step(self, uuid, exc_type, exc_val, exc_tb):
        status = Status.PASSED
        if exc_type is not None:
            if exc_type == pytest.skip.Exception:
                status = Status.SKIPPED
            else:
                status = Status.FAILED

        self.allure_logger.stop_step(uuid, stop=now(), status=status)

    @pytest.hookimpl
    def pytest_allure_before_finalizer(self, parent_uuid, uuid, name):
        after_fixture = TestAfterResult(name=name, start=now())
        self.allure_logger.start_after_fixture(parent_uuid, uuid, after_fixture)

    @pytest.hookimpl
    def pytest_allure_after_finalizer(self, uuid, exc_type, exc_val, exc_tb):
        self.allure_logger.stop_after_fixture(uuid, stop=now())

    @pytest.hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_runtest_protocol(self, item, nextitem):
        uuid = self._cache.set(item.nodeid)
        for fixturedef in _test_fixtures(item):
            group_uuid = self._cache.get(fixturedef)
            if not group_uuid:
                group_uuid = self._cache.set(fixturedef)
                group = TestResultContainer(uuid=group_uuid)
                self.allure_logger.start_group(group_uuid, group)
            self.allure_logger.update_group(group_uuid, children=uuid)

        test_case = TestResult(name=item.name, uuid=uuid)
        self.allure_logger.schedule_test(uuid, test_case)

        yield

        test_case.labels = [Label(name, value) for name, value in allure_labels(item)]
        test_case.links = [Link(link_type, url, name) for link_type, url, name in allure_links(item)]
        test_case.fullName = allure_full_name(item.nodeid)
        test_case.historyId = md5(test_case.fullName)
        test_case.labels.append(Label('package', allure_package(item.nodeid)))

        uuid = self._cache.pop(item.nodeid)
        self.allure_logger.close_test(uuid)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_call(self, item):
        uuid = self._cache.get(item.nodeid)
        self.allure_logger.update_test(uuid, start=now())
        yield
        self.allure_logger.update_test(uuid, stop=now())

    @pytest.hookimpl(hookwrapper=True)
    def pytest_fixture_setup(self, fixturedef, request):
        fixture_name = fixturedef.argname

        container_uuid = self._cache.get(fixturedef)

        if not container_uuid:
            container_uuid = self._cache.set(fixturedef)
            container = TestResultContainer(uuid=container_uuid)
            self.allure_logger.start_group(container_uuid, container)

        self.allure_logger.update_group(container_uuid, start=now())

        before_fixture_uuid = uuid4
        before_fixture = TestBeforeResult(name=fixture_name, start=now())
        self.allure_logger.start_before_fixture(container_uuid, before_fixture_uuid, before_fixture)

        parameters = allure_parameters(fixturedef, request)
        if parameters:
            test_uuid = self._cache.get(request._pyfuncitem.nodeid)
            parameters = Parameter(**parameters) if parameters else []
            self.allure_logger.update_test(test_uuid, parameters=parameters)

        yield

        self.allure_logger.stop_before_fixture(before_fixture_uuid, stop=now())

        for index, finalizer in enumerate(fixturedef._finalizer or ()):
            fixturedef._finalizer[index] = FinalizerSpy(container_uuid, fixturedef.argname, finalizer, self.config)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_fixture_post_finalizer(self, fixturedef):
        yield
        if hasattr(fixturedef, 'cached_result') and self._cache.get(fixturedef):
            container_uuid = self._cache.pop(fixturedef)
            self.allure_logger.stop_group(container_uuid, stop=now())

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        uuid = self._cache.set(item.nodeid)
        report = (yield).get_result()
        allure_item = self.allure_logger.get_item(uuid)
        status = allure_item.status or None
        status_details = None

        if call.excinfo and hasattr(call.excinfo.value, 'msg'):
            status_details = StatusDetails(message=call.excinfo.value.msg)
        elif hasattr(report, 'wasxfail'):
            status_details = StatusDetails(message=report.wasxfail)
        elif report.failed:
            status_details = StatusDetails(message=str(call.excinfo.exconly()), trace=str(report.longrepr))

        if report.when == 'setup':
            if report.passed:
                status = Status.PASSED
            if report.failed:
                status = Status.BROKEN
            if report.skipped:
                status = Status.SKIPPED

        if report.when == 'call':
            if report.passed and status == Status.PASSED:
                pass
            if report.failed:
                status = Status.FAILED
            if report.skipped:
                status = Status.SKIPPED

        if report.when == 'teardown':
            if report.failed and status == Status.PASSED:
                status = Status.BROKEN

        if status_details:
            self.allure_logger.update_test(uuid, status=status, statusDetails=status_details)
        else:
            self.allure_logger.update_test(uuid, status=status)

    @pytest.hookimpl
    def pytest_allure_attach_data(self, body, name, attachment_type, extension):
        self.allure_logger.attach_data(uuid4(), body, name=name, attachment_type=attachment_type, extension=extension)

    @pytest.hookimpl
    def pytest_allure_attach_file(self, source, name, attachment_type, extension):
        self.allure_logger.attach_file(uuid4(), source, name=name, attachment_type=attachment_type, extension=extension)


class FinalizerSpy(object):
    def __init__(self, parent_uuid, fixturename, finalizer, config):
        self._parent_uuid = parent_uuid
        self._config = config
        self._finalizer = finalizer
        self._uuid = uuid4()
        self._name = "{fixture}::{finalizer}".format(fixture=fixturename, finalizer=finalizer.__name__)

    def __call__(self, *args, **kwards):
        with self:
            return self._finalizer(*args, **kwards)

    def __enter__(self):
        self._config.hook.pytest_allure_before_finalizer(parent_uuid=self._parent_uuid,
                                                         uuid=self._uuid,
                                                         name=self._name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._config.hook.pytest_allure_after_finalizer(uuid=self._uuid,
                                                        exc_type=exc_type,
                                                        exc_val=exc_val,
                                                        exc_tb=exc_tb)


class ItemCache(object):

    def __init__(self):
        self._items = dict()

    def get(self, _id):
        return self._items.get(str(_id))

    def set(self, _id):
        return self._items.setdefault(str(_id), uuid4())

    def pop(self, _id):
        return self._items.pop(str(_id))


def _test_fixtures(item):
    fixturemanager = item.session._fixturemanager
    fixturedefs = []

    if hasattr(item, "fixturenames"):
        for name in item.fixturenames:
            fixturedef = fixturemanager.getfixturedefs(name, item.nodeid)
            if fixturedef:
                fixturedefs.append(fixturedef[-1])

    return fixturedefs
