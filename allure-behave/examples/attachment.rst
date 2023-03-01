===========
Attachments
===========

You can attach data and files to behave test results. An attachment can be added
from a step definition function or from a hook. See examples below for more
details.

----------------------------------
Attach data from a step definition
----------------------------------

The easiest way to add an attachment is to call the :code:`allure.attach`
function from a step definition:

Feature file:
^^^^^^^^^^^^^
..  code:: gherkin
    :name: data-attachment-feature

    Feature: Allure attachments in behave tests
        Scenario: Data attachment from step definitions
            Given a step that adds a named attachment
            And a step that adds a typed named attachment

Step definition file:
^^^^^^^^^^^^^^^^^^^^^
..  code:: python
    :name: data-attachment-steps

    import allure
    from behave import given

    @given("a step that adds a named attachment")
    def step_impl(context):
        allure.attach(
            "This is the attachment with the name 'step.txt'",
            name="step.txt"
        )

    @given("a step that adds a typed named attachment")
    def step_impl(context):
        allure.attach(
            (
                "[DEBUG] This attachment is named 'trace.log' and has TEXT "
                "document appearance"
            ),
            name="trace.log",
            attachment_type=allure.attachment_type.TEXT
        )

----------------------------------
Attach file from a step definition
----------------------------------

Call the :code:`allure.attach.file` function to attach a file:

Feature file:
^^^^^^^^^^^^^
..  code:: gherkin
    :name: file-attachment-feature

    Feature: Allure attachments in behave tests
        Scenario: File attachment from a step definition
            Given a step that attaches a file

Step definition file:
^^^^^^^^^^^^^^^^^^^^^
..  code:: python
    :name: file-attachment-steps

    import allure
    from behave import given

    @given("a step that attaches a file")
    def step_impl(context):
        allure.attach.file(
            "./logs/web",
            name="web.log",
            attachment_type=allure.attachment_type.TEXT
        )

------------------
Attach from a hook
------------------

You can also attach data and files from a behave hook, e.g., from the
:code:`after_scenario`:

..  code:: python
    :name: attach-hook

    import allure

    def after_scenario(context, scenario):
        allure.attach(
            "This attachment will appear on a scenario level",
            name="attachment.txt",
            attachment_type=allure.attachment_type.TEXT
        )
