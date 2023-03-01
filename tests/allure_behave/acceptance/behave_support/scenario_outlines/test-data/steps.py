from behave import given

@given("a user {name} {surname}")
def step_impl(context, name, surname):
    pass
