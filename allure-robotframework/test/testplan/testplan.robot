*** Settings ***
Library     ../run_robot_library.py
Library     ../test_allure_library.py


*** Variables **
${PLAN_A}   \{
...             "version":"1.0",
...             "tests": [
...                 { "id": "123", "selector": "Second testcase"}
...             ]
...         \}

*** Test Case ***
Failed Test Case With Message
    ${allure_report}    Run Robot With Allure  examples/testplan/testplan.rst  testplan=${PLAN_A}