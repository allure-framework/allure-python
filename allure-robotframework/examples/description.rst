==========================
Description of a test case
==========================

Allure-robotframework automatically converts documentation of a Robot Framework
test case into allure test case description. The documentation can be set with
the :code:`[Documentation]` test setting:

..  code:: robotframework
    :name: setting-singleline-robot

    *** Test Cases ***
    Single line doc from the setting
        [Documentation]     This documentation will appear as allure description
        No Operation

The documentation may span multiple lines:

..  code:: robotframework
    :name: setting-multiline-robot

    *** Test Cases ***
    Multiline doc from the setting
        [Documentation]     This documentation contains multiple lines of text.
        ...                 It will also appear as allure description.
        No Operation

------------------------------------------
The :code:`Set Test Documentation` keyword
------------------------------------------

The documentation can also be set dynamically with the
`Set Test Documentation keyword`_:

..  code:: robotframework
    :name: keyword-robot

    *** Test Cases ***
    Multiline doc from the keyword
        Set Test Documentation  This documentation will appear as allure description.


.. _Set Test Documentation keyword: https://robotframework.org/robotframework/latest/libraries/BuiltIn.html#Set%20Test%20Documentation

----------------------------------
Preconditions and expected results
----------------------------------

Import :code:`AllureLibrary` to set preconditions and expected results directly
from Robot Framework tests. Use :code:`Preconditions` and :code:`Expected Results`
for plain text, or :code:`Preconditions Html` and :code:`Expected Results Html`
for HTML. Each keyword replaces the previous value for its corresponding field.

..  code:: robotframework
    :name: preconditions-expected-results-robot

    *** Settings ***
    Library    AllureLibrary

    *** Test Cases ***
    Preconditions and expected results
        Preconditions    Preconditions
        Preconditions Html    <p>Preconditions</p>
        Expected Results    Expected results
        Expected Results Html    <p>Expected results</p>
