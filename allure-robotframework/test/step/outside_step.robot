*** Settings ***
Library     ../run_robot_library.py
Library     ../test_allure_library.py


*** Test Case ***
Use Library Keyword With Allure Step
    ${example_file}     Get Example File
    ${allure_report}    Run Robot With Allure    ${example_file}
    ${test_case}    Should Has Test Case   ${allure_report}   Use Library Keyword With Allure Step
    ${step}  Should Has Step   ${test_case}   outside_step_library.Keyword With Allure Step
    Should Has Step     ${step}   Passed Step Inside Keyword