=====================================
Allure tags for Robot Framework tests
=====================================

You can apply an allure tag to your Robot Framework tests either in Robot
Framework test data (.robot files) or in a test library (.py files).

----------------------------------------
Allure tags in Robot Framework test data
----------------------------------------

All Robot Framework tags (except those, started with ``allure.``) are
automatically converted into allure tags:

..  code:: robotframework
    :name: tags-static-robot

    *** Test Cases ***
    Distributed Legacy Test
        [Tags]  distributed     legacy
        No Operation

The conversion happens when a test case is completed, so any changes to the set
of tags are reflected:

..  code:: robotframework
    :name: tags-dynamic-robot

    *** Test Cases ***
    Isolated Test
        [Tags]          distributed
        Set Tags        isolated
        Remove Tags     distributed

Be careful, because any failed step stops subsequent tag modifications:

..  code:: robotframework
    :name: tags-partial-robot

    *** Test Cases ***
    Supposed to Be an Isolated Test
        [Documentation]     But ends up being a distributed one.
        [Tags]              distributed
        Fail                Unexpected failure
        Set Tags            isolated
        Remove Tags         distributed

You can apply an allure tag explicitly, with the
:code:`allure.label.tag:<value>` Robot Framework tag or its shorter version,
:code:`allure.tag:<value>`:

..  code:: robotframework
    :name: tags-explicit-robot

    *** Test Cases ***
    Explicit External Test
        [Tags]  allure.label.tag:explicit   allure.tag:extrenal
        No Operation

All other Robot Framework tags, starting with :code:`allure.` are not converted:

..  code:: robotframework
    :name: tags-noconv-robot

    *** Test Cases ***
    No Allure Tags
        [Tags]  allure.label.as_id:1008   allure.feature:Allure tags support
        No Operation

Read more about applying tags to Robot Framework test cases in this article:
`Tagging test cases`_.

-------------------------------------------
Allure tags in Robot Framework test library
-------------------------------------------

Use the :code:`@allure.tag` decorator or the :code:`allure.dynamic.tag` function
to add an allure tag to the current test result.

**my_lib.py***:

..  code:: python
    :name: tags-code-lib

    import allure

    @allure.tag("external")
    def connect_to_external_api():
        pass

    @allure.tag("legacy")
    def download_service_list():
        connect_to_external_api()
        allure.dynamic.tag("stateful")

**Robot Framework test data**:

..  code:: robotframework
    :name: tags-code-robot

    *** Settings ***
    Library     ./my_lib.py

    *** Test Cases ***
    Stateful External Legacy Test
        Download Service List

.. _`Tagging test cases`: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#tagging-test-cases