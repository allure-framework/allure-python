import csv
import io
import os
from urllib.parse import urlparse
from uuid import UUID
from pathlib import Path

import pytest

from allure_commons.model2 import Label
from allure_commons.model2 import Link
from allure_commons.model2 import StatusDetails
from allure_commons.model2 import Status
from allure_commons.model2 import Parameter
from allure_commons.types import LabelType
from allure_commons.types import LinkType

from allure_commons.utils import format_exception
from allure_commons.utils import format_traceback
from allure_commons.utils import md5
from allure_commons.utils import represent
from allure_commons.utils import SafeFormatter
from allure_commons.utils import uuid4

from .storage import get_test_data

ALLURE_TITLE_ATTR = "__allure_display_name__"
ALLURE_DESCRIPTION_MARK = "allure_description"
ALLURE_DESCRIPTION_HTML_MARK = "allure_description_html"
ALLURE_LABEL_MARK = 'allure_label'
ALLURE_LINK_MARK = 'allure_link'

MARK_NAMES_TO_IGNORE = {
    "usefixtures",
    "filterwarnings",
    "skip",
    "skipif",
    "xfail",
    "parametrize",
}


def get_allure_title_of_test(item, params):
    obj = getattr(item, "obj", None)
    if obj is not None:
        return get_allure_title(obj, params)


def get_allure_title(fn, kwargs):
    if fn is not None:
        title_format = getattr(fn, ALLURE_TITLE_ATTR, None)
        if title_format:
            return interpolate(title_format, kwargs)


def interpolate(format_str, kwargs):
    return SafeFormatter().format(format_str, **kwargs) if kwargs else format_str


def get_allure_description(item, feature, scenario):
    value = get_marker_value(item, ALLURE_DESCRIPTION_MARK)
    if value:
        return value

    feature_description = extract_description(feature)
    scenario_description = extract_description(scenario)
    return "\n\n".join(filter(None, [feature_description, scenario_description]))


def get_allure_description_html(item):
    return get_marker_value(item, ALLURE_DESCRIPTION_HTML_MARK)


def iter_all_labels(item):
    for mark in item.iter_markers(name=ALLURE_LABEL_MARK):
        name = mark.kwargs.get("label_type")
        if name:
            yield from ((name, value) for value in mark.args or [])


def iter_label_values(item, name):
    return (pair for pair in iter_all_labels(item) if pair[0] == name)


def convert_labels(labels):
    return [Label(name, value) for name, value in labels]


def get_allure_labels(item):
    return convert_labels(iter_all_labels(item))


def iter_all_links(item):
    for marker in item.iter_markers(name=ALLURE_LINK_MARK):
        url = marker.args[0] if marker and marker.args else None
        if url:
            yield url, marker.kwargs.get("name"), marker.kwargs.get("link_type")


def convert_links(links):
    return [Link(url=url, name=name, type=link_type) for url, name, link_type in links]


def get_allure_links(item):
    return convert_links(iter_all_links(item))


def get_link_patterns(config):
    patterns = {}
    for link_type, pattern in config.option.allure_link_pattern:
        patterns[link_type] = pattern
    return patterns


def is_url(maybeUrl):
    try:
        result = urlparse(maybeUrl)
    except AttributeError:
        return False

    return result and (
        getattr(result, "scheme", None) or getattr(result, "netloc", None)
    )


def apply_link_pattern(patterns, link_type, url):
    if is_url(url):
        return url

    pattern = patterns.get(link_type or LinkType.LINK)
    return url if pattern is None else pattern.format(url)


def get_marker_value(item, keyword):
    marker = item.get_closest_marker(keyword)
    return marker.args[0] if marker and marker.args else None


def should_convert_mark_to_tag(mark):
    return mark.name not in MARK_NAMES_TO_IGNORE and\
        not mark.args and not mark.kwargs


def iter_pytest_tags(item):
    for mark in item.iter_markers():
        if should_convert_mark_to_tag(mark):
            yield LabelType.TAG, mark.name


def extract_description(obj):
    description = getattr(obj, "description", None)

    if isinstance(description, str):
        return description

    if not isinstance(description, list):
        return None

    while description and description[0] == "":
        description = description[1:]
    while description and description[-1] == "":
        description = description[:-1]
    return "\n".join(description) or None


def get_test_name(node, scenario, params):
    return get_allure_title_of_test(node, params) or scenario.name


def get_full_name(feature, scenario):
    feature_path = os.path.normpath(feature.rel_filename)
    return f"{feature_path}:{scenario.name}"


