Links
-----

Issues are supported via tags prefixed with :code:`issue:` :

.. code:: robotframework

    *** Test Cases ***
    Test Case With Issue Link Without URL
        [Tags]  issue:ISSUE-1
        No Operation


.. code:: robotframework

    *** Test Cases ***
    Test Case With Issue Link With URL
        [Tags]  issue:https://jira.com/browse/ISSUE-1
        No Operation

TMS links are supported via tags prefixed with :code:`test_case:` :

.. code:: robotframework

    *** Test Cases ***
    Test Case With TMS Link Without URL
        [Tags]  test_case:TEST-1
        No Operation


.. code:: robotframework

    *** Test Cases ***
    Test Case With TMS Link With URL
        [Tags]  test_case:https://testrail.com/browse/TEST-1
        No Operation

Ordinary links are supported via tags prefixed with :code:`link:` :

.. code:: robotframework

    *** Test Cases ***
    Test Case With Unnamed Link
        [Tags]  link:https://homepage.com/
        No Operation


.. code:: robotframework

    *** Test Cases ***
    Test Case With Named Link
        [Tags]  link:[Home Page]https://homepage.com/
        No Operation

allure will track it and show actual tags set.
