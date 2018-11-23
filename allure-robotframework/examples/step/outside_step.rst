
.. code:: robotframework

    *** Settings ***
    Library     ./outside_step_library.py

    *** Test Cases ***
    Use Library Keyword With Allure Step
        Keyword With Allure Step