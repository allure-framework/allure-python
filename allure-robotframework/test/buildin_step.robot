*** Settings ***
Library    ./library/run.py
Library    ./library/test.py


*** Variables ***
${TC_LOG}    | *Test Cases*       |     |        |\n
...          | Demo Test Case Log |     |        |\n
...          |                    | Log | First  |\n
...          |                    | Log | Second |\n


*** Test Cases ***
Test Case Log
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    step.robot    ${TC_LOG}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case Log
    ${first_step_matcher}=    Should Has Step    ${allure_report}    ${tc_matcher}   BuiltIn.Log
    Should Has Parameter    ${allure_report}    ${first_step_matcher}   arg1    First
    ${second_step_matcher}=    Should Has Step    ${allure_report}    ${tc_matcher}   BuiltIn.Log
    Should Has Parameter    ${allure_report}    ${second_step_matcher}   arg1    Second

# ToDo: loglevel
# ToDo: Log Many
# ToDo: Comment