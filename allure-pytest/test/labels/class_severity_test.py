"""
>>> allure_report = getfixture('allure_report')
>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(2)),
...                 has_property('test_groups', has_length(0))
...             ))
"""


"""
>> assert_that(allure_report,
...             has_test_case('test_parent_class_severity_label',
...                 has_severity('trivial')
...             ))


>> assert_that(allure_report,
...             has_test_case('test_other_severity_in_child',
...                 has_severity('normal')
...             ))
"""

import pytest


@pytest.allure.severity(pytest.allure.severity_level.TRIVIAL)
class TestClass(object):

    def test_not_decorated_method(self):
        """
        >>> allure_report = getfixture('allure_report')
        >>> assert_that(allure_report,
        ...             has_test_case('test_not_decorated_method',
        ...                 has_severity('trivial')
        ...             ))
        ...
        """
        pass

    @pytest.allure.severity(pytest.allure.severity_level.MINOR)
    def test_decorated_method_in_decorated_class(self):
        """
        >>> allure_report = getfixture('allure_report')
        >>> assert_that(allure_report,
        ...             has_test_case('test_decorated_method_in_decorated_class',
        ...                 has_severity('minor')
        ...             ))
        """
        pass

# TODO it
"""
not today
class TestTestClass(TestClass):

    def test_parent_class_severity_label(self):
        pass

    @pytest.allure.severity(pytest.allure.severity_level.NORMAL)
    def test_other_severity_in_child(self):
        pass
"""
