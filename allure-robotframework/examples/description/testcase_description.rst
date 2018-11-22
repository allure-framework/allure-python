
Allure supports text case description. All next examples are valid:

.. code:: robotframework

    *** Test Cases ***
    Single Line Description
        [Documentation]     Single line description
        No Operation


.. code:: robotframework

    *** Test Cases ***
    Multi Line Description
        [Documentation]     Multi line
        ...                 description
        No Operation


.. code:: robotframework

    *** Test Cases ***
    Dynamic Description
        [Documentation]     Static description
        Set Test Documentation  Dynamic description


.. code:: robotframework

    *** Test Cases ***
    Append Dynamic Description
        [Documentation]     Static description
        Set Test Documentation  Dynamic description     append=yes