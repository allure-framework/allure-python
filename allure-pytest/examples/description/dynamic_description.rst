Dynamic description
-------------------

Also descriptions can be dynamically updated from within test body using allure.dynamic.description.


    >>> import allure

    >>> @allure.description("Initial description")
    ... def test_dynamic_description():
    ...     allure.dynamic.description("Actual description")

    >>> @allure.description_html("<h1>Initial HTML description</h1>")
    ... def test_dynamic_description_html():
    ...     allure.dynamic.description_html("<p>Actual HTML description</p>")
