Attachment in fixtures
----------------------

Attachments are shown in the context of a test entity they belong to.

You can attach some context from fixture:

    >>> import pytest
    >>> import allure

    >>> @pytest.fixture
    ... def fixture_with_attachment():
    ...     allure.attach("Fixture context")

    >>> def test_fixture_attachment(fixture_with_attachment):
    ...     pass


or fixture finalizer:

    >>> import pytest
    >>> import allure

    >>> @pytest.fixture
    ... def fixture_with_attachment_in_finalizer(request):
    ...     def finalizer():
    ...         allure.attach(__file__)
    ...     request.addfinalizer(finalizer)

    >>> def test_fixture_finalizer_attachment(fixture_with_attachment_in_finalizer):
    ...     pass