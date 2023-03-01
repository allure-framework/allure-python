======================================
Allure links for Robot Framework tests
======================================

You can add a link to a test result in a way, similar to
`allure labels <label.rst>`_, either

#. in a test case definition as a Robot Framework tag, or
#. in a test library (in python code)

---------------------------------------
A Robot Framework tag as an allure link
---------------------------------------

Use a :code:`allure.<LINK TYPE>[.<TEXT>]:<LINK>` tag to associate a link with
the test case. The :code:`<LINK Type>` should be one of :code:`link`,
:code:`issue` or :code:`tms`. The :code:`.<TEXT>` part is optional and may be
omitted. In that case the value of the link is used as the text.

The following example contains a test case with a link to the allure-python
repository:

..  code:: robotframework
    :name: tag-unnamed-robot

    *** Test Cases ***
    Allure Plain Link
        [Tags]  allure.link:https://github.com/allure-framework/allure-python
        No Operation

In the next example the exact same link will be shown as 'allure-python' in the
report:

..  code:: robotframework
    :name: tag-named-robot

    *** Test Cases ***
    Allure Plain Link
        [Tags]  allure.link.allure-python:https://github.com/allure-framework/allure-python
        No Operation

To link a test case to an issue, follow the next example:

..  code:: robotframework
    :name: tag-issue-robot

    *** Test Cases ***
    Allure Issue Link
        [Tags]  allure.issue.ISSUE-1:https://github.com/allure-framework/allure-python/issues/1
        No Operation

And you can also link a test case to the corresponding item in your test
management system:

..  code:: robotframework
    :name: tag-tms-robot

    *** Test Cases ***
    Allure TMS Link
        [Tags]  allure.tms.TESTCASE-1:https://my-tms/test-cases/1
        No Operation

Read more about applying tags to Robot Framework test cases in this article:
`Tagging test cases`_.

--------------------------------------
Add an allure link from a test library
--------------------------------------

Use allure.dynamic.link, allure.dynamic.issue or allure.dynamic.testcase to add
a link of an appropriate type.

The following example shows the usage of all those functions at once:

**my_lib.py**:

..  code:: python
    :name: code-links-lib

    import allure

    def add_three_links():
        allure.dynamic.link("https://github.com/allure-framework/allure-python", name="allure-python")
        allure.dynamic.issue("https://github.com/allure-framework/allure-python/issues/1", name="ISSUE-1")
        allure.dynamic.testcase("https://my-tms/test-cases/1", name="TESTCASE-1")

**The test data**:

..  code:: robotframework
    :name: code-links-robot

    *** Settings ***
    Library     ./my_lib.py

    *** Test Cases ***
    Allure Link Decorators and Functions
        Add Three Links


.. _`Tagging test cases`: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#tagging-test-cases