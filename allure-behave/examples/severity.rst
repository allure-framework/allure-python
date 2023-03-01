===============================
Specify severity of a test case
===============================

Use one of the following tags to specify severity of a test case:

#. :code:`@trivial`
#. :code:`@minor`
#. :code:`@normal`
#. :code:`@critical`
#. :code:`@blocker`

Those tags can be applied to scenarios:

..  code:: gherkin
    :name: severity-on-scenario

    Feature: Allure severity support
        @blocker
        Scenario: Blocking scenario
            Given noop

        @critical
        Scenario: Critical scenario
            Given noop

        @normal
        Scenario: Normal scenario
            Given noop

        @minor
        Scenario: Minor scenario
            Given noop

        @trivial
        Scenario: Trivial scenario
            Given noop

A severity tag can also be applied to a feature, affecting all scenarios of the
feature:

..  code:: gherkin
    :name: severity-on-feature

    @critical
    Feature: Allure severity support
        Scenario: This scenario inherits the @cricial tag
            Given noop

        Scenario: This scenario also inherits the @cricial tag
            Given noop

If multiple severity tags are affecting a scenario, the last one wins:

..  code:: gherkin
    :name: multiple-severities

    @critical, @blocker
    Feature: Allure severity support
        @minor @trivial
        Scenario: This is a trivial scenario
            Given noop

        Scenario: While this one is a blocker
            Given noop
