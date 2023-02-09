import allure_commons

@allure_commons.fixture
def before_all(context):
    pass

@allure_commons.fixture
def after_all(context):
    pass

@allure_commons.fixture
def before_feature(context, feature):
    pass

@allure_commons.fixture
def after_feature(context, feature):
    pass

@allure_commons.fixture
def before_scenario(context, scenario):
    pass

@allure_commons.fixture
def after_scenario(context, scenario):
    pass

@allure_commons.fixture
def before_step(context, step):
    pass

@allure_commons.fixture
def after_step(context, step):
    pass
