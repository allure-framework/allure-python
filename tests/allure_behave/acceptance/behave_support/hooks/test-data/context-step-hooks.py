import allure
import allure_commons

@allure_commons.fixture
def before_scenario(context, scenario):
    with allure.step("Step in before_scenario"):
        pass

@allure_commons.fixture
def after_scenario(context, scenario):
    with allure.step("Step in after_scenario"):
        pass
