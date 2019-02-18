Test severity
-------------

Nothing special here, just use ``allure.severity`` decorator

    >>> import allure


    >>> @allure.severity(allure.severity_level.MINOR)
    ... def test_severity():
    ...     pass

Allure supports next severity levels: ``TRIVIAL``, ``MINOR``, ``NORMAL``, ``CRITICAL`` , ``BLOCKER``.
By default, all tests marks with ``NORMAL`` severity.
