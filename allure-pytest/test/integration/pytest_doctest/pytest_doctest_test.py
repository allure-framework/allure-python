import allure
from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status


@allure.feature("Integration")
def test_pytest_doctest(allured_testdir):
    allured_testdir.testdir.makepyfile('''
        def some_func():
            """
            >>> some_func()
            True
            """
            return True

    ''')

    allured_testdir.run_with_allure("--doctest-modules")

    assert_that(allured_testdir.allure_report,
                has_test_case("test_pytest_doctest.some_func",
                              with_status("passed"))
                )

@allure.feature("Integration")
def test_pytest_doctest_failed(allured_testdir):
    allured_testdir.testdir.makepyfile('''
        def some_func():
            """
            >>> some_func()
            True
            """
            return not True

    ''')

    allured_testdir.run_with_allure("--doctest-modules")

    assert_that(
        allured_testdir.allure_report,
        has_test_case(
            "test_pytest_doctest_failed.some_func",
            with_status("failed")
        )
    )

@allure.feature("Integration")
def test_pytest_doctest_broken(allured_testdir):
    allured_testdir.testdir.makepyfile('''
        def some_func():
            """
            >>> raise ValueError()
            """
    ''')

    allured_testdir.run_with_allure("--doctest-modules")

    assert_that(
        allured_testdir.allure_report,
        has_test_case(
            "test_pytest_doctest_broken.some_func",
            with_status("broken")
        )
    )