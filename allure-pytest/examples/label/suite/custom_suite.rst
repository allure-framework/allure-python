Custom suite
____________

Use the `@allure.parent_suite`, `@allure.suite`, or `@allure.sub_suite`
decorators to overwrite default suite labels:

    >>> import allure

    >>> class TestCustomSuites:
    ...     @allure.parent_suite("parent suite name")
    ...     @allure.suite("suite name")
    ...     @allure.sub_suite("sub suite name")
    ...     def test_custom_suites(self):
    ...         pass


Use the `allure.dynamic.parent_suite`, `allure.dynamic.suite`, or
`allure.dynamic.sub_suite` functions to overwrite default suite labels
dynamically:

    >>> import allure

    >>> class TestCustomDynamicSuites:
    ...     def test_custom_dynamic_suites(self):
    ...         allure.dynamic.parent_suite("parent suite name")
    ...         allure.dynamic.suite("suite name")
    ...         allure.dynamic.sub_suite("sub suite name")
