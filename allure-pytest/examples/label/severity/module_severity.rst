Module severity
---------------

Allure uses pytest marks for marking tests in allure stuff. All features of pytest marking are applicable here.

Let's mark whole module with ``TRIVIAL`` severity:
    >>> import allure


    >>> pytestmark = allure.severity(allure.severity_level.TRIVIAL)

This test have the same as module severity level
    >>> def test_not_decorated_function():
    ...     pass

But for this one, severity overridden to ``MINOR`` level
    >>> @allure.severity(allure.severity_level.MINOR)
    ... def test_decorated_function():
    ...     pass

Test methods also inherit severity defined for module
    >>> class TestNotDecorated(object):
    ...     # will get TRIVIAL severity
    ...     def test_method_of_not_decorated_class(self):
    ...         pass

But you can redefine it for all class methods
    >>> @allure.severity(allure.severity_level.NORMAL)
    ... class TestDecorated(object):
    ...     # will have NORMAL severity in allure report
    ...     def test_method_of_decorated_class(self):
    ...         pass
