
For example, you have a something like a Selenium library. Lets define some stub for it:

.. literalinclude:: ./foreign_library.py


make helper as you project scope library:

.. literalinclude:: ./foreign_library_helper.py


and finally your test writen for foreign library works and makes attachments to allure report:

.. code:: robotframework

    *** Settings ***
    Library     ./foreign_library.py
    Library     ./foreign_library_helper.py

    *** Test Cases ***
    Override Library Keyword And Make Allure Attachment
        Capture Page Screenshot