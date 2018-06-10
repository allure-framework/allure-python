import allure


@allure.step("First step")
def step_with_parameters(arg_param, kwarg_param=None):
    pass


def test_defined_default_parameter():
    """
    >>> from allure_commons.utils import represent
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_defined_default_parameter',
    ...                           has_step('First step',
    ...                                    has_parameter('arg_param', represent(1)),
    ...                                    has_parameter('kwarg_param', represent(2)),
    ...                            )
    ...             )
    ... )
    """
    step_with_parameters(1, kwarg_param=2)


def test_not_defined_default_parameter():
    """
    >>> from allure_commons.utils import represent
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_not_defined_default_parameter',
    ...                           has_step('First step',
    ...                                    has_parameter('arg_param', represent(1)),
    ...                                    has_parameter('kwarg_param', represent(None)),
    ...                            )
    ...             )
    ... )
    """
    step_with_parameters(1)


def test_default_parameter_in_args():
    """
    >>> from allure_commons.utils import represent
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_default_parameter_in_args',
    ...                           has_step('First step',
    ...                                    has_parameter('arg_param', represent(1)),
    ...                                    has_parameter('kwarg_param', represent(2)),
    ...                            )
    ...             )
    ... )
    """
    step_with_parameters(1, 2)
