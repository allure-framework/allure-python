===============
Tag a test case
===============

You can add an allure tag to a test case by to apply a gherkin tag to a
corresponding scenario:

..  code:: gherkin
    :name: tag-scenario-feature

    Feature: Allure tag support
        @distributed
        Scenario: Applying a tag directly to a scenario
            Given noop

The tag can also be applied to a feature. In that case it propagates to all
scenarios of the feature:

..  code:: gherkin
    :name: tag-feature-feature

    @isolated
    Feature: Allure tag support
        Scenario: Applying a tag to a feature
            Given noop

You can add any number of tags that way:

..  code:: gherkin
    :name: tag-multiple-feature

    @node-1 @node-2
    Feature: Allure tag support
        @node-3 @node-4
        Scenario: Applying multiple tags
            Given noop

