import pytest
from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_parameter


def params_name(request):
    node_id = request.node.nodeid
    _, name = node_id.rstrip("]").split("[")
    return name


@pytest.mark.parametrize("param", [True, False])
def test_parametrization(executed_docstring_source, param):
    """
    >>> import pytest

    >>> @pytest.mark.parametrize("param", [True, False])
    ... def test_parametrization_example(param):
    ...     assert param
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_parametrization_example[{param}]".format(param=param),
                              has_parameter("param", str(param))
                              )
                )


@pytest.mark.xfail()
@pytest.mark.parametrize("param", [True, False], ids=["pass", "fail"])
def test_parametrization_with_ids(executed_docstring_source, param):
    """
    >>> import pytest

    >>> @pytest.mark.parametrize("param", [True, False], ids=["pass", "fail"])
    ... def test_parametrization_with_ids_example(param):
    ...     assert param
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case(
                    "test_parametrization_with_ids_example[{param}]".format(param="pass" if param else "fail"),
                    has_parameter("pass" if param else "fail", str(param))
                )
                )


@pytest.mark.parametrize("param1", [True, False])
@pytest.mark.parametrize("param2", [True, True])
def test_parametrization_many_decorators(executed_docstring_source, request, param1, param2):
    """
    >>> import pytest

    >>> @pytest.mark.parametrize("param1", [True, False])
    ... @pytest.mark.parametrize("param2", [True, True])
    ... def test_parametrization_many_decorators_example(param1, param2):
    ...     pass
    """

    test_name = "test_parametrization_many_decorators_example[{params_name}]".format(params_name=params_name(request))

    assert_that(executed_docstring_source.allure_report,
                has_test_case(test_name,
                              has_parameter("param1", str(param1)),
                              has_parameter("param2", str(param2))

                              )
                )


@pytest.mark.xfail()
@pytest.mark.parametrize("param1", [True, False], ids=["pass", "fail"])
@pytest.mark.parametrize("param2", [True, True])
def test_parametrization_many_decorators_with_partial_ids(executed_docstring_source, request, param1, param2):
    """
    >>> import pytest

    >>> @pytest.mark.parametrize("param1", [True, False], ids=["first_pass", "first_fail"])
    ... @pytest.mark.parametrize("param2", [True, True])
    ... def test_parametrization_many_decorators_with_partial_ids_example(param1, param2):
    ...     pass
    """

    test_name = "test_parametrization_many_decorators_with_partial_ids_example[{params_name}]".format(
        params_name=params_name(request))

    assert_that(executed_docstring_source.allure_report,
                has_test_case(test_name,
                              has_parameter("pass" if param1 else "fail", str(param1)),
                              has_parameter("param2", str(param2))

                              )
                )
