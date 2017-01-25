"""
>>> allure_report = getfixture('allure_report')
>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(8)),
...                 has_property('test_groups', has_length(2))
...             ))
"""

import pytest
import tempfile
from six import text_type

TEXT = "TEXT ATTACH"


@pytest.fixture
def attach_in_function_scope_fixture(svg):
    pytest.allure.attach.svg(svg)


def test_attach_in_function_scope_fixture(attach_in_function_scope_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_in_function_scope_fixture',
    ...                           has_before('attach_in_function_scope_fixture',
    ...                                      has_attachment('image/svg-xml')
    ...                           )
    ...             ))
    """
    pass


def test_attach_in_reused_function_scope_fixture(attach_in_function_scope_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_in_reused_function_scope_fixture',
    ...                           has_before('attach_in_function_scope_fixture',
    ...                                      has_attachment('image/svg-xml')
    ...                           )
    ...             ))
    """
    pass


@pytest.fixture
def attach_in_function_scope_finalizer(svg, request):
    def finalizer_function_scope_fixture():
        pytest.allure.attach.svg(svg)
    request.addfinalizer(finalizer_function_scope_fixture)


def test_attach_in_function_scope_finalizer(attach_in_function_scope_finalizer):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_in_function_scope_finalizer',
    ...                           has_after('attach_in_function_scope_finalizer::finalizer_function_scope_fixture',
    ...                                     has_attachment('image/svg-xml')
    ...                           )
    ...             ))
    """
    pass


def test_attach_in_reused_function_scope_finalizer(attach_in_function_scope_finalizer):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_in_reused_function_scope_finalizer',
    ...                           has_after('attach_in_function_scope_finalizer::finalizer_function_scope_fixture',
    ...                                     has_attachment('image/svg-xml')
    ...                           )
    ...             ))
    """
    pass

from six import u
def create_txt_attach(text):
    f = tempfile.NamedTemporaryFile(delete=False)
    if isinstance(text, text_type):
        f.write(text.encode('utf-8'))
    else:
        f.write(text)
    f.close()
    return f.name


@pytest.fixture(scope='module')
def attach_in_module_scope_fixture():
    pytest.allure.attach.txt(create_txt_attach(TEXT))


def test_attach_in_module_scope_fixture(attach_in_module_scope_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_in_module_scope_fixture',
    ...                           has_group_in(allure_report.test_groups,
    ...                                        has_before('attach_in_module_scope_fixture',
    ...                                                   has_attachment('text/plain')
    ...                                        ))
    ...             ))
    """
    pass


def test_attach_in_reuse_module_scope_fixture(attach_in_module_scope_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_in_reuse_module_scope_fixture',
    ...                           has_group_in(allure_report.test_groups,
    ...                                        has_before('attach_in_module_scope_fixture',
    ...                                                   has_attachment('text/plain')
    ...                                        ))
    ...             ))
    """
    pass


@pytest.fixture(scope='module')
def attach_in_module_scope_finalizer(request):
    def finalizer_module_scope_fixture():
        pytest.allure.attach.txt(create_txt_attach(TEXT))
    request.addfinalizer(finalizer_module_scope_fixture)


def test_attach_in_module_scope_finalizer(attach_in_module_scope_finalizer):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_in_module_scope_finalizer',
    ...                           has_group_in(allure_report.test_groups,
    ...                                        has_after('{fixture}::{finalizer}'.format(
    ...                                                                    fixture='attach_in_module_scope_finalizer',
    ...                                                                    finalizer='finalizer_module_scope_fixture'),
    ...                                                   has_attachment('text/plain')
    ...                                        ))
    ...             ))
    """
    pass


def test_attach_in_reuse_module_scope_finalizer(attach_in_module_scope_finalizer):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_in_reuse_module_scope_finalizer',
    ...                           has_group_in(allure_report.test_groups,
    ...                                        has_after('{fixture}::{finalizer}'.format(
    ...                                                                    fixture='attach_in_module_scope_finalizer',
    ...                                                                    finalizer='finalizer_module_scope_fixture'),
    ...                                                   has_attachment('text/plain')
    ...                                        ))
    ...             ))
    """
    pass
