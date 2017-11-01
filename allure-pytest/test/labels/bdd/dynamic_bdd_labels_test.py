import allure
import pytest


@allure.feature('first feature')
def test_dynamic_feature():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_dynamic_feature',
    ...                           has_feature('first feature'),
    ...                           has_feature('second feature')
    ...             )
    ... )
    """
    allure.dynamic.feature('second feature')


@pytest.mark.parametrize('feature', ['first feature', 'second feature'])
def test_parametrized_dynamic_feature(feature):
    """
    >>> allure_report = getfixture('allure_report')
    >>> for feature in ['first feature', 'second feature']:
    ...     assert_that(allure_report,
    ...                 has_test_case('test_parametrized_dynamic_feature[{feature}]'.format(feature=feature),
    ...                               has_feature(feature)
    ...                 )
    ...     )
    """
    allure.dynamic.feature(feature)
