*** Settings ***
Library    ./library/run.py
Library    ./library/test.py


*** Variables ***
${TC_SEVERITY}    | *Test Cases*                      |              |       |\n
...               | Demo Test Case Severity - Alpha   | [Tags]       | alpha |\n
...               |                                   | No Operation |       |\n
...               |                                   |              |       |\n
...               | Demo Test Case Severity - Bravo   | [Tags]       | bravo |\n
...               |                                   | No Operation |       |\n


*** Test Cases ***
Test Case Severity Critical
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    step.robot    ${TC_SEVERITY}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}    critical=alpha
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case Severity - Alpha
    Should Has Severity   ${allure_report}    ${tc_matcher}    critical
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case Severity - Bravo
    Should Not Has Severity   ${allure_report}    ${tc_matcher}

Test Case Severity Noncritical
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    step.robot    ${TC_SEVERITY}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}    noncritical=alpha
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case Severity - Alpha
    Should Not Has Severity   ${allure_report}    ${tc_matcher}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case Severity - Bravo
    Should Has Severity   ${allure_report}    ${tc_matcher}   critical