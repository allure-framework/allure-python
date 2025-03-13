import os
from uuid import UUID
from allure_commons.utils import md5
from allure_commons.model2 import StatusDetails
from allure_commons.model2 import Status
from allure_commons.model2 import Parameter
from allure_commons.utils import format_exception


ALLURE_DESCRIPTION_MARK = "allure_description"
ALLURE_DESCRIPTION_HTML_MARK = "allure_description_html"


def get_marker_value(item, keyword):
    marker = item.get_closest_marker(keyword)
    return marker.args[0] if marker and marker.args else None


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
