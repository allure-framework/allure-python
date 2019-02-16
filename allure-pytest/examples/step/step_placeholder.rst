Step param placeholders in title
--------------------------------


    >>> import allure

    >>> @allure.step("Step with two args: {0} and {1}")
    ... def step_with_args_in_placeholder(first, second):
    ...     pass


    >>> def test_step_with_args_in_placeholder():
    ...     step_with_args_in_placeholder("first", "second")


    >>> @allure.step("Step with two kwargs: {first} and {second}")
    ... def step_with_kwargs_in_placeholder(first="first", second="second"):
    ...     pass


    >>> def test_step_with_kwargs_in_placeholder():
    ...     step_with_kwargs_in_placeholder(first="1")


    >>> class TestClass(object):
    ...     @allure.step("Class method step with {1} and {second}")
    ...     def class_method_step_with_placeholder(self, first, second="second"):
    ...         pass
    ...
    ...     def test_class_method_as_step(self):
    ...         self.class_method_step_with_placeholder("first")

