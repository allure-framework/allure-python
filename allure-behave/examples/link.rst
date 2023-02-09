=========================
Add a link to a test case
=========================

There are two ways of adding a link to a test result:

#. Using gherkin tags
#. Dynamically in python code

--------------------------------
Using gherkin tags to add a link
--------------------------------

You can associate a link with a test by applying the
:code:`@allure.link.<name>:<URL>` tag to the scenario:

..  code:: gherkin
    :name: link-scenario-feature

    Feature: Allure link support
        @allure.link.report:https://qameta.io/allure-report/
        Scenario: Scenario with the link to the allure report website
            Given noop

A link can also be associated with any scenario in a feature by applying the tag
to the feature:

..  code:: gherkin
    :name: link-feature-feature

    @allure.link.homepage:https://qameta.io
    Feature: Allure link support
        Scenario: Scenario with the link to the homepage
            Given noop

        Scenario: Another scenario with the link to the homepage
            Given noop

A link to an issue or a test case can be added with :code:`@allure.issue:<URL>`
and :code:`@allure.tms:<URL>`:

..  code:: gherkin
    :name: specialized-links-feature

    Feature: Allure link support
        @allure.issue:https://github.com/allure-framework/allure-python/issues/1
        Scenario: Scenario associated with the issue
            Given noop

        @allure.tms:https://qameta.io/#features
        Scenario: Scenario associated with the TMS test case
            Given noop

Please, note, that no whitespaces are allowed in a gherkin tag. Make sure your
URLs are `properly encoded <https://www.rfc-editor.org/rfc/rfc3986#page-12>`_.

----------------------------
Providing a link dynamically
----------------------------

You may also create a link dynamically and associate it with a test case in
various places in your python code.

Example
^^^^^^^
Here we add two links dynamically: one from the :code:`before_scenario` hook and
another one from the step definition.

Feature file:
"""""""""""""

..  code:: gherkin
    :name: dynamic-links-feature

    Feature: Allure link support
        Scenario: Issue from the step definition and link from the hook
            Given a link is associated with this test case

Steps definition file:
""""""""""""""""""""""

..  code:: python
    :name: dynamic-links-steps

    import allure
    from behave import given

    @given("a link is associated with this test case")
    def step_impl(context):
        allure.dynamic.issue(
            "https://github.com/allure-framework/allure-python/issues/1",
            "Skip None and empty values in json"
        )

environment.py:
"""""""""""""""

..  code:: python
    :name: dynamic-links-hooks

    import allure

    def before_scenario(context, scenario):
        allure.dynamic.link(
            "https://qameta.io/allure-report/",
            name="Allure Report"
        )
