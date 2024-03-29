Test title
----------

Test titles can be made more readable with special @allure.title decorator.
Titles support placeholders for arguments.

    >>> import pytest
    >>> import allure


    >>> @allure.title("A some test title")
    ... def test_display_name():
    ...     pass


    >>> @allure.title("A some test title with param {param}")
    ... @pytest.mark.parametrize('param', [False])
    ... def test_display_name_template(param):
    ...     assert param

    >>> @allure.title("A test title with ParameterSet id {param_id}")
    ... @pytest.mark.parametrize('param', [False], ids=["some_id"])
    ... def test_display_name_parameter_set_id(param):
    ...     assert param
