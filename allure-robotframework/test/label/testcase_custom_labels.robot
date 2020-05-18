*** Settings ***
Library     ../run_robot_library.py
Library     ../test_allure_library.py


*** Test Case ***
Run Without options
    ${allure_report}   Run Robot With Allure   examples/label/testcase_custom_labels.rst
    ${test_case}     Should Has Test Case   ${allure_report}   Test Case With Custom Labels
    Should Has Label  ${test_case}  layer    UI
    Should Has Label  ${test_case}  stand    Alpha
    Should Has Label  ${test_case}  stand    Beta
