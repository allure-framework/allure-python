from . import init_step

init_step()

def test_pass_with_step_outside():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_pass_with_step_outside')
    ... )
    """
    assert True