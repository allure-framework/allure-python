import os
from uuid import UUID

from allure_commons.model2 import Parameter
from allure_commons.model2 import Status
from allure_commons.model2 import StatusDetails
from allure_commons.types import LabelType
from allure_commons.utils import format_exception
from allure_commons.utils import md5
from allure_commons.utils import represent

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


def get_marker_value(item, keyword):
    marker = item.get_closest_marker(keyword)
    return marker.args[0] if marker and marker.args else None


def allure_description(item):
    description = get_marker_value(item, ALLURE_DESCRIPTION_MARK)
    if description:
        return description
    elif hasattr(item, 'function'):
        return item.function.__doc__


def mark_to_str(marker):
    args = [represent(arg) for arg in marker.args]
    kwargs = ['{name}={value}'.format(name=key, value=represent(marker.kwargs[key])) for key in marker.kwargs]
    if marker.name in ('filterwarnings', 'skip', 'skipif', 'xfail', 'usefixtures', 'tryfirst', 'trylast'):
        markstr = '@pytest.mark.{name}'.format(name=marker.name)
    else:
        markstr = '{name}'.format(name=marker.name)
    if args or kwargs:
        parameters = ', '.join(args + kwargs)
        markstr = '{}({})'.format(markstr, parameters)
    return markstr


def pytest_markers(item):
    for keyword in item.keywords.keys():
        if any([keyword.startswith('allure_'), keyword == 'parametrize']):
            continue
        marker = item.get_closest_marker(keyword)
        if marker is None:
            continue

        yield mark_to_str(marker)


def allure_links(item):
    for mark in item.iter_markers(name=ALLURE_LINK_MARK):
        yield mark.kwargs["link_type"], mark.args[0], mark.kwargs["name"]
