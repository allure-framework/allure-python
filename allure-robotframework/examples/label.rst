=======================================
Allure labels for Robot Framework tests
=======================================

You can attach allure labels to test results using the following mechanisms:

#. From a test case file with robot framework tags
#. From a test library, i.e., directly from python code

-----------------------------------------
Add an allure label from a test case file
-----------------------------------------

Apply a :code:`allure.label.<NAME>:<VALUE>` tag to your test case. Such a tag
will be automatically converted to the allure label:

..  code:: robotframework
    :name: tag-custom-robot

    *** Test Cases ***
    Test authored by John Doe
        [Tags]  allure.label.author:John Doe
        No Operation

You can define any label that way, being it a built-in or a custom one. If you
want to add a built-in label, a shorter version of the syntax can be used:

..  code:: robotframework
    :name: tag-builtin-robot

    *** Test Cases ***
    Test with the pinned ID
        [Tags]  allure.id:1008
        ...     allure.story:RF tags as allure labels
        No Operation

Use the :code:`Test Tags` setting to automatically apply tags to all test cases:

..  code:: robotframework
    :name: tag-setting-robot

    *** Settings ***
    Test Tags  allure.feature:Allure labels support

    *** Test Cases ***
    Test with two BDD-labels
        [Tags]  allure.story:RF tags as allure labels
        No Operation

You can read more about applying tags to test cases here: `Tagging test cases`_.

---------------------------------------
Add an allure label from a test library
---------------------------------------

To add a label from python code use the :code:`@allure.label` decorator,
the :code:`allure.dynamic.label` function or their specialized alternatives for
built-in allure labels:

my_library.py:
^^^^^^^^^^^^^^
..  code:: python
    :name: code-labels-library

    import allure
    import os

    @allure.label("layer", "API")
    @allure.severity(allure.severity_level.CRITICAL)
    def open_api(host, port):
        allure.dynamic.label("endpoint", f"{host}:{port}")
        allure.dynamic.suite(f"Testing API at {host}")

Now, if you import this library in a test case file and invoke its
:code:`[Open API]` keyword, the test case receives four allure lables: layer,
severity, endpoint and suite:

..  code:: robotframework
    :name: code-labels-robot

    *** Settings ***
    Library  ./my_library.py

    *** Test Cases ***
    Test backend API
        [Documentation]     Four labels should be attached to this test result.
        Open API            host=localhost
        ...                 port=443


.. _`Tagging test cases`: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#tagging-test-cases