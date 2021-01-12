from pytest_bdd import scenario


@scenario("attachments_features\\attachment_in_step.feature", "Attachment in Given")
def test_given_with_attachments():
    pass


@scenario("attachments_features\\attachment_in_step.feature", "Attachment in When")
def test_when_with_attachments():
    pass


@scenario("attachments_features\\attachment_in_step.feature", "Attachment in Then")
def test_then_with_attachments():
    pass


@scenario("attachments_features\\attachment_in_exception_step.feature", "Attachment and Exception in Given")
def test_given_with_attachments_and_Exception():
    pass


@scenario("attachments_features\\attachment_in_many_steps.feature", "Attachment in Many Steps")
def test_attachment_in_many_steps():
    pass


@scenario("attachments_features\\attachment_in_failed_step.feature", "Attachment in Failed step")
def test_failed_step_with_attachment():
    pass
