Test manual label
-------------

By default, ``ALLURE_MANUAL`` label is not set.

Usage of ``allure.manual`` decorator with out arguments (``True`` by default)

    >>> import allure


    >>> @allure.manual()
    ... def test_manual():
    ...     pass


``False`` can be set just in case.

    >>> @allure.manual(False)
    ... def test_manual_false():
    ...     pass