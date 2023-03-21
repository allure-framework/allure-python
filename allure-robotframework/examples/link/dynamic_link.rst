Dynamic Links
-----

.. code:: robotframework

    *** Test Cases ***
    Test Case With Dynamic Link
        Evaluate    allure.dynamic.issue('https://jira.com/browse/ISSUE-1', 'ISSUE-1')
        ...         modules=allure
        Evaluate    allure.dynamic.testcase('https://testrail.com/browse/TEST-1', 'TEST-1')
        ...         modules=allure
        Evaluate    allure.dynamic.link('https://homepage.com/', name='homepage')
        ...         modules=allure
