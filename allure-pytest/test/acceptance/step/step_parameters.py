import pytest
from hamcrest import assert_that
from allure_commons.utils import represent
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step
from allure_commons_test.result import has_parameter


def params_name(request):
    node_id = request.node.nodeid
    _, name = node_id.rstrip("]").split("[")
    return name


@pytest.mark.parametrize(
    ["args", "kwargs"],
    [
        ([True], {"kwarg": False}),
        ([True], {"kwarg": False}),
        (["hi"], {"kwarg": None}),
        ([None], {"kwarg": 42})
    ]
)
def test_step_parameters(executed_docstring_source, request, args, kwargs):
    """
    >>> import pytest
    >>> import allure

    >>> @allure.step
    ... def step(arg, kwarg=None):
    ...     pass

    >>> @pytest.mark.parametrize(
    ...     ["args", "kwargs"],
    ...     [
    ...         ([True], {"kwarg": False}),
    ...         ([True], {"kwarg": False}),
    ...         (["hi"], {"kwarg": None}),
    ...         ([None], {"kwarg": 42})
    ...     ]
    ... )
    ... def test_args_less_than_placeholders_example(args, kwargs):
    ...     step(*args, **kwargs)
    """

    test_name = "test_args_less_than_placeholders_example[{params_name}]".format(
        params_name=params_name(request))

    assert_that(executed_docstring_source.allure_report,
                has_test_case(test_name,
                              has_step("step",
                                       *([has_parameter("arg", represent(arg)) for arg in args] +
                                         [has_parameter("kwarg", represent(kwarg)) for kwarg in kwargs.values()]
                                         )

                                       )
                              )
                )
