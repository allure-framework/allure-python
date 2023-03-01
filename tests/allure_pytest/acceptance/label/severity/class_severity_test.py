"""./allure-pytest/examples/label/severity/class_severity.rst"""

from hamcrest import assert_that, all_of, is_not
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_severity


def test_decorated_class_not_decorated_method(
    allure_pytest_runner: AllurePytestRunner
):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "TestDecoratedClass#test_not_decorated_method",
            has_severity("trivial")
        )
    )


def test_decorated_class_decorated_method(
    allure_pytest_runner: AllurePytestRunner
):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "TestDecoratedClass#test_decorated_method",
            all_of(
                has_severity("minor"),
                is_not(has_severity("trivial"))
            )
        )
    )


def test_not_decorated_sub_class_not_decorated_method(
    allure_pytest_runner: AllurePytestRunner
):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "TestNotDecoratedSubClass#test_not_decorated_method",
            has_severity("trivial")
        )
    )


def test_not_decorated_sub_class_decorated_method(
    allure_pytest_runner: AllurePytestRunner
):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "TestNotDecoratedSubClass#test_decorated_method",
            all_of(
                has_severity("critical"),
                is_not(
                    has_severity("trivial")
                )
            )
        )
    )
