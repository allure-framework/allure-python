Custom suite
____________


    >>> import allure

    >>> @allure.parent_suite("parent suite name")
    >>> @allure.suite("suite name")
    >>> @allure.sub_suite("sub suite name")
    ... def test_custom_suite():
    ...     pass


