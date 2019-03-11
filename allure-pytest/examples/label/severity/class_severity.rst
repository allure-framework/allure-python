Class level severity
--------------------

You can mark whole test class with allure severity decorator and remark some methods with another if you wish.
For example:

    >>> import allure


    >>> @allure.severity(allure.severity_level.TRIVIAL)
    ... class TestDecoratedClass(object):
    ...     def test_not_decorated_method(self):
    ...         pass
    ...
    ...     @allure.severity(allure.severity_level.MINOR)
    ...     def test_decorated_method(self):
    ...         pass

Also you can mark a class methods for redefine default severity:

    >>> class TestNotDecoratedSubClass(TestDecoratedClass):
    ...
    ...     def test_not_decorated_method(self):
    ...         pass
    ...
    ...     @allure.severity(allure.severity_level.CRITICAL)
    ...     def test_decorated_method(self):
    ...         pass
