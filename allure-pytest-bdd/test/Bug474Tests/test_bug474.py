from pytest_bdd import scenario, given, when, then, parsers
import pytest
import allure

a = 0
b = 0


@given(parsers.parse("two numbers: {first}, {second}"))
def step_impl(first, second):
    global a, b
    a = first
    b = second


@pytest.fixture()
@when("addition it")
def addition():
    allure.attach('A text attachment in module scope fixture', 'blah blah blah', allure.attachment_type.TEXT)
    sum_ = a+b
    return sum_


@then("must be sum of it")
def check_sum(addition):
    assert a+b == addition


@scenario("bug474.feature", "My Scenario Test")
def test_my_scenario():
    pass
