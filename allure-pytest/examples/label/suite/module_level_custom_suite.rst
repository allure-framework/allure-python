Module level custom suite
-------------------------

    >>> import allure

    >>> pytestmark = allure.suite("module level suite name")


    >>> def test_module_level_custom_suite():
    ...     pass