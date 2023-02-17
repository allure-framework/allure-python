===========================================
Use allure testplan to selectivly run tests
===========================================

You can filter test cases with a testplan file. Just create a JSON file and put
its path in the :code:`ALLURE_TESTPLAN_PATH` environment variable.

Then, when you run behave, allure will detect a testplan. Only tests that are
explicitly listed in the plan will be executed.

To demontrate how a testplan works with behave, lets assume the following
directory structure::

    .
    ├── features
    │   ├── steps
    │   │   └── steps.py
    │   ├── testplan-1.feature
    │   └── testplan-2.feature
    └── testplan.json

**testplan-1.feature**:

..  code:: gherkin
    :name: fullname-feature-1

    Feature: Allure testplan support
        Scenario: Scenario selection
            Given noop

        Scenario: Scenario deselection
            Given noop

**testplan-2.feature**:

..  code:: gherkin
    :name: fullname-feature-2

    Feature: Allure testplan support 2
        Scenario: Scenario selection 2
            Given noop

        Scenario: Scenario deselection 2
            Given noop

**steps.py**:

..  code:: python
    :name: steps

    from behave import given

    @given("noop")
    def step_impl(context):
        pass

**testplan.json**:

..  code:: json
    :name: fullname-testplan

    {
        "version":"1.0",
        "tests": [
            {
                "selector": "Allure testplan support: Scenario selection"
            },
            {
                "selector": "Allure testplan support 2: Scenario selection 2"
            }
        ]
    }

Now, when we run behave with allure and testplan enabled:

**on Linux or MacOS, with bash**:

..  code:: bash

    ALLURE_TESTPLAN_PATH=./testplan.json behave -f allure_behave.formatter:AllureFormatter -f pretty -o allure-results

or:

..  code:: bash

    export ALLURE_TESTPLAN_PATH=./testplan.json
    behave -f allure_behave.formatter:AllureFormatter -f pretty -o allure-results

**on Windows, with PowerShell**:

..  code:: powershell

    $Env:ALLURE_TESTPLAN_PATH = "./testplan.json"
    behave -f allure_behave.formatter:AllureFormatter -f pretty -o allure-results

We can see, that only test cases, enumerated in the testplan, are executed::

    Feature: Allure testplan support # features/testplan-1.feature:1

      Scenario: Scenario selection  # features/testplan-1.feature:2
        Given noop                  # features/steps/steps.py:3 0.000s

      Scenario: Scenario deselection  # features/testplan-1.feature:5
        Given noop                    # None

    SKIP Scenario Scenario deselection 2: Not in allure test plan
    Feature: Allure testplan support 2 # features/testplan-2.feature:1

      Scenario: Scenario selection 2  # features/testplan-2.feature:2
        Given noop                    # features/steps/steps.py:3 0.000s

      Scenario: Scenario deselection 2  # features/testplan-2.feature:5
        Given noop                      # None

    2 features passed, 0 failed, 0 skipped
    2 scenarios passed, 0 failed, 2 skipped
    2 steps passed, 0 failed, 2 skipped, 0 undefined
    Took 0m0.000s

------------------------------
Select test cases by allure id
------------------------------

If you link you scenarios to corresponding test cases with the :code:`as_id`
label, you can filter them by those IDs instead:

**testplan-1.feature**:

..  code:: gherkin
    :name: id-feature-1

    Feature: Allure testplan support
        @allure.label.as_id:1004
        Scenario: Scenario selection
            Given noop

        @allure.label.as_id:1005
        Scenario: Scenario deselection
            Given noop

**testplan-2.feature**:

..  code:: gherkin
    :name: id-feature-2

    Feature: Allure testplan support 2
        @allure.label.as_id:1006
        Scenario: Scenario selection 2
            Given noop

        @allure.label.as_id:1007
        Scenario: Scenario deselection 2
            Given noop

**steps.py**:

..  code:: json
    :name: id-testplan

    {
        "version":"1.0",
        "tests": [
            {"id": "1004"},
            {"id": "1006"}
        ]
    }

If we run behave with this testplan, the same set of scenarios will be executed.

.. Note::

    You can read more about allure labels support in behave
    `here <label.rst>`_.

---------------------
Hiding excluded tests
---------------------

To hide tests, excluded by the testplan, add the
:code:`-D AllureFormatter.hide_excluded=True` argument:

..  code:: shell

    behave -f allure_behave.formatter:AllureFormatter -D AllureFormatter.hide_excluded=True -f pretty -o allure-results

Skipped tests will still be visible in the behave output, but they will not be
included in the allure report.
