import os
from uuid import UUID
from allure_commons.utils import md5
from allure_commons.model2 import StatusDetails
from allure_commons.model2 import Status
from allure_commons.model2 import Parameter
from allure_commons.utils import format_exception


def get_step_name(step):
    return f"{step.keyword} {step.name}"


def get_name(node, scenario):
    if hasattr(node, 'callspec'):
        parts = node.nodeid.rsplit("[")
        params = parts[-1]
        return f"{scenario.name} [{params}"
    return scenario.name


def get_full_name(feature, scenario):
    feature_path = os.path.normpath(feature.rel_filename)
    return f"{feature_path}:{scenario.name}"


def get_uuid(*args):
    return str(UUID(md5(*args)))


def get_status_details(exception):
    message = str(exception)
    trace = format_exception(type(exception), exception)
    return StatusDetails(message=message, trace=trace) if message or trace else None


def get_pytest_report_status(pytest_report):
    pytest_statuses = ('failed', 'passed', 'skipped')
    statuses = (Status.FAILED, Status.PASSED, Status.SKIPPED)
    for pytest_status, status in zip(pytest_statuses, statuses):
        if getattr(pytest_report, pytest_status):
            return status


def get_params(node):
    if hasattr(node, 'callspec'):
        params = dict(node.callspec.params)
        outline_params = params.pop('_pytest_bdd_example', {})
        params.update(outline_params)
        return [Parameter(name=name, value=value) for name, value in params.items()]
