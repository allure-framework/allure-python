Severity
--------

Allure utilize a native severity, for example, we have two test cases with different tags:

.. code:: robotframework

    *** Test Cases ***
    Test Case With Tag Alpha
        [Tags]  alpha
        No Operation

    Test Case With Tag Bravo
        [Tags]  bravo
        No Operation


In case, when we run it with option ``--critical=alpha``, first test case will be marked as critical. The same result
gets when use ``--noncritical=bravo``.