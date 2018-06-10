*** Settings ***
Suite Setup     Suite Setup Keyword
Suite Teardown  Suite Teardown Keyword
*** Test Cases ***
Case Without Test Fixtures
    No Operation

Case With Test Setup
    [Setup]  Test Setup Keyword
    No Operation

Case With Test Teardown
    [Teardown]  Test Teardown Keyword
    No Operation

Case With Test Fixtures
    [Setup]  Test Setup Keyword
    [Teardown]  Test Teardown Keyword
    No Operation

*** Keywords ***
Suite Setup Keyword
    No Operation

Suite Teardown Keyword
    No Operation

Test Setup Keyword
    No Operation

Test Teardown Keyword
    No Operation