def get_rootdir(request):
    config = request.config
    return getattr(config, "rootpath", None) or Path(config.rootdir)


def get_title_path(request, feature):
    parts = Path(feature.filename).relative_to(get_rootdir(request)).parts
    return [*parts[:-1], feature.name or parts[-1]]


def get_uuid(*args):
    return str(UUID(md5(*args)))


def get_status(exception):
    if exception:
        if isinstance(exception, (pytest.skip.Exception, pytest.xfail.Exception)):
            return Status.SKIPPED
        elif isinstance(exception, (AssertionError, pytest.fail.Exception)):
            return Status.FAILED
        return Status.BROKEN
    else:
        return Status.PASSED


def get_status_details(exception, exception_type=None, traceback=None):
    if exception_type is None and exception is not None:
        exception_type = type(exception)
    message = format_exception(exception_type, exception)
    trace = format_traceback(traceback or getattr(exception, "__traceback__", None))
    return StatusDetails(message=message, trace=trace) if message or trace else None


def get_pytest_report_status(pytest_report, excinfo):
    if pytest_report.failed:
        return get_status(excinfo.value) if excinfo else Status.BROKEN

    if pytest_report.passed:
        return Status.PASSED

    if pytest_report.skipped:
        return Status.SKIPPED


def is_runtime_xfail(excinfo):
    return isinstance(excinfo.value, pytest.xfail.Exception)


def get_scenario_status_details(report, excinfo):
    if excinfo:
        message = excinfo.exconly()
        trace = report.longreprtext
        if not is_runtime_xfail(excinfo) and hasattr(report, "wasxfail"):
            reason = report.wasxfail
            message = (f"XFAIL {reason}" if reason else "XFAIL") + "\n\n" + message
        return StatusDetails(message=message, trace=trace)
    elif report.passed and hasattr(report, "wasxfail"):
        reason = report.wasxfail
        return StatusDetails(message=f"XPASS {reason}" if reason else "XPASS")
    elif report.failed and "XPASS(strict)" in report.longrepr:
        return StatusDetails(message=report.longrepr)


def get_outline_params(node):
    if hasattr(node, 'callspec'):
        return node.callspec.params.get('_pytest_bdd_example', {})
    return {}


def get_pytest_params(node):
    if hasattr(node, 'callspec'):
        pytest_params = dict(node.callspec.params)
        if "_pytest_bdd_example" in pytest_params:
            del pytest_params["_pytest_bdd_example"]
        return pytest_params
    return {}


def convert_params(outline_params, pytest_params):
    return [
        *(Parameter(
            name=name,
            value=value,
        ) for name, value in outline_params.items()),
        *(Parameter(
            name=name,
            value=represent(value),
        ) for name, value in pytest_params.items() if name not in outline_params),
    ]


def iter_pytest_labels(item, test_result):
    test_data = get_test_data(item)

    existing_labels = {label.name for label in test_result.labels}

    if LabelType.FEATURE not in existing_labels:
        yield LabelType.FEATURE, test_data.feature.name

    yield from iter_pytest_tags(item)


def iter_default_labels(item, test_result):
    return (
        Label(
            name=name,
            value=value,
        ) for name, value in iter_pytest_labels(item, test_result)
    )


def get_history_id(test_case_id, parameters, pytest_params):
    parameters_part = md5(*(pytest_params.get(p.name, p.value) for p in sorted(
        filter(lambda p: not p.excluded, parameters),
        key=lambda p: p.name,
    )))
    return f"{test_case_id}.{parameters_part}"


def post_process_test_result(item, test_result):
    test_data = get_test_data(item)

    test_result.labels.extend(iter_default_labels(item, test_result))
    test_result.historyId = get_history_id(
        test_case_id=test_result.testCaseId,
        parameters=test_result.parameters,
        pytest_params=test_data.params,
    )


def attach_data(lifecycle, body, name, attachment_type, extension=None, parent_uuid=None):
    lifecycle.attach_data(
        uuid4(),
        body,
        name=name,
        attachment_type=attachment_type,
        extension=extension,
        parent_uuid=parent_uuid,
    )


def attach_file(lifecycle, source, name, attachment_type, extension=None):
    lifecycle.attach_file(
        uuid4(),
        source,
        name=name,
        attachment_type=attachment_type,
        extension=extension,
    )


def format_csv(rows):
    with io.StringIO() as buffer:
        writer = csv.writer(buffer)
        writer.writerow(rows[0])
        writer.writerows(rows[1:])
        return buffer.getvalue()
