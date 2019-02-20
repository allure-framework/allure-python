import pytest
from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_attachment


@pytest.mark.parametrize("param", ["first", "second"])
def test_parametrized_attachment(executed_docstring_source, param):
    """
    >>> import pytest

    >>> @pytest.mark.parametrize("param", ["first", "second"])
    ... def test_parametrized_attachment_example(param):
    ...     assert param
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_parametrized_attachment_example[{param}]".format(param=param),
                              has_attachment()
                              )
                )
