*** Settings ***
Library     ../run_robot_library.py
Library     ../test_allure_library.py


*** Test Case ***
Run Without options
    ${allure_report}   Run Robot With Allure   examples/severity/severity.rst
    ${test_case}     Should Has Test Case   ${allure_report}   Test Case With Tag Alpha
    Should Has Severity     ${test_case}    critical
    ${test_case}    Should Has Test Case    ${allure_report}    Test Case With Tag Bravo
    Should Has Severity     ${test_case}    critical


Run With Critical Tags Option
    ${allure_report}   Run Robot With Allure   examples/severity/severity.rst   critical=alpha
    ${test_case}     Should Has Test Case   ${allure_report}   Test Case With Tag Alpha
    Should Has Severity     ${test_case}    critical
    ${test_case}    Should Has Test Case    ${allure_report}    Test Case With Tag Bravo
    Should Not Has Severity   ${test_case}


Run With Noncritical Tags Option
    ${allure_report}   Run Robot With Allure   examples/severity/severity.rst   noncritical=bravo
    ${test_case}     Should Has Test Case   ${allure_report}   Test Case With Tag Alpha
    Should Has Severity     ${test_case}    critical
    ${test_case}    Should Has Test Case    ${allure_report}    Test Case With Tag Bravo
    Should Not Has Severity   ${test_case}

