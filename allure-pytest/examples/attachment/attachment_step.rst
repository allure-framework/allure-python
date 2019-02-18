Attachment in step
------------------

Attachment usage for steps make your test more clear.

    >>> import pytest
    >>> import allure

    >>> @allure.step
    ... def step_with_attachment():
    ...     allure.attach("hello there")

    >>> def test_step_with_attachment():
    ...     step_with_attachment()
