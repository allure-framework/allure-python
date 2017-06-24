from behave.model import ScenarioOutline
from behave.runner_util import make_undefined_step_snippet
from allure.types import Severity
from allure.model2 import Status, Parameter, Label
from allure.model2 import StatusDetails
from allure.utils import md5
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
    return current_scenario_outline.name if current_scenario_outline else scenario.name


def scenario_history_id(scenario):
    return md5(scenario.filename, scenario.name)


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


def background_status(scenario):
    for step in scenario.background_steps:
        if step.status != 'passed':
            return step_status(step)
    return Status.PASSED


def step_status(result):
    if result.exception and not isinstance(result.exception, AssertionError):
        return Status.BROKEN
    else:
        return STATUS.get(result.status, None)


def step_status_details(result):
    if result.exception:
        message = ','.join(map(str, result.exception.args))
        message = '{name}: {message}'.format(name=result.exception.__class__.__name__, message=message)
        trace = '\n'.join(traceback.format_tb(result.exc_traceback)) if result.exc_traceback else None
        return StatusDetails(message=message, trace=trace)
    elif result.status == 'undefined':
        message = u"\nYou can implement step definitions for undefined steps with "
        message += u"these snippets:\n\n"
        message += make_undefined_step_snippet(result)
        return StatusDetails(message=message)
