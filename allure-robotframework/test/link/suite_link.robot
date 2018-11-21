*** Settings ***
Library     ../run_robot_library.py
Library     ../test_allure_library.py


*** Variables ***
${TC_LOG}    | *Settings*                        |              |                                     |\n
...          | Metadata                          | Link         | https://github.com/allure-framework |\n
...          |                                   |              |                                     |\n
...          | *Test Cases*                      |              |                                     |\n
...          | Demo Test Case In Suite With link |              |                                     |\n
...          |                                   | No Operation |                                     |\n


*** Test Cases ***
Test Case In Suite With link
    No Operation
# ToDo: deprecated, need to revove from code
#    ${tmp_dir}=    Make Temp Dir
#    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
#    ${test_case}=    Make Test Case    ${test_case_dir}    link.robot    ${TC_LOG}
#    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
#    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case In Suite With link
#    Should has link   ${allure_report}    ${tc_matcher}    https://github.com/allure-framework

# ToDo: other link types