*** Settings ***
Library     ../run_robot_library.py
Library     ../test_allure_library.py


*** Test Case ***
Override Library Keyword And Make Allure Attachment
    ${example_file}     Get Example File
    ${allure_report}   Run Robot With Allure   ${example_file}
    ${test_case}     Should Has Test Case   ${allure_report}    Override Library Keyword And Make Allure Attachment
    ${step}     Should Has Step     ${test_case}    foreign_library_helper.Capture Page Screenshot
    Should Has Attachment   ${step}    name=screenshot