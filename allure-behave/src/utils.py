from behave.model import ScenarioOutline
from behave.runner_util import make_undefined_step_snippet
from allure_commons.types import Severity
from allure_commons.model2 import Status, Parameter, Label
from allure_commons.model2 import StatusDetails
from allure_commons.utils import md5
from allure_commons.utils import represent
import traceback

STATUS = {
    'passed': Status.PASSED,
    'failed': Status.FAILED,
    'skipped': Status.SKIPPED,
    'untested': Status.SKIPPED,
    'undefined': Status.BROKEN
}


def scenario_name(scenario):
    scenario_outlines = [so for so in scenario.feature if isinstance(so, ScenarioOutline)]
    current_scenario_outline = next(iter(filter(lambda so: scenario in so.scenarios, scenario_outlines)), None)
    if current_scenario_outline:
        return current_scenario_outline.name if current_scenario_outline.name else current_scenario_outline.keyword
    return scenario.name if scenario.name else scenario.keyword


def scenario_history_id(scenario):
    parts = [scenario.feature.name, scenario.name]
    if scenario._row:
        row = scenario._row
        parts.extend([u'{name}={value}'.format(name=name, value=value) for name, value in zip(row.headings, row.cells)])
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
        if step.status != 'passed':
            return step_status(step)
    return Status.PASSED


def scenario_status_details(scenario):
    for step in scenario.all_steps:
        if step.status != 'passed':
            return step_status_details(step)


def fixture_status(exception, exc_traceback):
    if exception:
        return Status.FAILED if isinstance(exception, AssertionError) else Status.BROKEN
    else:
        return Status.BROKEN if exc_traceback else Status.PASSED


def fixture_status_details(exception, exc_traceback):
    if exception:
        message = u','.join(map(str, exception.args))
        message = u'{name}: {message}'.format(name=exception.__class__.__name__, message=message)
        trace = u'\n'.join(traceback.format_tb(exc_traceback)) if exc_traceback else None
        return StatusDetails(message=message, trace=trace)
    return None


def step_status(result):
    if result.exception and not isinstance(result.exception, AssertionError):
        return Status.BROKEN
    else:
        return STATUS.get(result.status, None)


def step_status_details(result):
    if result.exception:
        message = u','.join(map(lambda s: u'%s' % s, result.exception.args))
        message = u'{name}: {message}'.format(name=result.exception.__class__.__name__, message=message)
        trace = u'\n'.join(traceback.format_tb(result.exc_traceback)) if result.exc_traceback else None
        return StatusDetails(message=message, trace=trace)
    elif result.status == 'undefined':
        message = u'\nYou can implement step definitions for undefined steps with these snippets:\n\n'
        message += make_undefined_step_snippet(result)
        return StatusDetails(message=message)


def step_table(step):
    table = [','.join(step.table.headings)]
    [table.append(','.join(list(row))) for row in step.table.rows]
    return '\n'.join(table)
