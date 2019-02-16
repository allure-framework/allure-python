Description
-----------

You can add a detailed description for tests to provide as much context to the report reader as you want. This can be
done in several ways: you can add a @allure.description decorator providing a description string or you can use
``@allure.description_html`` to provide some HTML to be rendered in the 'Description' section of a test case.

    >>> import allure

    >>> @allure.description("""Test description""")
    ... def test_description():
    ...     pass


    >>> @allure.description_html("""<h1>Html test description</h1>""")
    ... def test_description_html():
    ...     pass


Alternatively description will be simply picked up from the docstring of a test method.

    >>> def test_docstring_description():
    ...     """ Docstring """


    >>> def test_unicode_docstring_description():
    ...     """ Докстринг в юникоде """
