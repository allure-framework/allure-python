import allure
import pytest

BODY = ['I Like to', 'Move It']


@pytest.mark.parametrize('attachment', BODY)
def test_attach_data_from_parametrized_test(attachment):
    """
    >>> allure_report = getfixture('allure_report')
    >>> for body in BODY:
    ...     assert_that(allure_report,
    ...                 has_test_case('test_attach_data_from_parametrized_test[{body}]'.format(body=body),
    ...                              has_attachment()
    ...                )
    ...     )
    """
    allure.attach(attachment)
