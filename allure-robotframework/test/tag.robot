*** Settings ***
Library    ./library/run.py
Library    ./library/test.py


*** Variables ***
${TC_TAGS}    | *Test Cases*             |                |                |                     |\n
...           | Demo Test Case With Tags |                |                |                     |\n
...           |                          | [Tags]         | my_awesome_tag | another_awesome_tag |\n
...           |                          | No Operation   |                |                     |\n

${TC_DYNAMIC_TAGS}    | *Test Cases*                     |          |                 |                 |\n
...                   | Demo Test Case With Dynamic Tags |          |                 |                 |\n
...                   |                                  | [Tags]   | static_tag      |                 |\n
...                   |                                  | Set Tags | dynamic_tag_one | dynamic_tag_two |\n

${TC_REMOVE_TAGS}     | *Test Cases*                      |                |                  |                  |\n
...                   | Demo Test Case With Removed Tags  |                |                  |                  |\n
...                   |                                   | [Tags]         | live_stat_tag    | dead_stat_tag    |\n
...                   |                                   | Set Tags       | live_dynamic_tag | dead_dynamic_tag |\n
...                   |                                   | Remove Tags    | dead_*           |                  |\n


*** Test Cases ***
Test Case With Tags
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    tag.robot    ${TC_TAGS}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case With Tags
    Should Has Tag    ${allure_report}    ${tc_matcher}    my_awesome_tag
    Should Has Tag    ${allure_report}    ${tc_matcher}    another_awesome_tag

Test Case With Dynamic Tags
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    tag.robot    ${TC_DYNAMIC_TAGS}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case With Dynamic Tags
    Should Has Tag    ${allure_report}    ${tc_matcher}    static_tag
    Should Has Tag    ${allure_report}    ${tc_matcher}    dynamic_tag_one
    Should Has Tag    ${allure_report}    ${tc_matcher}    dynamic_tag_two

Test Case With Removed Tags
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    tag.robot    ${TC_REMOVE_TAGS}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case With Removed Tags
    Should Has Tag    ${allure_report}    ${tc_matcher}    live_stat_tag
    Should Has Tag    ${allure_report}    ${tc_matcher}    live_dynamic_tag
    Should Not Has Tag    ${allure_report}    ${tc_matcher}    dead_stat_tag
    Should Not Has Tag    ${allure_report}    ${tc_matcher}    dead_dynamic_tag