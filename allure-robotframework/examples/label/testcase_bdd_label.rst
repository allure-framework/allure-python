
.. code:: robotframework

    *** Settings ***
    Force Tags  allure.feature:Label

    *** Test Case ***
    Test Cases With BDD Labels
        [Tags]  allure.story:Test case BDD labels
        No Operation
