*** Settings ***
Library     ../run_robot_library.py
Library     ../test_allure_library.py
Suite Setup  Run exampe


*** Keywords ***
Run exampe
    ${example_file}     Get Example File
    ${allure_report}   Run Robot With Allure   ${example_file}
    Set Suite Variable	${report}   ${allure_report}


*** Test Cases ***
Single Line Description
    ${test_case}     Should Has Test Case   ${report}   Single Line Description
    Should Has Description    ${test_case}    Single line description

Multi Line Description
    ${test_case}     Should Has Test Case   ${report}   Multi Line Description
    Should Has Description    ${test_case}    Multi line\n description

Dynamic Description
    ${test_case}     Should Has Test Case   ${report}   Dynamic Description
    Should Has Description    ${test_case}    Dynamic description

Append Dynamic Description
    ${test_case}     Should Has Test Case   ${report}   Append Dynamic Description
    Should Has Description    ${test_case}    Static description Dynamic description