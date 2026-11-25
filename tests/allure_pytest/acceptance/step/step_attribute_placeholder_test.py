"""
Regression tests for object attribute access in step title placeholders.

See https://github.com/allure-framework/allure-python/issues/896.
"""

from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step


def test_step_with_dataclass_attribute_placeholder(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure
    >>> from dataclasses import dataclass

    >>> @dataclass
    ... class Item:
    ...     name: str

    >>> @allure.step("Process item: {item.name}")
    ... def process(item):
    ...     pass

    >>> def test_dataclass_attribute_access():
    ...     process(Item(name="Widget"))
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_dataclass_attribute_access",
            has_step("Process item: 'Widget'"),
        ),
    )


def test_step_with_object_attribute_placeholder(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure

    >>> class Order:
    ...     def __init__(self, status):
    ...         self.status = status

    >>> @allure.step("Order is {order.status}")
    ... def check(order):
    ...     pass

    >>> def test_object_attribute_access():
    ...     check(Order("delivered"))
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_object_attribute_access",
            has_step("Order is 'delivered'"),
        ),
    )


def test_step_with_nested_attribute_placeholder(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure
    >>> from dataclasses import dataclass

    >>> @dataclass
    ... class Address:
    ...     city: str

    >>> @dataclass
    ... class User:
    ...     address: Address

    >>> @allure.step("User from {user.address.city}")
    ... def greet(user):
    ...     pass

    >>> def test_nested_attribute_access():
    ...     greet(User(address=Address(city="Brighton")))
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_nested_attribute_access",
            has_step("User from 'Brighton'"),
        ),
    )
