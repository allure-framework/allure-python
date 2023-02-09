=====================================
Provide a description for a test case
=====================================

Scenario description can be added in various ways:

#. In a .feature file
#. Dynamically in a step definition
#. Dynamically in a hook (e.g., before_scenario or after_scenario)

-----------------------------
Description in a feature file
-----------------------------

The easiest way to add a description to a test is to specify it directly in the
corresponding scenario in the .feature file. For example:

..  code-block:: gherkin
    :name: description-in-feature-feature

    Feature: Allure description for behave tests
        Scenario: Description from a .feature file
            This scenario has a description.
            This description spans across multiple lines.

            Given noop

The step definition is trivial:

..  code-block:: python
    :name: description-in-feature-steps

    from behave import given

    @given("noop")
    def step_impl(context):
        pass

-------------------
Dynamic description
-------------------

A description can be specified dynamically with the
:code:`allure.dynamic.description` function. This is useful if you want to
include runtime values in the description.


Description in a step definition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's suppose, we want to add a description to the following test:

..  code-block:: gherkin
    :name: description-in-step-feature

    Feature: Allure description for behave tests
        Scenario: Description from a step definition
            Given description is provided in a step definition

We can achieve that using the following step definition:

..  code-block:: python
    :name: description-in-step-steps

    from behave import given
    import allure

    @given("description is provided in a step definition")
    def step_impl(context):
        allure.dynamic.description(
            "This scenario has a description specified by the step definition"
        )


Description in a hook
^^^^^^^^^^^^^^^^^^^^^

It's also possible to add a description from a hook in the
:code:`environment.py` file.

Suppose we have the following feature file (and step definition is the same as
in `Description in a feature file`_):

..  code-block:: gherkin
    :name: description-in-hook-feature

    Feature: Allure description for behave tests
        Scenario: Description from the before_scenario hook
            Given noop

        Scenario: Description from the after_scenario hook
            Given noop

We can provide a description in the :code:`environment.py` like this:

..  code-block:: python
    :name: description-in-hook-env

    import allure

    def before_scenario(context, scenario):
        if "before_scenario" in scenario.name:
            allure.dynamic.description(
                "This scenario has a description specified in the "
                "before_scenario hook"
            )


    def after_scenario(context, scenario):
        if "after_scenario" in scenario.name:
            allure.dynamic.description(
                "This scenario has a description specified in the "
                "after_scenario hook"
            )
