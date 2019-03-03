from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_attachment


def test_attach_from_runtest_teardown(allured_testdir):
    allured_testdir.testdir.makeconftest("""
        import allure


        def pytest_runtest_teardown(*args, **kwargs):
            allure.attach(body="body", name="attachment from teardown")
    """)

    allured_testdir.testdir.makepyfile("""
        def test_attach_from_runtest_teardown():
            pass
    """)

    allured_testdir.run_with_allure()

    assert_that(allured_testdir.allure_report,
                has_test_case("test_attach_from_runtest_teardown",
                              has_attachment(name="attachment from teardown"),
                              )
                )


def test_attach_from_runtest_logfinish(allured_testdir):
    allured_testdir.testdir.makeconftest("""
        import allure


        def pytest_runtest_logfinish(*args, **kwargs):
            allure.attach(body="body", name="attachment from logfinish")
    """)

    allured_testdir.testdir.makepyfile("""
        def test_attach_from_runtest_logfinish():
            pass
    """)

    allured_testdir.run_with_allure()

    assert_that(allured_testdir.allure_report,
                has_test_case("test_attach_from_runtest_logfinish",
                              has_attachment(name="attachment from logfinish"),
                              )
                )
