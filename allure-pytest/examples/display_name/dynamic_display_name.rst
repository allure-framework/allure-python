Dynamic test title
------------------

    >>> import allure


    >>> @allure.title("A some test tile")
    >>> def test_dynamic_display_name():
    >>>     allure.dynamic.title("It is renamed test")
