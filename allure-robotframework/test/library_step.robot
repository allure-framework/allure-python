*** Settings ***
Library    ./library/run.py
Library    ./library/test.py

*** Variables ***
@{TC_OUTSIDE_STEP__LIBRARY}
...    from external import passed_outside_step, failed_outside_step
...
...    def step_contains_passed_outside_step(): passed_outside_step()
...
...    def step_contains_failed_outside_step(): failed_outside_step()


@{TC_OUTSIDE_STEP__EXTERNAL_PY}
...    import allure
...
...    @allure.step("Passed Outside Step")
...    def passed_outside_step(): pass
...
...    @allure.step("Failed Outside Step")
...    def failed_outside_step(): assert False, "Hello there"

${TC_PASSED_OUTSIDE_STEP}    | *Settings*                              |                                   |\n
...                          | Library                                 | ./helper.py                       |\n
...                          |                                         |                                   |\n
...                          | *TestCase*                              |                                   |\n
...                          | Demo Test Case With Passed Outside Step |                                   |\n
...                          |                                         | Step Contains Passed Outside Step |\n

${TC_FAILED_OUTSIDE_STEP}    | *Settings*                              |                                   |\n
...                          | Library                                 | ./helper.py                       |\n
...                          |                                         |                                   |\n
...                          | *TestCase*                              |                                   |\n
...                          | Demo Test Case With Failed Outside Step |                                   |\n
...                          |                                         | Step Contains Failed Outside Step |\n

*** Test Cases ***
Test Case With Passed Outside Step
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    Make File    ${test_case_dir}    helper.py    ${TC_OUTSIDE_STEP__LIBRARY}
    Make File    ${test_case_dir}    external.py    ${TC_OUTSIDE_STEP__EXTERNAL_PY}
    ${test_case}=    Make Test Case    ${test_case_dir}    step.robot    ${TC_PASSED_OUTSIDE_STEP}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}   Demo Test Case With Passed Outside Step
    ${step_matcher}=    Should Has Step    ${allure_report}    ${tc_matcher}   helper.Step Contains Passed Outside Step
    ${outside_step_matcher}=    Should Has Step    ${allure_report}    ${step_matcher}   Passed Outside Step
    Should Has Status    ${allure_report}    ${outside_step_matcher}    passed

Test Case With Failed Outside Step
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    Make File    ${test_case_dir}    helper.py    ${TC_OUTSIDE_STEP__LIBRARY}
    Make File    ${test_case_dir}    external.py    ${TC_OUTSIDE_STEP__EXTERNAL_PY}
    ${test_case}=    Make Test Case    ${test_case_dir}    step.robot    ${TC_FAILED_OUTSIDE_STEP}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}   Demo Test Case With Failed Outside Step
    Should Has Status    ${allure_report}    ${tc_matcher}    failed
    ${step_matcher}=    Should Has Step    ${allure_report}    ${tc_matcher}   helper.Step Contains Failed Outside Step
    ${outside_step_matcher}=    Should Has Step    ${allure_report}    ${step_matcher}   Failed Outside Step
    Should Has Status    ${allure_report}    ${outside_step_matcher}    failed