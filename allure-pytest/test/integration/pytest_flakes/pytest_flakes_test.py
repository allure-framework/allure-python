import pytest


@pytest.mark.xfail()
def test_pytest_flakes(allured_testdir, request):
    """
    >>> def test_pytest_flakes_example():
    ...     assert True
    """

    allured_testdir.parse_docstring_source(request)
    allured_testdir.run_with_allure("--flakes")

    assert False, allured_testdir.allure_report
