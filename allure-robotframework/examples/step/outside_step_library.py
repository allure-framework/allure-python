import allure


def keyword_with_allure_step():
    with allure.step("Passed Step Inside Keyword"):
        pass
