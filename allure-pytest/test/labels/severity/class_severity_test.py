"""
>>> allure_report = getfixture('allure_report')
>>> assert_that(allure_report,
...             all_of(
...                    has_property('test_cases', has_length(4)),
...                    has_property('test_groups', has_length(0))
...             )
... )  # doctest: +SKIP
"""


import allure


@allure.severity(allure.severity_level.TRIVIAL)
class TestDecoratedClass(object):

    def test_not_decorated_method(self):
        """
        >>> allure_report = getfixture('allure_report')
        >>> assert_that(allure_report,
        ...             has_test_case('TestDecoratedClass#test_not_decorated_method',
        ...                           has_severity('trivial')
        ...             )
        ... )
        """
        pass

    @allure.severity(allure.severity_level.MINOR)
    def test_decorated_method(self):
        """
        >>> allure_report = getfixture('allure_report')
        >>> assert_that(allure_report,
        ...             has_test_case('TestDecoratedClass#test_decorated_method',
        ...                           all_of(has_severity('minor'),
        ...                                  is_not(has_severity('trivial'))
        ...                           )
        ...             )
        ... )
        """
        pass


class TestNotDecoratedSubClass(TestDecoratedClass):

    def test_not_decorated_method(self):
        """
        >>> allure_report = getfixture('allure_report')
        >>> assert_that(allure_report,
        ...             has_test_case('TestNotDecoratedSubClass#test_not_decorated_method',
        ...                           has_severity('trivial')
        ...             )
        ... )
        """
        pass

    @allure.severity(allure.severity_level.CRITICAL)
    def test_decorated_method(self):
        """
        >>> allure_report = getfixture('allure_report')
        >>> assert_that(allure_report,
        ...             has_test_case('TestNotDecoratedSubClass#test_decorated_method',
        ...                           all_of(has_severity('critical'),
        ...                                  is_not(has_severity('trivial'))
        ...                           )
        ...             )
        ... )
        """
        pass
