*** Settings ***
Library     ../run_robot_library.py
Library     ../test_allure_library.py


*** Test Case ***
Run Without options
    ${allure_report}   Run Robot With Allure   examples/label
    ${test_case}     Should Has Test Case   ${allure_report}   Test Cases With BDD Labels
    Should Has Label  ${test_case}  epic    Tag
    Should Has Label  ${test_case}  feature    Label
    Should Has Label  ${test_case}  story    Test case BDD labels
