Dynamic links
-------------

    >>> import allure
    >>> import pytest


    >>> def test_dynamic_link():
    ...     allure.dynamic.issue("issues/24")


    >>> @pytest.mark.parametrize('link', ["issues/24", "issues/132"])
    ... def test_parametrize_dynamic_link(link):
    ...     allure.dynamic.issue(link)


    >>> @allure.issue("issues/24")
    ... @allure.issue("issues/132")
    ... def test_all_links_together():
    ...     allure.dynamic.link("allure", name="QAMETA", link_type="docs")
