from functools import partial
from hamcrest import assert_that
from hamcrest import not_
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_step
from allure_commons_test.result import has_attachment
from allure_commons_test.result import has_parameter
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import has_link
from allure_commons_test.container import has_container
from allure_commons_test.container import has_before, has_after
from allure_commons_test.label import has_severity
from allure_commons_test.label import has_tag
from allure_commons_test.label import has_label


def match(matcher, *args):
    for i, arg in enumerate(args):
        if not hasattr(arg, '__call__'):
            matcher = partial(matcher, arg)
        else:
            matcher = partial(matcher, match(arg, *args[i+1:]))
            break
    return matcher()


@then(u'allure report has a scenario with name "{scenario}"')
def step_scenario(context, scenario):
    matcher = partial(match, has_test_case, scenario)
    context.scenario = matcher
    assert_that(context.allure_report, matcher())


@then(u'allure report has not a scenario with name "{scenario}"')
def step_scenario(context, scenario):
    matcher = partial(match, not_, has_test_case, scenario)
    context.scenario = matcher
    assert_that(context.allure_report, matcher())


@then(u'scenario has before fixture "{fixture}"')
@then(u'this scenario has before fixture "{fixture}"')
def step_before_fixture(context, fixture):
    context_matcher = context.scenario
    matcher = partial(context_matcher, has_container, context.allure_report, has_before, fixture)
    context.before = matcher
    assert_that(context.allure_report, matcher())


@then(u'scenario has after fixture "{fixture}"')
@then(u'this scenario has after fixture "{fixture}"')
def step_after_fixture(context, fixture):
    context_matcher = context.scenario
    matcher = partial(context_matcher, has_container, context.allure_report, has_after, fixture)
    context.after = matcher
    assert_that(context.allure_report, matcher())


@then(u'scenario has not before fixture "{fixture}"')
@then(u'this scenario has not before fixture "{fixture}"')
def step_no_before_fixture(context, fixture):
    context_matcher = context.scenario
    matcher = partial(context_matcher, not_, has_container, context.allure_report, has_before, fixture)
    assert_that(context.allure_report, matcher())


@then(u'scenario has not after fixture "{fixture}"')
@then(u'this scenario has not after fixture "{fixture}"')
def step_impl(context, fixture):
    context_matcher = context.scenario
    matcher = partial(context_matcher, not_, has_container, context.allure_report, has_after, fixture)
    assert_that(context.allure_report, matcher())


@then(u'{item} contains step "{step}"')
@then(u'this {item} contains step "{step}"')
def step_step(context, item, step):
    context_matcher = getattr(context, item)
    matcher = partial(context_matcher, has_step, step)
    context.step = matcher
    assert_that(context.allure_report, matcher())


@then(u'{item} has "{status}" status')
@then(u'this {item} has "{status}" status')
def step_status(context, item, status):
    context_matcher = getattr(context, item)
    matcher = partial(context_matcher, with_status, status)
    assert_that(context.allure_report, matcher())


@then(u'{item} has status details with message "{message}"')
@then(u'this {item} has status details with message "{message}"')
def step_status(context, item, message):
    context_matcher = getattr(context, item)
    matcher = partial(context_matcher, has_status_details, with_message_contains, message)
    assert_that(context.allure_report, matcher())


@then(u'scenario has "{severity}" severity')
@then(u'this scenario has "{severity}" severity')
def step_severity(context, severity):
    context_matcher = context.scenario
    matcher = partial(context_matcher, has_severity, severity)
    assert_that(context.allure_report, matcher())


@then(u'scenario has "{tag}" tag')
@then(u'this scenario has "{tag}" tag')
def step_tag(context, tag):
    context_matcher = context.scenario
    matcher = partial(context_matcher, has_tag, tag)
    assert_that(context.allure_report, matcher())


@then(u'scenario has "{url}" link')
@then(u'this scenario has "{url}" link')
@then(u'scenario has "{url}" link with type "{link_type}"')
@then(u'this scenario has "{url}" link with type "{link_type}"')
@then(u'scenario has "{url}" link with type "{link_type}" and name "{name}"')
@then(u'this scenario has "{url}" link with type "{link_type}" and name "{name}"')
def step_link(context, url, link_type=None, name=None,):
    context_matcher = context.scenario
    matcher = partial(context_matcher, has_link, url, link_type, name)
    assert_that(context.allure_report, matcher())


@then(u'scenario has "{name}" label with value "{value}"')
@then(u'this scenario has "{name}" label with value "{value}"')
def step_label(context, name, value):
    context_matcher = context.scenario
    matcher = partial(context_matcher, has_label, name, value)
    assert_that(context.allure_report, matcher())


@then(u'{item} has parameter "{name}" with value "{value}"')
@then(u'this {item} has parameter "{name}" with value "{value}"')
def step_parameter(context, item, name, value):
    context_matcher = getattr(context, item)
    matcher = partial(context_matcher, has_parameter, name, value)
    assert_that(context.allure_report, matcher())


@then(u'{item} has attachment')
@then(u'this {item} has attachment')
def step_attachment(context, item):
    context_matcher = getattr(context, item)
    matcher = partial(context_matcher, has_attachment)
    assert_that(context.allure_report, matcher())
