====================================
Attachments in allure_robotframework
====================================

You can attach data and files to a test result with the :code:`Attach` and
:code:`Attach File` keywords.

---------------
Data attachment
---------------

Use the :code:`Attach` to attach some textual data to your test:

..  code:: robotframework
    :name: data-attachment-default

    *** Settings ***
    Library         AllureLibrary

    *** Variables ***
    ${log_message}  This attachment was created using the allure_robotframework
    ...             library

    *** Test Cases ***
    Data Attachment
        Attach      ${log_message}

You can provide a name and a type of your attachments:

..  code:: robotframework
    :name: data-attachment-name-type

    *** Settings ***
    Library     AllureLibrary

    *** Variables ***
    ${links}    https://github.com/allure-framework/allure2
    ...         https://github.com/allure-framework/allure-python

    *** Test Cases ***
    Data Attachment
        Attach  ${links}
        ...     name=links  attachment_type=URI_LIST


---------------
File attachment
---------------

Use the :code:`Attach File` keyword to attach some file:

..  code:: robotframework
    :name: file-attachment-default

    *** Settings ***
    Library     AllureLibrary

    *** Test Cases ***
    File Attachment
        Attach File     ./my_file.txt

It's possible to specify a name and a type of the attachment:

..  code:: robotframework
    :name: file-attachment-name-type

    *** Settings ***
    Library             AllureLibrary

    *** Test Cases ***
    File Attachment
        Attach File     ./my_file.txt
        ...             name=my-file  attachment_type=TEXT


---------------------
Automatic attachments
---------------------

If you want to automatically attach files, created by some library, you can use
the trick, described below.

Lets say, we want to automatically attach screenshots, created by the
`SeleniumLibrary's Capture Page Screenshot`_ keyword. To achieve that, lets
create a wrapper over the SeleniumLibrary:

selenium_wrapper.py:
^^^^^^^^^^^^^^^^^^^^
..  code:: python
    :name: selenium-wrapper

    import allure
    from robot.libraries.BuiltIn import BuiltIn

    class SeleniumWrapper:
        ROBOT_LIBRARY_SCOPE = "TEST SUITE"
        ROBOT_LISTENER_API_VERSION = 2

        def __init__(self):
            self.ROBOT_LIBRARY_LISTENER = self

        def _start_suite(self, name, attrs):
            BuiltIn().set_library_search_order(__name__)

        def capture_page_screenshot(self, *args, **kwargs):
            target_lib = BuiltIn().get_library_instance('SeleniumLibrary')
            path = target_lib.capture_page_screenshot(*args, **kwargs)
            allure.attach.file(
                path,
                name="page",
                attachment_type=allure.attachment_type.JPG
            )
            return path

    selenium_wrapper = SeleniumWrapper

The wrapper sets itself as the first library in the library resolution order of
the Robot Framework. It uses the SeleniumLibrary under the hood, attaching the
output file to the allure report.

Import both the library and the wrapper in your .robot file:

..  code:: robotframework
    :name: selenium-suite

    *** Settings ***
    Library     SeleniumLibrary
    Library     ./selenium_wrapper.py

    *** Test Cases ***
    Automatic Screenshot Attachment
        Open Browser                https://localhost:443    Chrome
        Capture Page Screenshot
        [Teardown]  Close Browser

All screenshots are now automatically attached to your allure report.

.. _SeleniumLibrary's Capture Page Screenshot: https://robotframework.org/SeleniumLibrary/SeleniumLibrary.html#Capture%20Page%20Screenshot
