class TestSuiteClass(object):

    def test_default_suite_class_method(self):
        """
        >>> allure_report = getfixture('allure_report')
        >>> assert_that(allure_report,
        ...             has_test_case('test_default_suite_class_method',
        ...                           has_parent_suite('test.labels.suite'),
        ...                           has_suite('class_suite_test'),
        ...                           has_sub_suite('TestSuiteClass')
        ...             )
        ... )

        """
