import pytest

import allure_commons
from allure_commons.utils import now
from allure_commons.utils import uuid4
from allure_commons.model2 import Label
from allure_commons.model2 import Status
from allure_commons.model2 import StatusDetails
from allure_commons.types import LabelType, AttachmentType
from allure_commons.utils import platform_label
from allure_commons.utils import host_tag, thread_tag
from allure_commons.utils import md5

from .utils import save_test_data
from .utils import post_process_test_result
from .utils import get_uuid
from .utils import get_step_name
from .utils import get_status_details
from .utils import get_pytest_report_status
from .utils import get_full_name
from .utils import get_test_name
from .utils import get_outline_params
from .utils import get_pytest_params
from .utils import convert_params
from .utils import get_allure_labels
from .utils import get_allure_links
from .utils import get_allure_description
from .utils import get_allure_description_html

from functools import partial


class PytestBDDListener:
    def __init__(self, lifecycle):
        self.lifecycle = lifecycle
        self.host = host_tag()
        self.thread = thread_tag()

    def _scenario_finalizer(self, scenario):
        for step in scenario.steps:
            step_uuid = get_uuid(str(id(step)))
            with self.lifecycle.update_step(uuid=step_uuid) as step_result:
                if step_result:
                    step_result.status = Status.SKIPPED
                    self.lifecycle.stop_step(uuid=step_uuid)

    @pytest.hookimpl
    def pytest_bdd_before_scenario(self, request, feature, scenario):
        item = request.node
        uuid = get_uuid(item.nodeid)
        outline_params = get_outline_params(item)
        pytest_params = get_pytest_params(item)
        params = { **pytest_params, **outline_params }
        save_test_data(
            item=item,
            feature=feature,
            scenario=scenario,
            pytest_params=pytest_params,
        )

        full_name = get_full_name(feature, scenario)
        with self.lifecycle.schedule_test_case(uuid=uuid) as test_result:
            test_result.fullName = full_name
            test_result.name = get_test_name(item, scenario, params)
            test_result.description = get_allure_description(item, feature, scenario)
            test_result.descriptionHtml = get_allure_description_html(item)
            test_result.start = now()
            test_result.testCaseId = md5(full_name)
            test_result.labels.append(Label(name=LabelType.HOST, value=self.host))
            test_result.labels.append(Label(name=LabelType.THREAD, value=self.thread))
            test_result.labels.append(Label(name=LabelType.FRAMEWORK, value="pytest-bdd"))
            test_result.labels.append(Label(name=LabelType.LANGUAGE, value=platform_label()))
            test_result.labels.extend(get_allure_labels(item))
            test_result.links.extend(get_allure_links(item))
            test_result.parameters.extend(convert_params(outline_params, pytest_params))

        finalizer = partial(self._scenario_finalizer, scenario)
        item.addfinalizer(finalizer)

    @pytest.hookimpl
    def pytest_bdd_after_scenario(self, request, feature, scenario):
        uuid = get_uuid(request.node.nodeid)
        with self.lifecycle.update_test_case(uuid=uuid) as test_result:
            test_result.stop = now()

    @pytest.hookimpl
    def pytest_bdd_before_step(self, request, feature, scenario, step, step_func):
        parent_uuid = get_uuid(request.node.nodeid)
        uuid = get_uuid(str(id(step)))
        with self.lifecycle.start_step(parent_uuid=parent_uuid, uuid=uuid) as step_result:
            step_result.name = get_step_name(step)

    @pytest.hookimpl
    def pytest_bdd_after_step(self, request, feature, scenario, step, step_func, step_func_args):
        uuid = get_uuid(str(id(step)))
        with self.lifecycle.update_step(uuid=uuid) as step_result:
            step_result.status = Status.PASSED
        self.lifecycle.stop_step(uuid=uuid)

    @pytest.hookimpl
    def pytest_bdd_step_error(self, request, feature, scenario, step, step_func, step_func_args, exception):
        uuid = get_uuid(str(id(step)))
        with self.lifecycle.update_step(uuid=uuid) as step_result:
            step_result.status = Status.FAILED
            step_result.statusDetails = get_status_details(exception)
        self.lifecycle.stop_step(uuid=uuid)

    @pytest.hookimpl
    def pytest_bdd_step_func_lookup_error(self, request, feature, scenario, step, exception):
        uuid = get_uuid(str(id(step)))
        with self.lifecycle.update_step(uuid=uuid) as step_result:
            step_result.status = Status.BROKEN
        self.lifecycle.stop_step(uuid=uuid)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        report = (yield).get_result()

        status = get_pytest_report_status(report)

        status_details = StatusDetails(
            message=call.excinfo.exconly(),
            trace=report.longreprtext) if call.excinfo else None

        uuid = get_uuid(report.nodeid)
        with self.lifecycle.update_test_case(uuid=uuid) as test_result:

            if test_result and report.when == "setup":
                test_result.status = status
                test_result.statusDetails = status_details

            if report.when == "call" and test_result:
                if test_result.status not in [Status.PASSED, Status.FAILED]:
                    test_result.status = status
                    test_result.statusDetails = status_details

            if report.when == "teardown" and test_result:
                if test_result.status == Status.PASSED and status != Status.PASSED:
                    test_result.status = status
                    test_result.statusDetails = status_details
                if report.caplog:
                    self.attach_data(report.caplog, "log", AttachmentType.TEXT, None)
                if report.capstdout:
                    self.attach_data(report.capstdout, "stdout", AttachmentType.TEXT, None)
                if report.capstderr:
                    self.attach_data(report.capstderr, "stderr", AttachmentType.TEXT, None)
                post_process_test_result(item, test_result)

        if report.when == 'teardown':
            self.lifecycle.write_test_case(uuid=uuid)

    @allure_commons.hookimpl
    def attach_data(self, body, name, attachment_type, extension):
        self.lifecycle.attach_data(uuid4(), body, name=name, attachment_type=attachment_type, extension=extension)

    @allure_commons.hookimpl
    def attach_file(self, source, name, attachment_type, extension):
        self.lifecycle.attach_file(uuid4(), source, name=name, attachment_type=attachment_type, extension=extension)
