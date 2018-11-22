*** Settings ***
Library     ../run_robot_library.py
Library     ../test_allure_library.py


*** Test Case ***
Override Library Keyword And Make Allure Attachment
    ${allure_report}   Run Robot With Allure   examples/attach/foreign_library_attach.rst
    ${test_case}     Should Has Test Case   ${allure_report}    Override Library Keyword And Make Allure Attachment
    ${step}     Should Has Step     ${test_case}    foreign_library_helper.Capture Page Screenshot
    Should Has Attachment   ${step}    name=screenshot