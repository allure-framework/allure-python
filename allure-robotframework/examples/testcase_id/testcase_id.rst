Testcase id
----

Allure supports custom testcase id. 
It uniquely identifies the test instead of the full name:

.. code:: robotframework

    *** Settings ***
    Library    ./testcases_library.py
    *** Test Cases ***
    Test Case With Id
        Set Testcase Id    some-allure-id
