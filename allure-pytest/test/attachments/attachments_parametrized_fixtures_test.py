import pytest
import allure


PARAMS = ["first", "second", "third"]


@pytest.fixture(scope='module', params=PARAMS)
def attach_data_in_parametrized_fixture(request):
    allure.attach(request.param, name=request.param, attachment_type='text/plain')


def test_attach_data_in_parametrized_fixture(attach_data_in_parametrized_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> for param in PARAMS:
    ...     assert_that(allure_report,
    ...                 has_test_case('test_attach_data_in_parametrized_fixture[{param}]'.format(param=param),
    ...                               has_container(allure_report,
    ...                                            has_before('attach_data_in_parametrized_fixture',
    ...                                                       has_attachment(attach_type='text/plain', name=param)
    ...                                            )
    ...                               )
    ...                 )
    ...     )
    """
    pass
