# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from enum import Enum
from behave.runner_util import make_undefined_step_snippet
from allure_commons.types import Severity
from allure_commons.model2 import Status, Parameter
from allure_commons.model2 import StatusDetails
from allure_commons.utils import md5
from allure_commons.utils import format_exception, format_traceback

STATUS = {
    'passed': Status.PASSED,
    'failed': Status.FAILED,
    'skipped': Status.SKIPPED,
    'untested': Status.SKIPPED,
    'undefined': Status.BROKEN
}


def scenario_name(scenario):
    return scenario.name if scenario.name else scenario.keyword


def scenario_history_id(scenario):
    parts = [scenario.feature.name, scenario.name]
    if scenario._row:
        row = scenario._row
        parts.extend(['{name}={value}'.format(name=name, value=value) for name, value in zip(row.headings, row.cells)])
    return md5(*parts)


def scenario_parameters(scenario):
    row = scenario._row
    return [Parameter(name=name, value=value) for name, value in zip(row.headings, row.cells)] if row else None


def scenario_severity(scenario):
    tags = scenario.feature.tags + scenario.tags
    severities = list(filter(lambda tag: tag in [severity.value for severity in Severity], tags))
    return Severity(severities[-1]) if severities else Severity.NORMAL


def scenario_tags(scenario):
    tags = scenario.feature.tags + scenario.tags
    tags = list(filter(lambda tag: tag not in [severity.value for severity in Severity], tags))
    return set(tags) if tags else []


def scenario_status(scenario):
    for step in scenario.all_steps:
        if step_status(step) != 'passed':
            return step_status(step)
    return Status.PASSED


def scenario_status_details(scenario):
    for step in scenario.all_steps:
        if step_status(step) != 'passed':
            return step_status_details(step)


def get_status_details(exc_type, exception, exc_traceback):
    if exception:
        return StatusDetails(message=format_exception(exc_type, exception),
                             trace=format_traceback(exc_traceback))


def step_status(result):
    if result.exception:
        return get_status(result.exception)
    else:
        if isinstance(result.status, Enum):
            return STATUS.get(result.status.name, None)
        else:
            return STATUS.get(result.status, None)


def get_status(exception):
    if exception and isinstance(exception, AssertionError):
        return Status.FAILED
    elif exception:
        return Status.BROKEN
    return Status.PASSED


def step_status_details(result):
    if result.exception:
        # workaround for https://github.com/behave/behave/pull/616
        trace = result.exc_traceback if type(result.exc_traceback) == list else format_traceback(result.exc_traceback)
        return StatusDetails(message=format_exception(type(result.exception), result.exception), trace=trace)

    elif result.status == 'undefined':
        message = '\nYou can implement step definitions for undefined steps with these snippets:\n\n'
        message += make_undefined_step_snippet(result)
        return StatusDetails(message=message)


def step_table(step):
    table = [','.join(step.table.headings)]
    [table.append(','.join(list(row))) for row in step.table.rows]
    return '\n'.join(table)
