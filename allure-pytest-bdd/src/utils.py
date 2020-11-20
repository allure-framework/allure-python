import os
from uuid import UUID
from allure_commons.utils import md5
from allure_commons.utils import represent
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

def get_step_name(node, step):
    name = "{step_keyword} {step_name}".format(step_keyword=step.keyword, step_name=step.name)
    if hasattr(node, 'callspec'):
        for key, value in node.callspec.params.items():
            name = name.replace(key, value)
    return name


def get_name(node, scenario):
    if hasattr(node, 'callspec'):
        parts = node.nodeid.rsplit("[")
        return "{name} [{params}".format(name=scenario.name, params=parts[-1])
    return scenario.name
from allure_commons.model2 import StatusDetails
from allure_commons.model2 import Status
from allure_commons.model2 import Parameter
from allure_commons.utils import format_exception


def get_step_name(node, step):
    name = "{step_keyword} {step_name}".format(step_keyword=step.keyword, step_name=step.name)
    if hasattr(node, 'callspec'):
        for key, value in node.callspec.params.items():
            name = name.replace("<{key}>".format(key=key), "<{{{key}}}>".format(key=key))
            name = name.format(**node.callspec.params)
    return name


def get_name(node, scenario):
    if hasattr(node, 'callspec'):
        parts = node.nodeid.rsplit("[")
        return "{name} [{params}".format(name=scenario.name, params=parts[-1])
    return scenario.name


def get_full_name(feature, scenario):
    feature_path = os.path.normpath(feature.rel_filename)
    return "{feature}:{scenario}".format(feature=feature_path, scenario=scenario.name)


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
        params = node.callspec.params
        return [Parameter(name=name, value=value) for name, value in params.items()]


def get_marker_value(item, keyword):
    marker = item.get_closest_marker(keyword)
    return marker.args[0] if marker and marker.args else None


def allure_description(item):
    description = get_marker_value(item, ALLURE_DESCRIPTION_MARK)
    if description:
        return description
    elif hasattr(item, 'function'):
        return item.function.__doc__


def pytest_markers(item):
    for keyword in item.keywords.keys():
        if any([keyword.startswith('allure_'), keyword == 'parametrize']):
            continue
        marker = item.get_closest_marker(keyword)
        if marker is None:
            continue

        yield mark_to_str(marker)


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


def allure_links(item):
    for mark in item.iter_markers(name=ALLURE_LINK_MARK):
        yield (mark.kwargs["link_type"], mark.args[0], mark.kwargs["name"])

def get_tags_from_environment_vars(env_vars_list):
    tags = set()
    for var_name in env_vars_list.split(','):
        tags.add(f"{var_name}: {os.environ.get(var_name)}")
    return tags
