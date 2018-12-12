from functools import partial
from hamcrest import assert_that
from hamcrest import not_, anything
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_description
from allure_commons_test.result import has_step
from allure_commons_test.result import with_status
from allure_commons_test.result import has_parameter
from allure_commons_test.result import has_link
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import with_trace_contains
from allure_commons_test.result import has_attachment
from allure_commons_test.label import has_severity
from allure_commons_test.label import has_tag
from allure_commons_test.label import has_label
from allure_commons_test.container import has_container
from allure_commons_test.container import has_before, has_after


def match(matcher, *args):
    for i, arg in enumerate(args):
        if not hasattr(arg, '__call__'):
            matcher = partial(matcher, arg)
        else:
            matcher = partial(matcher, match(arg, *args[i+1:]))
            break
    return matcher()


def should_has_test_case(allure_report, test_case):
    test_case_matcher = partial(match, has_test_case, test_case)
    assert_that(allure_report, test_case_matcher())
    return allure_report, test_case_matcher


def should_has_tag(context, tag):
    allure_report, test_case_matcher = context
    tag_matcher = partial(test_case_matcher, has_tag, tag)
    assert_that(allure_report, tag_matcher())


def should_not_has_tag(conetxt, tag):
    allure_report, test_case_matcher = conetxt
    tag_matcher = partial(test_case_matcher, not_, has_tag, tag)
    assert_that(allure_report, tag_matcher())


def should_has_severity(context, severity):
    allure_report, test_case_matcher = context
    severity_matcher = partial(test_case_matcher, has_severity, severity)
    assert_that(allure_report, severity_matcher())


def should_not_has_severity(context):
    allure_report, test_case_matcher = context
    severity_matcher = partial(test_case_matcher, not_, has_severity, anything)
    assert_that(allure_report, severity_matcher())


def should_has_step(context, step):
    allure_report, item_matcher = context
    step_matcher = partial(item_matcher, has_step, step)
    assert_that(allure_report, step_matcher())
    return allure_report, step_matcher


def should_not_has_step(context, step):
    allure_report, item_matcher = context
    step_matcher = partial(item_matcher, not_, has_step, step)
    assert_that(allure_report, step_matcher())


def should_has_attachment(context, attach_type=None, name=None):
    allure_report, item_matcher = context
    matcher = partial(item_matcher, has_attachment,  attach_type, name)
    assert_that(allure_report, matcher())


def should_has_description(context, description):
    allure_report, test_case_matcher = context
    description_matcher = partial(test_case_matcher, has_description, description)
    assert_that(allure_report, description_matcher())


def should_has_before_fixture(context, fixture):
    allure_report, test_case_matcher = context
    fixture_matcher = partial(test_case_matcher, has_container, allure_report,  has_before, fixture)
    assert_that(allure_report, fixture_matcher())
    return allure_report, fixture_matcher


def should_has_after_fixture(context, fixture):
    allure_report, test_case_matcher = context
    fixture_matcher = partial(test_case_matcher, has_container, allure_report,  has_after, fixture)
    assert_that(allure_report, fixture_matcher())
    return allure_report, fixture_matcher


def should_has_status(context, status):
    allure_report, item_matcher = context
    status_matcher = partial(item_matcher, with_status, status)
    assert_that(allure_report, status_matcher())


def should_has_parameter(context, name, value):
    allure_report, item_matcher = context
    matcher = partial(item_matcher, has_parameter, name, value)
    assert_that(allure_report, matcher())


def should_has_status_detail_with_message(conext, message):
    allure_report, item_matcher = conext
    matcher = partial(item_matcher, has_status_details, with_message_contains, message)
    assert_that(allure_report, matcher())


def should_has_status_detail_with_traceback(conext, traceback):
    allure_report, item_matcher = conext
    matcher = partial(item_matcher, has_status_details, with_trace_contains, traceback)
    assert_that(allure_report, matcher())


def should_has_link(context, link, link_type=None, link_name=None):
    allure_report, test_case_matcher = context
    matcher = partial(test_case_matcher, has_link, link, link_type, link_name)
    assert_that(allure_report, matcher())


def should_has_label(context, name, value):
    allure_report, test_case_matcher = context
    matcher = partial(test_case_matcher, has_label, name, value)
    assert_that(allure_report, matcher())
