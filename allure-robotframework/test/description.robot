*** Settings ***
Library    ./library/run.py
Library    ./library/test.py


*** Variables ***
${TC_single}    | *Test Cases*                 |                 |                         |\n
...             | Demo Single Line Description |                 |                         |\n
...             |                              | [Documentation] | Single line description |\n
...             |                              | No Operation    |                         |\n

${TC_multi}    | *Test Cases*                |                 |                         |\n
...            | Demo Multi Line Description |                 |                         |\n
...            |                             | [Documentation] | Multi line              |\n
...            |                             | ...             | description             |\n
...            |                             | No Operation    |                         |\n

${TC_dynamic}    | *Test Cases              |                        |                     |\n
...              | Demo Dynamic Description |                        |                     |\n
...              |                          | [Documentation]        | Static description  |\n
...              |                          | Set Test Documentation | Dynamic description |\n

${TC_append}    | *Test Cases                     |                        |                     |\n
...             | Demo Append Dynamic Description |                        |                     |\n
...             |                                 | [Documentation]        | Static description  |\n
...             |                                 | Set Test Documentation | Dynamic description |\n
...             |                                 | ...                    | append=yes          |\n


*** Test Cases ***
Single Line Description
    ${tmp_dir}    Make Temp Dir
    ${test_case_dir}    Make Dir    ${tmp_dir}    test
    ${test_case}    Make Test Case    ${test_case_dir}    description.robot    ${TC_single}
    ${allure_report}    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}    Should Has Test Case    ${allure_report}    Demo Single Line Description
    Should Has Description    ${allure_report}    ${tc_matcher}    Single line description

Multi Line Description
    ${tmp_dir}    Make Temp Dir
    ${test_case_dir}    Make Dir    ${tmp_dir}    test
    ${test_case}    Make Test Case    ${test_case_dir}    description.robot    ${TC_multi}
    ${allure_report}    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}    Should Has Test Case    ${allure_report}    Demo Multi Line Description
    Should Has Description    ${allure_report}    ${tc_matcher}    Multi line\n description

Dynamic Description
    ${tmp_dir}    Make Temp Dir
    ${test_case_dir}    Make Dir    ${tmp_dir}    test
    ${test_case}    Make Test Case    ${test_case_dir}    description.robot    ${TC_dynamic}
    ${allure_report}    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}       Should Has Test Case      ${allure_report}    Demo Dynamic Description
    Should Has Description    ${allure_report}    ${tc_matcher}    Dynamic description

Append Dynamic Description
    ${tmp_dir}    Make Temp Dir
    ${test_case_dir}    Make Dir    ${tmp_dir}    test
    ${test_case}    Make Test Case    ${test_case_dir}    description.robot    ${TC_append}
    ${allure_report}    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}    Should Has Test Case    ${allure_report}    Demo Append Dynamic Description
    Should Has Description    ${allure_report}    ${tc_matcher}    Static description Dynamic description