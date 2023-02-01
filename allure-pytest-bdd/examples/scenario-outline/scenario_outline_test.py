from pytest_bdd import scenario, given, when, then
from pytest_bdd import parsers


@scenario("outline.feature", "Two examples with two parameters each")
def test_scenario_outline():
    pass


@given(parsers.parse("first step for {first} value"))
def given_first_step_for_first_value(first):
    pass


@when(parsers.parse("something is done with the value {second}"))
def when_something_is_done_with_the_value_second(second):
    pass


@then(parsers.parse("check postconditions using {first} and {second}"))
def then_check_postconditions_using_first_and_second(first, second):
    pass
