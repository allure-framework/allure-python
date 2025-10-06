from behave import Given,When,Then
import allure

@Given("start test")
def step_impl(context, ):
    print("Start Test")

@When("we do something")
def step_impl(context, ):
    print("we do something")

@Then("compare the change")
def step_impl(context, ):
    print("compare the change")
