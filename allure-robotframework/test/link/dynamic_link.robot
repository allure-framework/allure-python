*** Settings ***
Library     ../run_robot_library.py
Library     ../test_allure_library.py
Suite Setup  Run test case with dynamic link


*** Keywords ***
Run test case with dynamic link
    ${allure_report}      Run Robot With Allure   examples/link/dynamic_link.rst
    ${test_case}          Should Has Test Case    ${allure_report}   Test Case With Dynamic Link
    Set Suite Variable    ${test_case}


*** Test Case ***
Test Case With Dynamic Links
    ${test case} Should Has issue To https://jira.com/browse/ISSUE-1 With Name ISSUE-1
    ${test case} Should Has test_case To https://testrail.com/browse/TEST-1 With Name TEST-1
    ${test case} Should Has link To https://homepage.com/ With Name homepage

*** Keywords ***
${test case} Should Has ${link type} To ${url} With Name ${name}
    Should Has Link  ${test_case}  ${url}  ${link type}  ${name}
