"""
>>> allure_report = getfixture('allure_report')
>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(7)),
...                 has_property('test_groups', has_length(0))
...             ))
"""

import pytest

XML = '''body {
    background-color: lightblue;
}
'''
NAME = 'attach name'


def test_attach_from_test(xml):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_from_test',
    ...                           has_attachment('application/xml')
    ...             ))
    """
    pytest.allure.attach.xml(xml)


def test_named_attach_from_test(xml):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_named_attach_from_test',
    ...                           has_attachment('application/xml', name=NAME)
    ...             ))
    """
    pytest.allure.attach.xml(xml, name="attach name")


def attach_svg(svg):
    pytest.allure.attach.svg(svg)


def test_attach_from_function(svg):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_from_function',
    ...                           has_attachment('image/svg-xml')
    ...             ))
    """
    attach_svg(svg)


def test_many_attaches(svg, xml):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_many_attaches',
    ...                           all_of(has_attachment('application/xml'),
    ...                                  has_attachment('image/svg-xml')
    ...                           )
    ...             ))
    """
    attach_svg(svg)
    pytest.allure.attach.xml(xml)


def test_attach_from_step(svg):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_from_step',
    ...                           has_step('Step with attachment',
    ...                                     has_attachment('image/svg-xml')
    ...                            )
    ...             ))
    """
    with pytest.allure.step('Step with attachment'):
        pytest.allure.attach.svg(svg)


def test_attach_user_type(tmpdir):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_user_type',
    ...                           has_attachment('text/css')
    ...             ))
    """
    _file = tmpdir.join('test.wtf')
    _file.write(XML)
    pytest.allure.attach(_file.strpath, 'text/css', 'css')


def test_named_attach_user_type(tmpdir):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_named_attach_user_type',
    ...                           has_attachment('text/css', name=NAME)
    ...             ))
    """
    _file = tmpdir.join('another_test.wtf')
    _file.write(XML)
    pytest.allure.attach(_file.strpath, 'text/css', 'css', name=NAME)
