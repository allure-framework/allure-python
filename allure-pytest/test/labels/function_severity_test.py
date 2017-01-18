import pytest


@pytest.allure.severity(pytest.allure.severity_level.MINOR)
def test_minor():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_minor',
    ...                 has_severity('minor')
    ...             ))

    """
    pass
