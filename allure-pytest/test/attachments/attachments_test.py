"""
>>> allure_report = getfixture('allure_report')
>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(9)),
...                 has_property('test_groups', has_length(0)),
...                 has_property('attachments', has_length(11))
...             ))
"""

import pytest


def test_attach_file_from_test(xml_file):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_file_from_test',
    ...                           has_attachment()
    ...             )
    ... )
    """
    pytest.allure.attach.file(xml_file)


def test_attach_data_from_test(xml_body):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_data_from_test',
    ...                           has_attachment()
    ...             )
    ... )
    """
    pytest.allure.attach(xml_body)


def test_attach_file_from_test_with_name_and_type(xml_file):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_file_from_test_with_name_and_type',
    ...                           has_attachment(attach_type='application/xml', name='my name')
    ...             ))
    """
    pytest.allure.attach.file(xml_file, name='my name', attachment_type=pytest.allure.attachment_type.XML)


def test_attach_data_from_test_with_name_and_type(xml_body):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_data_from_test_with_name_and_type',
    ...                           has_attachment(attach_type='application/xml', name='my name')
    ...             ))
    """
    pytest.allure.attach(xml_body, name='my name', attachment_type=pytest.allure.attachment_type.XML)


def test_attach_file_from_test_with_user_type(xml_file):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_file_from_test_with_user_type',
    ...                           has_attachment(attach_type='text/xml')
    ...             ))
    """
    pytest.allure.attach.file(xml_file, attachment_type='text/xml')


def test_attach_data_from_test_with_user_type(xml_body):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_data_from_test_with_user_type',
    ...                           has_attachment(attach_type='text/xml')
    ...             ))
    """
    pytest.allure.attach(xml_body, attachment_type='text/xml')


def attach_svg_file(svg_file):
    pytest.allure.attach.file(svg_file, attachment_type=pytest.allure.attachment_type.SVG)


def test_attach_file_from_function(svg_file):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_file_from_function',
    ...                           has_attachment('image/svg-xml')
    ...             ))
    """
    attach_svg_file(svg_file)


def test_many_attaches(svg_file, xml_body):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_many_attaches',
    ...                           all_of(has_attachment('application/xml'),
    ...                                  has_attachment('image/svg-xml')
    ...                           )
    ...             ))
    """
    attach_svg_file(svg_file)
    pytest.allure.attach(xml_body, attachment_type=pytest.allure.attachment_type.XML)


def test_attach_from_step(svg_file, xml_body):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_from_step',
    ...                           has_step('Step with attachment',
    ...                                    all_of(has_attachment('image/svg-xml'),
    ...                                           has_step('Nested step with attachment',
    ...                                                    has_attachment('application/xml')
    ...                                           )
    ...                                    )
    ...                            )
    ...             )
    ... )
    """
    with pytest.allure.step('Step with attachment'):
        pytest.allure.attach.file(svg_file, attachment_type=pytest.allure.attachment_type.SVG)
        with pytest.allure.step('Nested step with attachment'):
            pytest.allure.attach(xml_body, attachment_type=pytest.allure.attachment_type.XML)
