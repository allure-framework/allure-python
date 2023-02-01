import allure
from behave import given

@given("step that passes")
def given_step_that_passes(_):
    pass

@given("step which adds a dynamic description to the scenario")
def given_step_which_adds_a_dynamic_description_to_the_scenario(_):
    allure.dynamic.description(
        "This scenario has a description specified by a step definition"
    )