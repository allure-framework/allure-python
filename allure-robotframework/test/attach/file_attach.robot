*** Settings ***
Library     ../run_robot_library.py
Library     ../test_allure_library.py


*** Test Case ***
Data Attachment
    ${example_file}     Get Example File
    ${allure_report}    Run Robot With Allure    ${example_file}
    ${test_case}     Should Has Test Case   ${allure_report}    File Attachment
    ${step}   Should Has Step     ${test_case}    AllureLibrary.Attach File
    Should Has Attachment    ${step}