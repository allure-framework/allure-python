# -*- coding: utf-8 -*-


def test_utf_func_déjà_vu():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_utf_func_déjà_vu')
    ... )
    """
    assert False


class TestScenario:

    def test_utf_method_例子(self):
        """
        >>> allure_report = getfixture('allure_report')
        >>> assert_that(allure_report,
        ...             has_test_case('test_utf_method_例子')
        ... )
        """
        pass
