from pytest_bdd import scenario, given, when, then


@scenario("scenario.feature", "Simple passed example")
def test_scenario_passes():
    pass


@given("the preconditions are satisfied")
def given_the_preconditions_are_satisfied():
    pass


@when("the action is invoked")
def when_the_action_is_invoked():
    pass


@then("the postconditions are held")
def then_the_postconditions_are_held():
    pass
