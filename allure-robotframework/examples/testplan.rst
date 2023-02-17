=========================================
Allure testplan for Robot Framework tests
=========================================

You can filter Robot Framework test cases by an ID or by a name with an allure
testplan.

#. Create a testplan file.
#. Set the :code:`ALLURE_TESTPLAN_PATH` environment variable to the testplan
   path.
#. Run the Robot Framework with the :code:`allure_robotframework.testplan`
   pre-run modifier.

-------------------
Creating a testplan
-------------------

Lets say, we have the following Robot Framework test data in the
:code:`testplan.robot` file:

..  code:: robotframework
    :name: testdata

    *** Test Cases ***
    Selected by Name
        No Operation

    Selected by ID
        [Tags]  allure.id:1008
        No Operation

    Not Selected
        [Tags]  allure.id:1009
        No Operation

And we want to select only two test cases:

#. The test case :code:`Selected by Name`.
#. The test case with ID :code:`1008`.

To achieve that, we need the following testplan (lets say, we put it in the
:code:`testplan.json` file):

..  code:: json
    :name: testplan

    {
        "version":"1.0",
        "tests": [
            {
                "selector": "Testplan.Selected by Name"
            },
            {"id": "1008"}
        ]
    }

-------------------------------------------------------------
Setting the :code:`ALLURE_TESTPLAN_PATH` environment variable
-------------------------------------------------------------

Refer to the docs on the environment you are working in on how to set up an
environment variable.

If you are working in Linux or MacOS and use bash or a similar shell, the most
convinient way is to put :code:`ALLURE_TESTPLAN_PATH=./testplan.json` before the
:code:`robot` command, or use the
:code:`export ALLURE_TESTPLAN_PATH=./testplan.json` statement.

If you are using PowerShell, set up the variable with the
:code:`$Env:ALLURE_TESTPLAN_PATH = "./testplan.json"` statement.

---------------------------
Running the Robot Framework
---------------------------

The following example shows how to execute the abovementioned test cases with
the testplan enabled (this is for Linux, bash; if you are using another
OS/Shell, the invocation may looks differently):

..  code:: shell

    ALLURE_TESTPLAN_PATH=./testplan.json robot --log NONE --report NONE --output NONE --extension robot --loglevel DEBUG --listener allure_robotframework:./allure-results --prerunmodifier allure_robotframework.testplan ./testplan.robot

The test cases, listed in the plan, will be executed::

    ==============================================================================
    Testplan
    ==============================================================================
    Selected by Name                                                      | PASS |
    ------------------------------------------------------------------------------
    Selected by ID                                                        | PASS |
    ------------------------------------------------------------------------------
    Testplan                                                              | PASS |
    2 tests, 2 passed, 0 failed
    ==============================================================================
    Output:  None

You can read more about the CLI arguments here:
`the Robot Framework command line options`_.

.. _`the Robot Framework command line options`: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#command-line-options