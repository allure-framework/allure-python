Selecting tests by TAG label
----------------------------

You can use following commandline options to specify different sets of tests to execute passing a list of
values as compiled expression:

--allure-tags

There are some tests marked with TAG labels:

    >>> import allure

    >>> @allure.tag("some feature", "smoke")
    ... def test_feature_smoke():
    ...     pass

    >>> @allure.tag("some feature", "load")
    ... def test_feature_load():
    ...     pass


    >>> @pytest.mark.some_feature
    >>> @pytest.mark.e2e
    ... def test_feature_e2e():
    ...     pass


If you run ``pytest`` with following options: ``$ pytest tests.py --allure-tags="some_feature and (smoke or e2e)" --alluredir=./report`` first
and last tests will be runned.
All spaces in tags in the expression should be replaced with "_".
The function only works with statically assigned tags by @allure.tag marker.