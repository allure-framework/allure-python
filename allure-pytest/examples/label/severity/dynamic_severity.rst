Dynamic Severity
-------------

    >>> import allure
    >>> import pytest

    >>> def test_dynamic_severity():
    ...     # Some condition
    ...     if True:
    ...       allure.dynamic.severity(allure.severity_level.CRITICAL)