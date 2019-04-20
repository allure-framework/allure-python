*** Settings ***
Library     ../run_robot_library.py
Library     ../test_allure_library.py
Suite Setup  Run example


*** Keywords ***
Run example
    ${allure_report}   Run Robot With Allure   examples/link/link.rst
    Set Suite Variable	${report}   ${allure_report}


*** Test Case ***
Test Case With Issue Link Without URL
    ${test_case}     Should Has Test Case   ${report}   Test Case With Issue Link Without URL
    Should Has Link  ${test_case}  ISSUE-1  issue

Test Case With Issue Link With URL
    ${test_case}     Should Has Test Case   ${report}   Test Case With Issue Link With URL
    Should Has Link  ${test_case}  https://jira.com/browse/ISSUE-1  issue

Test Case With TMS Link Without URL
    ${test_case}     Should Has Test Case   ${report}   Test Case With TMS Link Without URL
    Should Has Link  ${test_case}  TEST-1  test_case

Test Case With TMS Link With URL
    ${test_case}     Should Has Test Case   ${report}   Test Case With TMS Link With URL
    Should Has Link  ${test_case}  https://testrail.com/browse/TEST-1  test_case

Test Case With Unlabeled Link
    ${test_case}     Should Has Test Case   ${report}   Test Case With Unlabeled Link
    Should Has Link  ${test_case}  https://homepage.com/  link

Test Case With Labeled Link
    ${test_case}     Should Has Test Case   ${report}   Test Case With Labeled Link
    Should Has Link  ${test_case}  https://homepage.com/  link  Home Page

