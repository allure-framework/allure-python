*** Settings ***
Library     ../run_robot_library.py
Library     ../test_allure_library.py


*** Test Case ***
Use Library Keyword With Allure Step
    ${allure_report}    Run Robot With Allure    examples/step/outside_step.rst
    ${test_case}    Should Has Test Case   ${allure_report}   Use Library Keyword With Allure Step
    ${step}  Should Has Step   ${test_case}   outside_step_library.Keyword With Allure Step
    Should Has Step     ${step}   Passed Step Inside Keyword