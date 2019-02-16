Custom label
____________

If you want mark test with custom labels, you need to use ``allure.label(label_type, *values)`` decorator.


For this test:

    >>> import allure

    >>> @allure.label("Application", "desktop", "mobile")
    ... def test_custom_label():
    ...     pass

allure will get two labels "desktop", "mobile" with "Application" type.

