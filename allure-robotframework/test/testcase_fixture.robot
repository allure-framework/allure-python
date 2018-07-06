*** Settings ***
Library    ./library/run.py
Library    ./library/test.py


*** Variables ***
${TC_SETUP}    | *Test Cases*                   |              |                    |\n
...            | Demo Test Case With Test Setup |              |                    |\n
...            |                                | [Setup]      | Test Setup Keyword |\n
...            |                                | No Operation |                    |\n
...            | *Keywords*                     |              |                    |\n
...            | Test Setup Keyword             |              |                    |\n
...            |                                | No Operation |                    |\n

${TC_SETUP_FAILED}    | *Test Cases*                          |              |                    |\n
...                   | Demo Test Case With Failed Test Setup |              |                    |\n
...                   |                                       | [Setup]      | Test Setup Keyword |\n
...                   |                                       | No Operation |                    |\n
...                   | *Keywords*                            |              |                    |\n
...                   | Test Setup Keyword                    |              |                    |\n
...                   |                                       | Fail         |                    |\n

${TC_TEARDOWN}    | *Test Cases*                      |              |                       |\n
...               | Demo Test Case With Test Teardown |              |                       |\n
...               |                                   | [Teardown]   | Test Teardown Keyword |\n
...               |                                   | No Operation |                       |\n
...               | *Keywords*                        |              |                       |\n
...               | Test Teardown Keyword             |              |                       |\n
...               |                                   | No Operation |                       |\n

${TC_FAILED_TEARDOWN}    | *Test Cases*                             |              |                       |\n
...                      | Demo Test Case With Failed Test Teardown |              |                       |\n
...                      |                                          | [Teardown]   | Test Teardown Keyword |\n
...                      |                                          | No Operation |                       |\n
...                      | *Keywords*                               |              |                       |\n
...                      | Test Teardown Keyword                    |              |                       |\n
...                      |                                          | Fail         |                       |\n

${TC_SETUP_TEARDOWN}    | *Test Cases*                                |              |                       |\n
...                     | Demo Test Case With Test Setup And Teardown |              |                       |\n
...                     |                                             | [Setup]      | Test Setup Keyword    |\n
...                     |                                             | [Teardown]   | Test Teardown Keyword |\n
...                     |                                             | No Operation |                       |\n
...                     | *Keywords*                                  |              |                       |\n
...                     | Test Setup Keyword                          |              |                       |\n
...                     |                                             | No Operation |                       |\n
...                     | Test Teardown Keyword                       |              |                       |\n
...                     |                                             | No Operation |                       |\n

${TC_FAILED_SETUP_TEARDOWN}
...    | *Test Cases*                                       |              |                       |\n
...    | Demo Test Case With Test Failed Setup And Teardown |              |                       |\n
...    |                                                    | [Setup]      | Test Setup Keyword    |\n
...    |                                                    | [Teardown]   | Test Teardown Keyword |\n
...    |                                                    | No Operation |                       |\n
...    | *Keywords*                                         |              |                       |\n
...    | Test Setup Keyword                                 |              |                       |\n
...    |                                                    | Fail         |                       |\n
...    | Test Teardown Keyword                              |              |                       |\n
...    |                                                    | Fail         |                       |\n


*** Test Cases ***
Test Case With Test Setup
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    fixture.robot    ${TC_SETUP}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case With Test Setup
    ${fixture_matcher}=    Should Has Before Fixture    ${allure_report}    ${tc_matcher}    Test Setup Keyword
    Should Has Step    ${allure_report}    ${fixture_matcher}   BuiltIn.No Operation

Test Case With Failed Test Setup
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    fixture.robot    ${TC_SETUP_FAILED}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case With Failed Test Setup
    Should Has Status    ${allure_report}    ${tc_matcher}    failed
    ${fixture_matcher}=    Should Has Before Fixture    ${allure_report}    ${tc_matcher}    Test Setup Keyword
    Should Has Status    ${allure_report}    ${fixture_matcher}    failed
    ${step_matcher}=    Should Has Step    ${allure_report}    ${fixture_matcher}   BuiltIn.Fail
    Should Has Status    ${allure_report}    ${step_matcher}    failed

Test Case With Test Teardown
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    fixture.robot    ${TC_TEARDOWN}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case With Test Teardown
    ${fixture_matcher}=    Should Has After Fixture    ${allure_report}    ${tc_matcher}    Test Teardown Keyword
    Should Has Step    ${allure_report}    ${fixture_matcher}   BuiltIn.No Operation

Test Case With Failed Test Teardown
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    fixture.robot    ${TC_FAILED_TEARDOWN}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case With Failed Test Teardown
    Should Has Status    ${allure_report}    ${tc_matcher}    failed
    ${fixture_matcher}=    Should Has After Fixture    ${allure_report}    ${tc_matcher}    Test Teardown Keyword
    Should Has Status    ${allure_report}    ${fixture_matcher}    failed
    ${step_matcher}=    Should Has Step    ${allure_report}    ${fixture_matcher}   BuiltIn.Fail
    Should Has Status    ${allure_report}    ${step_matcher}    failed

Test Case With Test Setup And Teardown
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    fixture.robot    ${TC_SETUP_TEARDOWN}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case With Test Setup And Teardown
    ${before_fixture_matcher}=    Should Has Before Fixture    ${allure_report}    ${tc_matcher}    Test Setup Keyword
    Should Has Step    ${allure_report}    ${before_fixture_matcher}   BuiltIn.No Operation
    ${after_fixture_matcher}=    Should Has After Fixture    ${allure_report}    ${tc_matcher}    Test Teardown Keyword
    Should Has Step    ${allure_report}    ${after_fixture_matcher}   BuiltIn.No Operation

Test Case With Test Failed Setup And Teardown
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    fixture.robot    ${TC_FAILED_SETUP_TEARDOWN}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case With Test Failed Setup And Teardown
    Should Has Status    ${allure_report}    ${tc_matcher}    failed
    ${before_fixture_matcher}=    Should Has Before Fixture    ${allure_report}    ${tc_matcher}    Test Setup Keyword
    Should Has Status    ${allure_report}    ${before_fixture_matcher}    failed
    ${step_matcher}=    Should Has Step    ${allure_report}    ${before_fixture_matcher}   BuiltIn.Fail
    Should Has Status    ${allure_report}    ${step_matcher}    failed
    ${after_fixture_matcher}=    Should Has After Fixture    ${allure_report}    ${tc_matcher}    Test Teardown Keyword
    Should Has Status    ${allure_report}    ${after_fixture_matcher}    failed
    ${step_matcher}=    Should Has Step    ${allure_report}    ${after_fixture_matcher}   BuiltIn.Fail
    Should Has Status    ${allure_report}    ${step_matcher}    failed