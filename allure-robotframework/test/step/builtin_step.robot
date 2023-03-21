*** Settings ***
Library     ../run_robot_library.py
Library     ../test_allure_library.py


*** Test Case ***
Use Library Keyword With Allure Step
    ${allure_report}    Run Robot With Allure   examples/step/builtin_step.rst
    ${test_case}    Should Has Test Case   ${allure_report}   Log Builtin Keyword
    ${step}  Should Has Step   ${test_case}   BuiltIn.Log
    Should Has Parameter    ${step}   arg1  The rose is red
    ${step}  Should Has Step   ${test_case}   BuiltIn.Log
    Should Has Parameter    ${step}   arg1  the violet's blue

# ToDo: loglevel
# ToDo: Log Many
# ToDo: Comment