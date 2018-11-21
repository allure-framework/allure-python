Tags
----

Allure supports robotframework tags:

.. code:: robotframework

    *** Test Cases ***
    Test Case With Tags
        [Tags]  alpha   bravo
        No Operation


уou can manipulate with tags:

.. code:: robotframework

    *** Test Cases ***
    Test Case With Dynamic Tags
        [Tags]  alpha
        Set Tags    bravo


.. code:: robotframework

    *** Test Cases ***
    Test Case With Removed Tags
        [Tags]  alpha   bravo
        Set Tags    charlie
        Remove Tags     bravo

allure will track it and show actual tags set.
