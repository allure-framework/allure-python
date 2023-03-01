from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

import allure
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status


@allure.feature("Integration")
def test_pytest_get_allure_listener_plugin(
    allure_pytest_runner: AllurePytestRunner
):
    """
    >>> def test_pytest_get_allure_listener_plugin(request):
    ...     assert request.config.pluginmanager.get_plugin('allure_listener')
    """

    output = allure_pytest_runner.run_docstring()

    assert_that(
        output,
        has_test_case(
            "test_pytest_get_allure_listener_plugin",
            with_status("passed")
        )
    )
