import csv
import io
from enum import Enum
from behave.runner_util import make_undefined_step_snippet
from allure_commons.types import Severity, LabelType
from allure_commons.model2 import Status, Parameter
from allure_commons.model2 import Link, Label
from allure_commons.model2 import StatusDetails
from allure_commons.utils import md5
from allure_commons.utils import format_exception, format_traceback
from allure_commons.mapping import parse_tag, labels_set

TEST_PLAN_SKIP_REASON = "Not in allure test plan"

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
        parts.extend([f'{name}={value}' for name, value in zip(row.headings, row.cells)])
    return md5(*parts)


def scenario_parameters(scenario):
    row = scenario._row
    return [Parameter(name=name, value=value) for name, value in zip(row.headings, row.cells)] if row else None


def scenario_links(scenario, issue_pattern, link_pattern):
    tags = scenario.feature.tags + scenario.tags
    parsed = [
        parse_tag(item, issue_pattern=issue_pattern, link_pattern=link_pattern)
        for item in tags
    ]
    return filter(lambda x: isinstance(x, Link), parsed)


def scenario_labels(scenario):
    tags = scenario.feature.tags + scenario.tags
    default_labels = [Label(name=LabelType.SEVERITY, value=Severity.NORMAL)]
    parsed = [parse_tag(item) for item in tags]
    return labels_set(list(filter(lambda x: isinstance(x, Label), default_labels + parsed)))


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


def get_fullname(scenario):
    name_with_param = scenario_name(scenario)
    name = name_with_param.rsplit(" -- ")[0]
    return f"{scenario.feature.name}: {name}"


def get_hook_name(name, parameters):
    tag = None
    if name in ["before_tag", "after_tag"]:
        param_list = list(parameters.items())
        if len(param_list) > 1:
            tag = param_list[1][1]
        else:
            tag = param_list[0][1][1]
    name = name.replace("_", " ")
    if tag:
        tag = tag.replace("'", "")
        name = f"{name} @{tag}"
    return name


def step_status_details(result):
    if result.exception:
        # workaround for https://github.com/behave/behave/pull/616
        trace = "\n".join(result.exc_traceback) if isinstance(
            result.exc_traceback,
            list
        ) else format_traceback(result.exc_traceback)
        return StatusDetails(
            message=format_exception(
                type(result.exception),
                result.exception
            ),
            trace=trace
        )

    elif result.status == 'undefined':
        message = '\nYou can implement step definitions for undefined steps with these snippets:\n\n'
        message += make_undefined_step_snippet(result)
        return StatusDetails(message=message)


def step_table(step):
    with io.StringIO() as buffer:
        writer = csv.writer(buffer)
        writer.writerow(step.table.headings)
        writer.writerows(r.cells for r in step.table.rows)
        return buffer.getvalue()


def is_planned_scenario(scenario, test_plan):
    if test_plan:
        fullname = get_fullname(scenario)
        labels = scenario_labels(scenario)
        id_labels = list(filter(lambda label: label.name == LabelType.ID, labels))
        allure_id = id_labels[0].value if id_labels else None
        for item in test_plan:
            if (allure_id and allure_id == item.get("id")) or fullname == item.get("selector"):
                return
        scenario.skip(reason=TEST_PLAN_SKIP_REASON)
