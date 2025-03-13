import os
from uuid import UUID
from allure_commons.utils import md5
from allure_commons.utils import SafeFormatter
from allure_commons.model2 import StatusDetails
from allure_commons.model2 import Status
from allure_commons.model2 import Parameter
from allure_commons.utils import format_exception


ALLURE_DESCRIPTION_MARK = "allure_description"
ALLURE_DESCRIPTION_HTML_MARK = "allure_description_html"
ALLURE_TITLE_MARK = "allure_title"


def get_marker_value(item, keyword):
    marker = item.get_closest_marker(keyword)
    return marker.args[0] if marker and marker.args else None


def get_allure_title(item):
    return get_marker_value(item, ALLURE_TITLE_MARK)


def interpolate_args(format_str, args):
    return SafeFormatter().format(format_str, **args) if args else format_str


def get_allure_description(item, feature, scenario):
    value = get_marker_value(item, ALLURE_DESCRIPTION_MARK)
    if value:
        return value

    feature_description = resolve_description(feature.description)
    scenario_description = resolve_description(scenario.description)
    return "\n\n".join(filter(None, [feature_description, scenario_description]))


def get_allure_description_html(item):
    return get_marker_value(item, ALLURE_DESCRIPTION_HTML_MARK)


def resolve_description(description):
    if isinstance(description, str):
        return description

    if not isinstance(description, list):
        return None

    while description and description[0] == "":
        description = description[1:]
    while description and description[-1] == "":
        description = description[:-1]
    return "\n".join(description) or None


def get_step_name(step):
    return f"{step.keyword} {step.name}"


def get_test_name(node, scenario, params):
    allure_name = get_allure_title(node)
    if allure_name:
        return interpolate_args(allure_name, params)

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


def get_pytest_params(node):
    if hasattr(node, 'callspec'):
        pytest_params = dict(node.callspec.params)
        pytest_bdd_params = pytest_params.pop('_pytest_bdd_example', {})
        return {**pytest_bdd_params, **pytest_params}


def convert_params(pytest_params):
    return [
        Parameter(
            name=name,
            value=value,
        ) for name, value in (pytest_params or {}).items()
    ]
