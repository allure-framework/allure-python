from hamcrest import assert_that, all_of
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_parameter


def test_metafunc_param(allure_pytest_runner: AllurePytestRunner):
    """
    >>> def pytest_generate_tests(metafunc):
    ...     if "metafunc_param" in metafunc.fixturenames:
    ...         metafunc.parametrize("metafunc_param", [True, False])


    >>> def test_metafunc_param_example(metafunc_param):
    ...     assert metafunc_param
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        all_of(
            has_test_case(
                "test_metafunc_param_example[True]",
                has_parameter("metafunc_param", "True")
            ),
            has_test_case(
                "test_metafunc_param_example[False]",
                has_parameter("metafunc_param", "False")
            )
        )
    )


def test_metafunc_param_with_ids(allure_pytest_runner: AllurePytestRunner):
    """
    >>> def pytest_generate_tests(metafunc):
    ...     if "metafunc_param_with_ids" in metafunc.fixturenames:
    ...         metafunc.parametrize(
    ...             "metafunc_param_with_ids",
    ...             [True, False],
    ...             ids=["pass", "fail"]
    ...         )


    >>> def test_metafunc_param_with_ids_example(metafunc_param_with_ids):
    ...     assert metafunc_param_with_ids
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        all_of(
            has_test_case(
                "test_metafunc_param_with_ids_example[pass]",
                has_parameter("metafunc_param_with_ids", "True")
            ),
            has_test_case(
                "test_metafunc_param_with_ids_example[fail]",
                has_parameter("metafunc_param_with_ids", "False")
            )
        )
    )
