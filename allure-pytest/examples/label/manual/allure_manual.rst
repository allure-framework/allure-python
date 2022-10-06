Test manual label
-------------

By default, ``ALLURE_MANUAL`` label is not set.

Usage of ``allure.manual`` decorator.

    >>> import allure


    >>> @allure.manual
    ... def test_manual():
    ...     pass

    >>> def test_manual_dynamic():
    ...     allure.dynamic.manual()
