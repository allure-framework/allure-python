BDD labels
----------

There are two decorators: @allure.feature and @allure.story to mark your tests according to Feature/Story breakdown
specific to your project

    >>> import allure


    >>> @allure.epic("My epic")
    ... @allure.feature("My feature")
    ... @allure.story("My story")
    ... def test_single_bdd_label():
    ...     pass


    >>> @allure.epic("My epic", "Another epic")
    ... @allure.feature("My feature", "Another feature", "One more feature")
    ... @allure.story("My story", "Alternative story")
    ... def test_multiple_bdd_label():
    ...     pass
