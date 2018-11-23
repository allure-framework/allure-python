*** Settings ***
Library     ../run_robot_library.py
Library     ../test_allure_library.py


*** Test Case ***
Data Attachment
    ${allure_report}    Run Robot With Allure    examples/attach/file_attach.rst
    ${test_case}     Should Has Test Case   ${allure_report}    File Attachment
    ${step}   Should Has Step     ${test_case}    AllureLibrary.Attach File
    Should Has Attachment    ${step}