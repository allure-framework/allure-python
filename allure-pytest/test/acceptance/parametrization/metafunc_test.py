import pytest
from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_parameter


@pytest.mark.parametrize("param", [True, False])
def test_metafunc_param(executed_docstring_source, param):
    """
    >>> def pytest_generate_tests(metafunc):
    ...     if "metafunc_param" in metafunc.fixturenames:
    ...         metafunc.parametrize("metafunc_param", [True, False])


    >>> def test_metafunc_param_example(metafunc_param):
    ...     assert metafunc_param
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_metafunc_param_example[{param}]".format(param=param),
                              has_parameter("metafunc_param", str(param))
                              )
                )


@pytest.mark.parametrize("param", [True, False])
def test_metafunc_param_with_ids(executed_docstring_source, param):
    """
    >>> def pytest_generate_tests(metafunc):
    ...     if "metafunc_param_with_ids" in metafunc.fixturenames:
    ...         metafunc.parametrize("metafunc_param_with_ids", [True, False], ids=["pass", "fail"])


    >>> def test_metafunc_param_with_ids_example(metafunc_param_with_ids):
    ...     assert metafunc_param_with_ids
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_metafunc_param_with_ids_example[{param}]".format(param="pass" if param else "fail"),
                              has_parameter("metafunc_param_with_ids", str(param))
                              )
                )
