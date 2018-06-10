import allure

TEMPLATE = "{1} and {kwarg}"


class TestClass(object):

    @allure.step(title=TEMPLATE)
    def step_method(self, arg, kwarg=2):
        pass

    def test_step_method_placeholders(self):
        """
        >>> allure_report = getfixture('allure_report')
        >>> assert_that(allure_report,
        ...             has_test_case('test_step_method_placeholders',
        ...                           has_step(TEMPLATE.format("self", 1, kwarg=2))
        ...             )
        ... )
        """
        self.step_method(1)
