*** Settings ***
Library     ../run_robot_library.py
Library     ../test_allure_library.py


*** Variables ***
${TC_SUITE_SETUP}    | *Settings*                      |                     |\n
...                  | Suite Setup                     | Suite Setup Keyword |\n
...                  |                                 |                     |\n
...                  | *Test Cases*                    |                     |\n
...                  | Demo Test Case With Suite Setup |                     |\n
...                  |                                 | No Operation        |\n
...                  | *Keywords*                      |                     |\n
...                  | Suite Setup Keyword             |                     |\n
...                  |                                 | No Operation        |\n


*** Test Cases ***
Dummy
    No Operation

# ToDo: fix me - Container just holds a common fixtures, It is not repeat test structure.
#Test Case With Suite Setup
#    ${tmp_dir}=    Make Temp Dir
#    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
#    ${test_case}=    Make Test Case    ${test_case_dir}    fixture.robot    ${TC_SUITE_SETUP}
#    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
#    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case With Suite Setup
#    ${fixture_matcher}=    Should Has Before Fixture    ${allure_report}    ${tc_matcher}    Suite Setup Keyword
#    Should Has Step    ${allure_report}    ${fixture_matcher}   BuiltIn.No Operation

# ToDo: TearDown