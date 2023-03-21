
.. code:: robotframework

    *** Settings ***
    Library    ./labels_library.py
    *** Test Case ***
    Test Case With Custom Labels
        [Setup]    Open Browser With UI Layer
        Add Custom Label    stand   Alpha   Beta
