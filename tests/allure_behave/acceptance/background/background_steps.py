from behave import given

@given("the first background step that is passed")
def the_first_background_step_that_is_passed(*args, **kwargs):
    pass


@given("the first background step that is failed")
def the_first_background_step_that_is_failed(*args, **kwargs):
    assert False, "Failed assertion message"


@given("the first background step that is broken")
def the_first_background_step_that_is_broken(*args, **kwargs):
    raise ValueError("Something is broken")


@given("the second background step with no failures")
@given("the first step with no failures")
@given("the second step with no failures")
@given("the step with no failures")
def the_step_with_no_failures(*args, **kwargs):
    pass
