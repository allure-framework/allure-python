
.. code:: robotframework

    *** Settings ****
    Force Tags:   epic:Tag    feature:Label

    *** Test Case ***
    Test Cases With BDD Labels
        [Tags]  story:Test case BDD labels
        No Operation
