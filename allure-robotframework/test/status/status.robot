*** Settings ***
Library     ../run_robot_library.py
Library     ../test_allure_library.py


*** Test Case ***
Use Library Keyword With Allure Step
    ${example_file}     Get Example File
    ${allure_report}    Run Robot With Allure    ${example_file}
    ${test_case}    Should Has Test Case   ${allure_report}   Test Case With Failed Step With Message
    Should Has Status    ${test_case}    failed
    Should Has Status Detail With Message    ${test_case}    Failed Details
    ${step}    Should Has Step    ${test_case}   BuiltIn.Fail
    Should Has Status    ${step}    failed
    Should Has Status Detail With Message    ${step}    Failed Details