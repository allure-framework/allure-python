from behave import given

@given("the first background step that is passed")
def step_impl(_):
    pass

@given("the first background step that is failed")
def step_impl(_):
    assert False, "Failed assertion message"

@given("the first background step that is broken")
def step_impl(_):
    raise ValueError("Something is broken")

@given("the second background step with no failures")
@given("the first step with no failures")
@given("the second step with no failures")
@given("the step with no failures")
def step_impl(_):
    pass
