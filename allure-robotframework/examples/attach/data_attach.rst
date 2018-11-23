

.. code:: robotframework

    *** Settings ***
    Library     AllureLibrary

    *** Test Cases ***
    Data Attachment
        Attach  Hello world


.. code:: robotframework

    *** Settings ***
    Library     AllureLibrary

    *** Test Cases ***
    Data Attachment With Name And Type
        Attach  https://github.com/allure-framework/allure2 https://github.com/allure-framework/allure-python
        ...     name=links  attachment_type=URI_LIST