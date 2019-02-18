Attachments
-----------

Reports can display many different types of provided attachments that can complement a test, step or fixture result.
Attachments can be created either with invocation of ``allure.attach(body, name, attachment_type, extension):``

``body`` - raw content to be written into the file.
``name`` - a string with name of the file
``attachment_type`` - one of the allure.attachment_type values
``extension`` - is provided will be used as an extension for the created file.

    >>> import allure

    >>> def test_attach_body_with_default_kwargs():
    ...     allure.attach("Some content in plain text")

    >>> def test_attach_body():
    ...     xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    ...     <tag>
    ...         <inside>...</inside>
    ...     </tag>
    ...     """
    ...     allure.attach(xml_content, name='some attachment name', attachment_type=allure.attachment_type.XML)
    ...
    ...     allure.attach("Some content in plain text")


or ``allure.attach.file(source, name, attachment_type, extension)``:
``source`` - a string containing path to the file.
(other arguments are the same)

    >>> def test_attach_file():
    ...
    ...     allure.attach.file(__file__)  # this file path
