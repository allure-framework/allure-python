import pytest
from hamcrest import assert_that
from hamcrest import all_of
from hamcrest import has_property, has_value
from hamcrest import contains_string
from allure_commons_test.report import has_test_case


@pytest.mark.parametrize("param", ["first", "second"])
def test_parametrized_attachment(executed_docstring_source, param):
    """
    >>> import pytest
    >>> import allure

    >>> @pytest.mark.parametrize("param", ["first", "second"])
    ... def test_parametrized_attachment_example(param):
    ...     allure.attach(param)
    """

    assert_that(executed_docstring_source.allure_report,
                all_of(
                    has_test_case("test_parametrized_attachment_example[{param}]".format(param=param)),
                    has_property("attachments",
                                 has_value(contains_string(param))
                                 )
                ))
