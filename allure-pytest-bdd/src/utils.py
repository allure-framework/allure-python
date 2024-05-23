import os
from uuid import UUID
from allure_commons.utils import md5
from allure_commons.model2 import StatusDetails
from allure_commons.model2 import Status
from allure_commons.model2 import Parameter
from allure_commons.utils import format_exception
from allure_commons.types import LabelType


ALLURE_DESCRIPTION_MARK = 'allure_description'
ALLURE_DESCRIPTION_HTML_MARK = 'allure_description_html'
ALLURE_LABEL_MARK = 'allure_label'
ALLURE_LINK_MARK = 'allure_link'
ALLURE_UNIQUE_LABELS = [
    LabelType.SEVERITY,
    LabelType.FRAMEWORK,
    LabelType.HOST,
    LabelType.SUITE,
    LabelType.PARENT_SUITE,
    LabelType.SUB_SUITE
]


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


def format_allure_link(config, url, link_type):
    pattern = dict(config.option.allure_link_pattern).get(link_type, '{}')
    return pattern.format(url)


def allure_labels(item):
    unique_labels = dict()
    labels = set()
    for mark in item.iter_markers(name=ALLURE_LABEL_MARK):
        label_type = mark.kwargs["label_type"]
        if label_type in ALLURE_UNIQUE_LABELS:
            if label_type not in unique_labels.keys():
                unique_labels[label_type] = mark.args[0]
        else:
            for arg in mark.args:
                labels.add((label_type, arg))
    for k, v in unique_labels.items():
        labels.add((k, v))
    return labels
