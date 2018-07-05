# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import six
import pytest
from allure_commons.utils import represent
from allure_commons.utils import format_exception, format_traceback, escape_non_unicode_symbols
from allure_commons.model2 import Status
from allure_commons.model2 import StatusDetails

ALLURE_TITLE = 'allure_title'
ALLURE_DESCRIPTION = 'allure_description'
ALLURE_DESCRIPTION_HTML = 'allure_description_html'
ALLURE_LABEL_PREFIX = 'allure_label'
ALLURE_LINK_PREFIX = 'allure_link'
ALLURE_UNIQUE_LABELS = ['severity', 'thread', 'host']


def get_marker_value(item, keyword):
    marker = item.keywords.get(keyword)
    return marker.args[0] if marker and marker.args else None


def allure_title(item):
    return get_marker_value(item, ALLURE_TITLE)


def allure_description(item):
    description = get_marker_value(item, ALLURE_DESCRIPTION)
    if description:
        return description
    elif hasattr(item, 'function'):
        return item.function.__doc__


def allure_description_html(item):
    return get_marker_value(item, ALLURE_DESCRIPTION_HTML)


def allure_labels(item):
    for keyword in item.keywords.keys():
        if keyword.startswith(ALLURE_LABEL_PREFIX):
            marker = item.get_marker(keyword)
            label_type = marker.kwargs['label_type']
            if label_type in ALLURE_UNIQUE_LABELS:
                yield (label_type, marker.args[0])
            else:
                for value in marker.args:
                    yield (label_type, value)


def allure_links(item):
    for keyword in item.keywords.keys():
        if keyword.startswith(ALLURE_LINK_PREFIX):
            marker = item.get_marker(keyword)
            link_type = marker.kwargs['link_type']
            url = marker.args[0]
            name = marker.kwargs['name']
            yield (link_type, url, name)


def pytest_markers(item):
    for keyword in item.keywords.keys():
        if not any((keyword.startswith('allure_'),
                    keyword == 'parametrize')):
            marker = item.get_marker(keyword)
            if marker:
                yield mark_to_str(marker)


def mark_to_str(marker):
    args = [represent(arg) for arg in marker.args]
    kwargs = ['{name}={value}'.format(name=key, value=represent(marker.kwargs[key])) for key in marker.kwargs]
    if args or kwargs:
        parameters = ', '.join(args + kwargs)
        return '@pytest.mark.{name}({parameters})'.format(name=marker.name, parameters=parameters)
    else:
        return '@pytest.mark.{name}'.format(name=marker.name)


def allure_package(item):
    parts = item.nodeid.split('::')
    path = parts[0].rsplit('.', 1)[0]
    return path.replace('/', '.')


def allure_name(item, parameters):
    name = escape_name(item.name)
    title = allure_title(item)
    return title.format(**parameters) if title else name


def allure_full_name(item):
    parts = item.nodeid.split('::')
    package = allure_package(item)
    clazz = '.{clazz}'.format(clazz=parts[1]) if len(parts) > 2 else ''
    test = parts[-1]
    full_name = '{package}{clazz}#{test}'.format(package=package, clazz=clazz, test=test)
    return escape_name(full_name)


def escape_name(name):
    if six.PY2:
        try:
            name.decode('string_escape').encode('unicode_escape')
        except UnicodeDecodeError:
            return name.decode('string_escape').decode('utf-8')
    return name.encode('ascii', 'backslashreplace').decode('unicode_escape')


def get_outcome_status(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    return get_status(exception)


def get_outcome_status_details(outcome):
    exception_type, exception, exception_traceback = outcome.excinfo or (None, None, None)
    return get_status_details(exception_type, exception, exception_traceback)


def get_status(exception):
    if exception:
        if isinstance(exception, AssertionError) or isinstance(exception, pytest.fail.Exception):
            return Status.FAILED
        elif isinstance(exception, pytest.skip.Exception):
            return Status.SKIPPED
        return Status.BROKEN
    else:
        return Status.PASSED


def get_status_details(exception_type, exception, exception_traceback):
    message = escape_non_unicode_symbols(format_exception(exception_type, exception))
    trace = escape_non_unicode_symbols(format_traceback(exception_traceback))
    return StatusDetails(message=message, trace=trace) if message or trace else None


def get_pytest_report_status(pytest_report):
    pytest_statuses = ('failed', 'passed', 'skipped')
    statuses = (Status.FAILED, Status.PASSED, Status.SKIPPED)
    for pytest_status, status in zip(pytest_statuses, statuses):
        if getattr(pytest_report, pytest_status):
            return status
