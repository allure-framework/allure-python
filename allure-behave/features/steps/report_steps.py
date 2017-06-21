from functools import partial
from hamcrest import assert_that
from allure_testing.report import has_test_case
from allure_testing.result import with_status
from allure_testing.result import has_step
from allure_testing.result import has_attachment
from allure_testing.result import has_parameter
from allure_testing.container import has_container
from allure_testing.container import has_before
from allure_testing.label import has_severity
from allure_testing.label import has_tag


def match(matcher, *args):
    for i, arg in enumerate(args):
        if not hasattr(arg, '__call__'):
            matcher = partial(matcher, arg)
        else:
            matcher = partial(matcher, match(arg, *args[i+1:]))
            break
    return matcher()


@then(u'allure report has a scenario with name "{scenario}"')
def step_impl(context, scenario):
    matcher = partial(match, has_test_case, scenario)
    context.scenario = matcher
    assert_that(context.allure_report, matcher())


@then(u'scenario has background "{background}"')
@then(u'this scenario has background "{background}"')
def step_impl(context, background):
    context_matcher = context.scenario
    matcher = partial(context_matcher, has_container, context.allure_report, has_before, background)
    context.background = matcher
    assert_that(context.allure_report, matcher())


@then(u'{item} contains step "{step}"')
@then(u'this {item} contains step "{step}"')
def step_impl(context, item, step):
    context_matcher = getattr(context, item)
    matcher = partial(context_matcher, has_step, step)
    context.step = matcher
    assert_that(context.allure_report, matcher())


@then(u'{item} has "{status}" status')
@then(u'this {item} has "{status}" status')
def step_impl(context, item, status):
    context_matcher = getattr(context, item)
    matcher = partial(context_matcher, with_status, status)
    assert_that(context.allure_report, matcher())


@then(u'scenario has "{severity}" severity')
@then(u'this scenario has "{severity}" severity')
def step_impl(context, severity):
    context_matcher = context.scenario
    matcher = partial(context_matcher, has_severity, severity)
    assert_that(context.allure_report, matcher())


@then(u'scenario has "{tag}" tag')
@then(u'this scenario has "{tag}" tag')
def step_impl(context, tag):
    context_matcher = context.scenario
    matcher = partial(context_matcher, has_tag, tag)
    assert_that(context.allure_report, matcher())


@then(u'{item} has parameter "{name}" with value "{value}"')
@then(u'this {item} has parameter "{name}" with value "{value}"')
def step_impl(context, item, name, value):
    context_matcher = getattr(context, item)
    matcher = partial(context_matcher, has_parameter, name, value)
    assert_that(context.allure_report, matcher())


@then(u'{item} has attachment')
@then(u'this {item} has attachment')
def step_impl(context, item):
    context_matcher = getattr(context, item)
    matcher = partial(context_matcher, has_attachment)
    assert_that(context.allure_report, matcher())








