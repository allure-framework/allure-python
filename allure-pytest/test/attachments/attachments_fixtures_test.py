import pytest
import allure

TEXT = "attachment body"


@pytest.fixture
def attach_file_in_function_scope_fixture(svg_file):
    allure.attach.file(svg_file, attachment_type=allure.attachment_type.SVG)


def test_attach_file_in_function_scope_fixture(attach_file_in_function_scope_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_file_in_function_scope_fixture',
    ...                           has_container(allure_report,
    ...                                         has_before('attach_file_in_function_scope_fixture',
    ...                                                     has_attachment(attach_type='image/svg-xml')
    ...                                         )
    ...                           )
    ...             )
    ... )
    """
    pass


def test_attach_file_in_reused_function_scope_fixture(attach_file_in_function_scope_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_file_in_reused_function_scope_fixture',
    ...                           has_container(allure_report,
    ...                                         has_before('attach_file_in_function_scope_fixture',
    ...                                                    has_attachment(attach_type='image/svg-xml')
    ...                                         )
    ...                           )
    ...             )
    ... )
    """
    pass


@pytest.fixture
def attach_file_in_function_scope_finalizer(svg_file, request):
    def finalizer_function_scope_fixture():
        allure.attach.file(svg_file, attachment_type=allure.attachment_type.SVG)
    request.addfinalizer(finalizer_function_scope_fixture)


def test_attach_file_in_function_scope_finalizer(attach_file_in_function_scope_finalizer):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_file_in_function_scope_finalizer',
    ...                           has_container(allure_report,
    ...                                         has_after('attach_file_in_function_scope_finalizer::finalizer_function_scope_fixture',
    ...                                                   has_attachment(attach_type='image/svg-xml')
    ...                                         )
    ...                           )
    ...             )
    ... )
    """
    pass


def test_attach_file_in_reused_function_scope_finalizer(attach_file_in_function_scope_finalizer):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_file_in_reused_function_scope_finalizer',
    ...                           has_container(allure_report,
    ...                                         has_after('attach_file_in_function_scope_finalizer::finalizer_function_scope_fixture',
    ...                                                   has_attachment(attach_type='image/svg-xml')
    ...                                          )
    ...                           )
    ...             )
    ... )
    """
    pass


@pytest.fixture(scope='module')
def attach_data_in_module_scope_fixture():
    allure.attach(TEXT, attachment_type='text/plain')


def test_attach_data_in_module_scope_fixture(attach_data_in_module_scope_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_data_in_module_scope_fixture',
    ...                           has_container(allure_report,
    ...                                        has_before('attach_data_in_module_scope_fixture',
    ...                                                   has_attachment(attach_type='text/plain')
    ...                                        )
    ...                           )
    ...             )
    ... )
    """
    pass


def test_attach_data_in_reused_module_scope_fixture(attach_data_in_module_scope_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_data_in_reused_module_scope_fixture',
    ...                           has_container(allure_report,
    ...                                        has_before('attach_data_in_module_scope_fixture',
    ...                                                   has_attachment(attach_type='text/plain')
    ...                                        )
    ...                           )
    ...             )
    ... )
    """
    pass


@pytest.fixture(scope='module')
def attach_data_in_module_scope_finalizer(request):
    def finalizer_module_scope_fixture():
        allure.attach(TEXT, attachment_type='text/plain')
    request.addfinalizer(finalizer_module_scope_fixture)


def test_attach_data_in_module_scope_finalizer(attach_data_in_module_scope_finalizer):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_data_in_module_scope_finalizer',
    ...                           has_container(allure_report,
    ...                                        has_after('{fixture}::{finalizer}'.format(
    ...                                                                    fixture='attach_data_in_module_scope_finalizer',
    ...                                                                    finalizer='finalizer_module_scope_fixture'),
    ...                                                   has_attachment(attach_type='text/plain')
    ...                                        )
    ...                           )
    ...             )
    ... )
    """
    pass


def test_attach_data_in_reused_module_scope_finalizer(attach_data_in_module_scope_finalizer):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_data_in_reused_module_scope_finalizer',
    ...                           has_container(allure_report,
    ...                                        has_after('{fixture}::{finalizer}'.format(
    ...                                                                    fixture='attach_data_in_module_scope_finalizer',
    ...                                                                    finalizer='finalizer_module_scope_fixture'),
    ...                                                   has_attachment(attach_type='text/plain')
    ...                                        )
    ...                           )
    ...             )
    ... )
    """
    pass
