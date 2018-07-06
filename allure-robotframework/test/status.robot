*** Settings ***
Library    ./library/run.py
Library    ./library/test.py


*** Variables ***
${TC_FAILED_STEP_WITH_MESSAGE}    | *TestCases*                                  |      |                    |\n
...                               | Demo Test Case With Failed Step With Message |      |                    |\n
...                               |                                              | Fail | msg=Failed Details |\n


*** Test Cases ***
Test Case With Failed Step With Message
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    status.robot    ${TC_FAILED_STEP_WITH_MESSAGE}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case With Failed Step With Message
    Should Has Status    ${allure_report}    ${tc_matcher}    failed
    Should Has Status Detail With Message    ${allure_report}    ${tc_matcher}    Failed Details
    ${step_matcher}=    Should Has Step    ${allure_report}    ${tc_matcher}   BuiltIn.Fail
    Should Has Status    ${allure_report}    ${step_matcher}    failed
    Should Has Status Detail With Message    ${allure_report}    ${step_matcher}    Failed Details