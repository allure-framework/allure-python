import allure
import allure_commons

@allure.step("Step in {caller}")
def step(caller):
    pass


@allure_commons.fixture
def before_all(context):
    step("before_all")


@allure_commons.fixture
def after_all(context):
    step("after_all")
