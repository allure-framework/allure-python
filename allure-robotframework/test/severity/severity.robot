*** Settings ***
Library     ../run_robot_library.py
Library     ../test_allure_library.py


*** Test Case ***
Run Without options
    ${example_file}     Get Example File
    ${allure_report}   Run Robot With Allure   ${example_file}
    ${test_case}     Should Has Test Case   ${allure_report}   Test Case With Tag Alpha
    Should Has Severity     ${test_case}    critical
    ${test_case}    Should Has Test Case    ${allure_report}    Test Case With Tag Bravo
    Should Has Severity     ${test_case}    critical


Run With Critical Tags Option
    ${example_file}     Get Example File
    ${allure_report}   Run Robot With Allure   ${example_file}  critical=alpha
    ${test_case}     Should Has Test Case   ${allure_report}   Test Case With Tag Alpha
    Should Has Severity     ${test_case}    critical
    ${test_case}    Should Has Test Case    ${allure_report}    Test Case With Tag Bravo
    Should Not Has Severity   ${test_case}


Run With Noncritical Tags Option
    ${example_file}     Get Example File
    ${allure_report}   Run Robot With Allure   ${example_file}  noncritical=bravo
    ${test_case}     Should Has Test Case   ${allure_report}   Test Case With Tag Alpha
    Should Has Severity     ${test_case}    critical
    ${test_case}    Should Has Test Case    ${allure_report}    Test Case With Tag Bravo
    Should Not Has Severity   ${test_case}

