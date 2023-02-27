=================================
Add a custom label to a test case
=================================

It's possible to add a custom label to a behave scenario. Simply apply
:code:`@allure.label.<name>:<value>` tag to your scenario, e.g.:

..  code:: gherkin
    :name: label-feature

    Feature: Allure label for behave tests
        @allure.label.author:John-Doe
        Scenario: Scenario marked with an author label
            Given noop

Note, that neither the name nor the value of a label, added that way, may
contain a whitespace character.
