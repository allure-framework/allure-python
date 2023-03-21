
Allure report contains all next fixtures:



.. code:: robotframework

    *** Keywords ***
    Passed Setup
        No Operation

    Failed Setup
        Fail

    Passed Teardown
        No Operation

    Failed Teardown
        Fail

    *** Test Cases ***
    Test Case With Test Setup
        [Setup]     Passed Setup
        No Operation

    Test Case With Failed Test Setup
        [Setup]     Failed Setup
        No Operation

    Test Case With Test Teardown
        [Teardown]  Passed Teardown
        No Operation

    Test Case With Failed Test Teardown
        [Teardown]  Failed Teardown
        No Operation

    Test Case With Test Setup And Teardown
        [Setup]     Passed Setup
        [Teardown]  Passed Teardown
        No Operation

    Test Case With Test Failed Setup And Teardown
        [Setup]     Failed Setup
        [Teardown]  Failed Teardown
        No Operation