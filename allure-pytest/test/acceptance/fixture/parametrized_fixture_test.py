import pytest
from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.container import has_container
from allure_commons_test.container import has_before
from allure_commons_test.result import has_parameter


def params_name(request):
    node_id = request.node.nodeid
    _, name = node_id.rstrip("]").split("[")
    return name


@pytest.mark.parametrize("param", [True, False])
def test_function_scope_parametrized_fixture(param, executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.fixture(params=[True, False])
    ... def parametrized_fixture(request):
    ...     pass

    >>> def test_function_scope_parametrized_fixture_example(parametrized_fixture):
    ...     pass
    """
    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_function_scope_parametrized_fixture_example[{param}]".format(param=param),
                              has_parameter("parametrized_fixture", str(param)),
                              has_container(executed_docstring_source.allure_report,
                                            has_before("parametrized_fixture")
                                            )
                              )
                )


@pytest.mark.parametrize("param", [True, False], ids=["param_true", "param_false"])
def test_function_scope_parametrized_fixture_with_ids(param, executed_docstring_source, request):
    """
    >>> import pytest

    >>> @pytest.fixture(params=[True, False], ids=["param_true", "param_false"])
    ... def parametrized_fixture(request):
    ...     pass

    >>> def test_function_scope_parametrized_fixture_with_ids_example(parametrized_fixture):
    ...     pass
    """

    test_name = "test_function_scope_parametrized_fixture_with_ids_example[{params_name}]".format(
        params_name=params_name(request))

    assert_that(executed_docstring_source.allure_report,
                has_test_case(test_name,
                              has_parameter("parametrized_fixture", str(param)),
                              has_container(executed_docstring_source.allure_report,
                                            has_before("parametrized_fixture")
                                            )
                              )
                )
