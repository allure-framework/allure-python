import pytest
import logging


logger = logging.getLogger(__name__)
logger.info("Log outside test should not break, only be ignored")


@pytest.fixture
def fixture_with_log():
    logger.info("Log in fixture setup")
    yield
    logger.info("Log in fixture teardown")


def test_logs(fixture_with_log):
    """
    >>> from allure_commons.utils import represent
    >>> allure_report = getfixture('allure_report_with_params')('--log-cli-level=INFO')
    >>> assert_that(allure_report,
    ...             has_test_case('test_logs',
    ...                           has_step(contains_string('Log inside test')),
    ...                           has_container(allure_report,
    ...                                         has_before('fixture_with_log',
    ...                                                    has_step(contains_string('Log in fixture setup'))
    ...                                         ),
    ...                                         has_after('fixture_with_log::teardown',
    ...                                                   has_step(contains_string('Log in fixture teardown'))
    ...                                         )
    ...                           )
    ...             )
    ... )
    """
    logger.info("Log inside test")
