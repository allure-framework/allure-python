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
from allure_commons_test.result import has_attachment
from allure_commons_test.label import has_severity
from allure_commons_test.label import has_tag
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
    return test_case_matcher


def should_has_description(allure_report, test_case_matcher, description):
    description_matcher = partial(test_case_matcher, has_description, description)
    assert_that(allure_report, description_matcher())
    return description_matcher


def should_has_tag(allure_report, test_case_matcher, tag):
    tag_matcher = partial(test_case_matcher, has_tag, tag)
    assert_that(allure_report, tag_matcher())
    return tag_matcher


def should_not_has_tag(allure_report, test_case_matcher, tag):
    tag_matcher = partial(test_case_matcher, not_, has_tag, tag)
    assert_that(allure_report, tag_matcher())


def should_has_status(allure_report, item_matcher, status):
    status_matcher = partial(item_matcher, with_status, status)
    assert_that(allure_report, status_matcher())


def should_has_severity(allure_report, test_case_matcher, severity):
    severity_matcher = partial(test_case_matcher, has_severity, severity)
    assert_that(allure_report, severity_matcher())


def should_not_has_severity(allure_report, test_case_matcher):
    severity_matcher = partial(test_case_matcher, not_, has_severity, anything)
    assert_that(allure_report, severity_matcher())


def should_has_step(allure_report, item_matcher, step):
    step_matcher = partial(item_matcher, has_step, step)
    assert_that(allure_report, step_matcher())
    return step_matcher


def should_not_has_step(allure_report, item_matcher, step):
    step_matcher = partial(item_matcher, not_, has_step, step)
    assert_that(allure_report, step_matcher())


def should_has_before_fixture(allure_report, test_case_matcher, fixture):
    fixture_matcher = partial(test_case_matcher, has_container, allure_report,  has_before, fixture)
    assert_that(allure_report, fixture_matcher())
    return fixture_matcher


def should_has_after_fixture(allure_report, test_case_matcher, fixture):
    fixture_matcher = partial(test_case_matcher, has_container, allure_report,  has_after, fixture)
    assert_that(allure_report, fixture_matcher())
    return fixture_matcher


def should_has_parameter(allure_report, item_matcher, name, value):
    matcher = partial(item_matcher, has_parameter, name, value)
    assert_that(allure_report, matcher())


def should_has_link(allure_report, test_case_matcher, link, link_type=None, link_name=None):
    matcher = partial(test_case_matcher, has_link, link, link_type, link_name)
    assert_that(allure_report, matcher())


def should_has_status_detail_with_message(allure_report, item_matcher, message):
    matcher = partial(item_matcher, has_status_details, with_message_contains, message)
    assert_that(allure_report, matcher())


def should_has_attachment(allure_report, item_matcher, attach_type=None, name=None):
    matcher = partial(item_matcher, has_attachment,  attach_type, name)
    assert_that(allure_report, matcher())
