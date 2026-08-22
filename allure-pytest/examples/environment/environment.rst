Environment
-----------

Reports can display information about the environment the tests were executed in, such as the operating system, the
browser or the address of the test stand. It is shown on the report's overview page and is provided with invocation of
``allure.environment(*args, **kwargs)``.

Values may be passed as keyword arguments:

    >>> import allure

    >>> def test_environment_from_keywords():
    ...     allure.environment(browser="chrome", stand="staging")

A mapping may be passed instead, which allows keys that are not valid python identifiers:

    >>> def test_environment_from_mapping():
    ...     allure.environment({"os.name": "Windows 11", "browser version": "125.0"})

Both forms may be combined in a single call:

    >>> def test_environment_from_mapping_and_keywords():
    ...     allure.environment({"python.version": "3.13.0"}, stand="production")

Values from all the calls made during the test run are merged together, so the environment may be filled in from
different places, for example, from a session-scoped fixture:

    >>> import pytest

    >>> @pytest.fixture(scope="session")
    ... def host_name():
    ...     allure.environment(hostname="my.host.local")
    ...     return "my.host.local"

    >>> def test_environment_from_fixture(host_name):
    ...     pass

A key set more than once keeps the value of the latest call.

The data is stored in the ``environment.properties`` file in the allure results directory. Note that the calls are only
recorded once the allure results directory is set up, i.e., starting from the ``pytest_sessionstart`` hook.
