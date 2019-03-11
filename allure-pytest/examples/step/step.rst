Steps
-----


    >>> import allure


    >>> def test_inline_step():
    ...     with allure.step("inline step"):
    ...         pass


    >>> @allure.step
    ... def passed_step():
    ...     pass


    >>> def test_reusable_step():
    ...     passed_step()


    >>> def test_nested_steps():
    ...     with allure.step("grand parent step"):
    ...         with allure.step("parent step"):
    ...             passed_step()


    >>> class TestClass(object):
    ...     @allure.step("class method as step")
    ...     def class_method(self):
    ...         pass
    ...
    ...     def test_class_method_as_step(self):
    ...         self.class_method()

