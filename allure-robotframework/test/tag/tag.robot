*** Settings ***
Library     ../run_robot_library.py
Library     ../test_allure_library.py
Suite Setup  Run exampe


*** Keywords ***
Run exampe
    ${allure_report}   Run Robot With Allure   examples/tag/tag.rst
    Set Suite Variable	${report}   ${allure_report}


*** Test Case ***
Test Case With Tags
    ${test_case}     Should Has Test Case   ${report}   Test Case With Tags
    Should Has Tag  ${test_case}    alpha
    Should Has Tag  ${test_case}    bravo

Test Case With Dynamic Tags
    ${test_case}     Should Has Test Case   ${report}   Test Case With Dynamic Tags
    Should Has Tag  ${test_case}    alpha
    Should Has Tag  ${test_case}    bravo

Test Case With Removed Tags
    ${test_case}     Should Has Test Case   ${report}   Test Case With Removed Tags
    Should Has Tag  ${test_case}    alpha
    Should Has Tag  ${test_case}    charlie