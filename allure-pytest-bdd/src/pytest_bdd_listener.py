import pytest

from allure_commons.utils import now
from allure_commons.model2 import Label
from allure_commons.model2 import Status
from allure_commons.types import LabelType, AttachmentType
from allure_commons.utils import platform_label
from allure_commons.utils import host_tag, thread_tag
from allure_commons.utils import md5

from .steps import get_step_uuid
from .steps import process_gherkin_step_args
from .steps import report_remaining_steps
from .steps import report_undefined_step
from .steps import start_gherkin_step
from .steps import stop_gherkin_step
from .storage import save_excinfo
from .storage import save_test_data
from .utils import attach_data
from .utils import get_allure_description
from .utils import get_allure_description_html
from .utils import get_allure_labels
from .utils import get_allure_links
from .utils import convert_params
from .utils import get_full_name
from .utils import get_title_path
from .utils import get_outline_params
from .utils import get_pytest_params
from .utils import get_pytest_report_status
from .utils import get_scenario_status_details
from .utils import get_test_name
from .utils import get_uuid
from .utils import post_process_test_result

from functools import partial


class PytestBDDListener:
    def __init__(self, lifecycle):
        self.lifecycle = lifecycle
        self.host = host_tag()
        self.thread = thread_tag()

    @pytest.hookimpl
    def pytest_bdd_before_scenario(self, request, feature, scenario):
        item = request.node
        uuid = get_uuid(item.nodeid)

        outline_params = get_outline_params(item)
        pytest_params = get_pytest_params(item)
        params = {**pytest_params, **outline_params}

        save_test_data(
            item=item,
            feature=feature,
            scenario=scenario,
            params=params,
        )

        full_name = get_full_name(feature, scenario)
        with self.lifecycle.schedule_test_case(uuid=uuid) as test_result:
            test_result.fullName = full_name
            test_result.titlePath = get_title_path(request, feature)
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

        finalizer = partial(report_remaining_steps, self.lifecycle, item)
        item.addfinalizer(finalizer)

    @pytest.hookimpl
    def pytest_bdd_after_scenario(self, request, feature, scenario):
        uuid = get_uuid(request.node.nodeid)
        with self.lifecycle.update_test_case(uuid=uuid) as test_result:
            test_result.stop = now()

    @pytest.hookimpl
    def pytest_bdd_before_step(self, request, feature, scenario, step, step_func):
        start_gherkin_step(self.lifecycle, request.node, step, step_func)

    @pytest.hookimpl
    def pytest_bdd_before_step_call(self, request, feature, scenario, step, step_func, step_func_args):
        process_gherkin_step_args(self.lifecycle, request.node, step, step_func, step_func_args)

    @pytest.hookimpl
    def pytest_bdd_after_step(self, request, feature, scenario, step, step_func, step_func_args):
        stop_gherkin_step(self.lifecycle, request.node, get_step_uuid(step))

    @pytest.hookimpl
    def pytest_bdd_step_error(self, request, feature, scenario, step, step_func, step_func_args, exception):
        stop_gherkin_step(self.lifecycle, request.node, get_step_uuid(step), exception=exception)

    @pytest.hookimpl
    def pytest_bdd_step_func_lookup_error(self, request, feature, scenario, step, exception):
        report_undefined_step(self.lifecycle, request.node, step, exception)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        report = (yield).get_result()

        excinfo = call.excinfo

        status = get_pytest_report_status(report, excinfo)
        status_details = get_scenario_status_details(report, excinfo)

        uuid = get_uuid(report.nodeid)
        with self.lifecycle.update_test_case(uuid=uuid) as test_result:

            if test_result and report.when == "setup":
                test_result.status = status
                test_result.statusDetails = status_details

            if report.when == "call" and test_result:

                # Save the exception to access it from the finalizer to report
                # the remaining steps
                save_excinfo(item, excinfo)

                if test_result.status is None or test_result.status == Status.PASSED:
                    test_result.status = status
                    test_result.statusDetails = status_details

            if report.when == "teardown" and test_result:
                if test_result.status == Status.PASSED and status in [Status.FAILED, Status.BROKEN]:
                    test_result.status = status
                    test_result.statusDetails = status_details
                if report.caplog:
                    attach_data(self.lifecycle, report.caplog, "log", AttachmentType.TEXT, None)
                if report.capstdout:
                    attach_data(self.lifecycle, report.capstdout, "stdout", AttachmentType.TEXT, None)
                if report.capstderr:
                    attach_data(self.lifecycle, report.capstderr, "stderr", AttachmentType.TEXT, None)
                post_process_test_result(item, test_result)

        if report.when == 'teardown':
            self.lifecycle.write_test_case(uuid=uuid)
