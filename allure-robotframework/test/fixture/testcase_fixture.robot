*** Settings ***
Library     ../run_robot_library.py
Library     ../test_allure_library.py
Suite Setup  Run exampe


*** Keywords ***
Run exampe
    ${allure_report}   Run Robot With Allure   examples/fixture/testcase_fixture.rst
    Set Suite Variable	${report}   ${allure_report}


*** Test Cases ***
Test Case With Test Setup
    ${test_case}     Should Has Test Case   ${report}   Test Case With Test Setup
    ${fixture}  Should Has Before Fixture    ${test_case}    Passed Setup
    Should Has Step    ${fixture}   BuiltIn.No Operation

Test Case With Failed Test Setup
    ${test_case}     Should Has Test Case   ${report}   Test Case With Failed Test Setup
    Should Has Status    ${test_case}    failed
    ${fixture}  Should Has Before Fixture    ${test_case}    Failed Setup
    Should Has Status     ${fixture}    failed
    ${step}    Should Has Step    ${fixture}   BuiltIn.Fail
    Should Has Status    ${step}    failed

Test Case With Test Teardown
    ${test_case}     Should Has Test Case   ${report}   Test Case With Test Teardown
    ${fixture}  Should Has After Fixture    ${test_case}    Passed Teardown
    Should Has Step    ${fixture}   BuiltIn.No Operation

Test Case With Failed Test Teardown
    ${test_case}     Should Has Test Case   ${report}   Test Case With Failed Test Teardown
    Should Has Status    ${test_case}    failed
    ${fixture}  Should Has After Fixture    ${test_case}    Failed Teardown
    Should Has Status     ${fixture}    failed
    ${step}    Should Has Step    ${fixture}   BuiltIn.Fail
    Should Has Status    ${step}    failed

Test Case With Test Setup And Teardown
    ${test_case}     Should Has Test Case   ${report}   Test Case With Test Setup And Teardown
    ${fixture}  Should Has Before Fixture    ${test_case}    Passed Setup
    Should Has Step    ${fixture}   BuiltIn.No Operation
    ${fixture}  Should Has After Fixture    ${test_case}    Passed Teardown
    Should Has Step    ${fixture}   BuiltIn.No Operation

Test Case With Test Failed Setup And Teardown
    ${test_case}     Should Has Test Case   ${report}   Test Case With Test Failed Setup And Teardown
    Should Has Status    ${test_case}    failed
    ${fixture}  Should Has Before Fixture    ${test_case}    Failed Setup
    Should Has Status     ${fixture}    failed
    ${step}    Should Has Step    ${fixture}   BuiltIn.Fail
    Should Has Status    ${step}    failed
    ${fixture}  Should Has After Fixture    ${test_case}    Failed Teardown
    Should Has Status     ${fixture}    failed
    ${step}    Should Has Step    ${fixture}   BuiltIn.Fail
    Should Has Status    ${step}    failed
