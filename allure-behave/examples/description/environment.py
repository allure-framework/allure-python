import allure

def before_scenario(_, scenario):
    if "before_scenario" in scenario.name:
        allure.dynamic.description(
            "This scenario has a description specified in before_scenario hook"
        )


def after_scenario(_, scenario):
    if "after_scenario" in scenario.name:
        allure.dynamic.description(
            "This scenario has a description specified in after_scenario hook"
        )
