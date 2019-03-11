Select test by severity level
-----------------------------

By using ``--allure-severities`` commandline option with a list of comma-separated severity levels only tests with
corresponding severities will be run.


For example, if you want to run only test_vip run pytest with ``--allure-severities=critical`` option:

    >>> import allure

    >>> @allure.severity(allure.severity_level.CRITICAL)
    ... def test_vip():
    ...     pass

    >>> def test_with_default_severity():
    ...     """ by default severity level is NORMAL """
    ...     pass

    >>> @allure.severity(allure.severity_level.MINOR)
    ... def test_minor():
    ...     pass
