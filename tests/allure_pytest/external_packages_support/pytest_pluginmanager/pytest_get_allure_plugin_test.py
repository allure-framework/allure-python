import allure
from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status


@allure.feature("Integration")
def test_pytest_get_allure_listener_plugin(allured_testdir):
    allured_testdir.testdir.makepyfile("""
        def test_pytest_get_allure_listener_plugin(request):
            assert request.config.pluginmanager.get_plugin('allure_listener')
    """)

    allured_testdir.run_with_allure()

    assert_that(allured_testdir.allure_report,
                has_test_case("test_pytest_get_allure_listener_plugin",
                              with_status("passed"))
                )
