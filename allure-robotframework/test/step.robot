*** Settings ***
Library    ./library/run.py
Library    ./library/test.py


*** Variables ***
${TC_STEP}    | *TestCases*              |              |\n
...           | Demo Test Case With Step |              |\n
...           |                          | No Operation |\n

${TC_FAILED_STEP}    | *TestCases*                     |      |\n
...                  | Demo Test Case With Failed Step |      |\n
...                  |                                 | Fail |\n

${TC_SEQUENCE_STEPS_WITH_FILED_ONE}
...    | *TestCases*                                    |               |             |\n
...    | Demo Test Case With Steps Sequence With Failed |               |             |\n
...    |                                                | No Operation  |             |\n
...    |                                                | Fail          |             |\n
...    |                                                | Comment       | Hello World |\n

${TC_NESTED_STEPS}    | *TestCases*                      |                   |\n
...                   | Demo Test Case With Nested Steps |                   |\n
...                   |                                  | Grand Parent Step |\n
...                   | *Keywords*                       |                   |\n
...                   | Grand Parent Step                |                   |\n
...                   |                                  | Parent Step       |\n
...                   | Parent Step                      |                   |\n
...                   |                                  | No Operation      |\n

${TC_NESTED_STEPS_LAST_FAILED}    | *TestCases*                                  |                   |\n
...                               | Demo Test Case With Nested Steps Last Failed |                   |\n
...                               |                                              | Grand Parent Step |\n
...                               | *Keywords*                                   |                   |\n
...                               | Grand Parent Step                            |                   |\n
...                               |                                              | Parent Step       |\n
...                               | Parent Step                                  |                   |\n
...                               |                                              | Fail              |\n


*** Test Cases ***
Test Case With Step
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    step.robot    ${TC_STEP}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case With Step
    ${step_matcher}=    Should Has Step    ${allure_report}    ${tc_matcher}   BuiltIn.No Operation
    Should Has Status    ${allure_report}    ${step_matcher}    passed

Test Case With Failed Step
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    step.robot    ${TC_FAILED_STEP}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case With Failed Step
    Should Has Status    ${allure_report}    ${tc_matcher}    failed
    ${step_matcher}=    Should Has Step    ${allure_report}    ${tc_matcher}   BuiltIn.Fail
    Should Has Status    ${allure_report}    ${step_matcher}    failed

Test Case With Steps Sequence With Failed
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    step.robot    ${TC_SEQUENCE_STEPS_WITH_FILED_ONE}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case With Steps Sequence With Failed
    Should Has Status    ${allure_report}    ${tc_matcher}    failed
    ${first_step_matcher}=    Should Has Step    ${allure_report}    ${tc_matcher}   BuiltIn.No Operation
    Should Has Status    ${allure_report}    ${first_step_matcher}    passed
    ${second_step_matcher}=    Should Has Step    ${allure_report}    ${tc_matcher}   BuiltIn.Fail
    Should Has Status    ${allure_report}    ${second_step_matcher}    failed
    Should Not Has Step    ${allure_report}    ${tc_matcher}   BuiltIn.Comment

Test Case With Nested Steps
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    step.robot    ${TC_NESTED_STEPS}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case With Nested Steps
    ${grand_parent_step_matcher}=    Should Has Step    ${allure_report}    ${tc_matcher}   Grand Parent Step
    Should Has Status    ${allure_report}    ${grand_parent_step_matcher}    passed
    ${parent_step_matcher}=    Should Has Step    ${allure_report}    ${grand_parent_step_matcher}   Parent Step
    Should Has Status    ${allure_report}    ${parent_step_matcher}    passed
    ${step_matcher}=    Should Has Step    ${allure_report}    ${parent_step_matcher}   BuiltIn.No Operation
    Should Has Status    ${allure_report}    ${step_matcher}    passed

Test Case With Nested Steps Last Failed
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    step.robot    ${TC_NESTED_STEPS_LAST_FAILED}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case With Nested Steps Last Failed
    Should Has Status    ${allure_report}    ${tc_matcher}    failed
    ${grand_parent_step_matcher}=    Should Has Step    ${allure_report}    ${tc_matcher}   Grand Parent Step
    Should Has Status    ${allure_report}    ${grand_parent_step_matcher}    failed
    ${parent_step_matcher}=    Should Has Step    ${allure_report}    ${grand_parent_step_matcher}   Parent Step
    Should Has Status    ${allure_report}    ${parent_step_matcher}    failed
    ${step_matcher}=    Should Has Step    ${allure_report}    ${parent_step_matcher}   BuiltIn.Fail
    Should Has Status    ${allure_report}    ${step_matcher}    failed
