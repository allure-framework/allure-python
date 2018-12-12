
.. code:: robotframework

    *** Settings ***
    Library     ./status_library.py

    *** Test Cases ***
    Failed Test Case With Message
        Fail    msg=Failed Details

    Failed Test Case With Traceback
        Set Log Level    DEBUG
        Fail    msg=Failed Details

    Failed Test Case With Python Traceback
        Set Log Level    DEBUG
        Fail With Traceback      Fail message
