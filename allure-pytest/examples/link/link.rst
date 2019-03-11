Links
-----

    >>> import allure

    >>> @allure.link("http://qameta.io")
    >>> def test_link():
    ...     pass


    >>> @allure.issue("https://github.com/allure-framework/allure-python/issues/24")
    ... def test_issue_link():
    ...    pass


    >>> @allure.testcase("issues/24#issuecomment-277330977")
    ... def test_testcase_link():
    ...     pass


    >>> @allure.link("http://qameta.io", name="QAMETA", link_type="homepage")
    ... def test_custom_link():
    ...     pass

