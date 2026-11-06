import allure


__all__ = [
    "attach", "attach_file", "global_attach", "global_attach_file", "global_error",
    "preconditions", "preconditions_html", "expected_results", "expected_results_html",
]


def _attachment_type(name):
    try:
        return allure.attachment_type[name]
    except KeyError:
        return name


def attach(data, name=None, attachment_type=None, extension=None):
    allure.attach(data, name=name, attachment_type=_attachment_type(attachment_type), extension=extension)


def attach_file(source, name=None, attachment_type=None, extension=None):
    allure.attach.file(source, name=name, attachment_type=_attachment_type(attachment_type), extension=extension)


def global_attach(data, name=None, attachment_type=None, extension=None):
    allure.global_attach(data, name=name, attachment_type=_attachment_type(attachment_type), extension=extension)


def global_attach_file(source, name=None, attachment_type=None, extension=None):
    allure.global_attach.file(source, name=name, attachment_type=_attachment_type(attachment_type), extension=extension)


def global_error(message, trace=None, *, status = allure.error_status.BROKEN):
    allure.global_error(message, trace=trace, status=status)


def preconditions(text):
    """Set the test preconditions as plain text."""
    allure.dynamic.preconditions(text)


def preconditions_html(text):
    """Set the test preconditions as HTML."""
    allure.dynamic.preconditions_html(text)


def expected_results(text):
    """Set the expected test results as plain text."""
    allure.dynamic.expected_results(text)


def expected_results_html(text):
    """Set the expected test results as HTML."""
    allure.dynamic.expected_results_html(text)
