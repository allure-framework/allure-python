from six import string_types
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest import all_of, anything, any_of
from hamcrest import has_entry, has_item, has_property, equal_to


class HasContainer(BaseMatcher):

    def __init__(self, report, *matchers):
        self.report = report
        self.matchers = matchers

    def _matches(self, item):
        return has_property('test_containers',
                            has_item(
                                     all_of(
                                            has_entry('children', has_item(item['uuid'])),
                                            *self.matchers
                                     )
                            )).matches(self.report)

    def describe_to(self, description):
        description.append_text('describe me later').append_list('[', ', ', ']', self.matchers)

    def describe_mismatch(self, item, mismatch_descaription):
        self.matches(item, mismatch_descaription)


def has_container(report, *matchers):
    """
    >>> from hamcrest import assert_that

    >>> from allure_commons_test.report import has_test_case

    >>> class Report(object):
    ...     test_cases = [
    ...         {
    ...              'fullName': 'test_case',
    ...              'uuid': 'test_case_uuid'
    ...         },
    ...         {
    ...              'fullName': 'test_case_without_container',
    ...              'uuid': 'test_case_without_container_uuid'
    ...         }
    ...     ]
    ...     test_containers = [
    ...         {
    ...             'children' : ['test_case_uuid'],
    ...             'befores': [ {'name': 'before_fixture'} ]
    ...         }
    ...     ]

    >>> assert_that(Report,
    ...             has_test_case('test_case',
    ...                           has_container(Report,
    ...                                        has_before('before_fixture')
    ...                           )
    ...             )
    ... )

    >>> assert_that(Report,
    ...             has_test_case('test_case_without_container',
    ...                           has_container(Report,
    ...                                        has_before('before_fixture')
    ...                           )
    ...             )
    ... ) # doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    AssertionError: ...
    Expected: ...
         but: ...
    <BLANKLINE>
    """
    return HasContainer(report, *matchers)


class HasSameContainer(BaseMatcher):

    def __init__(self, *args):
        self.test_case_names = [test_case_name for test_case_name in args if isinstance(test_case_name, string_types)]
        self.matchers = args[len(self.test_case_names):]

    @staticmethod
    def _test_case_id_by_name(report, test_case_name):
        for test_case in report.test_cases:
            if test_case['fullName'].endswith(test_case_name):
                return test_case['uuid']

    def _matches(self, report):
        return has_property('test_containers',
                            has_item(
                                     all_of(
                                            has_entry('children',
                                                      all_of(
                                                             *[has_item(self._test_case_id_by_name(report, name))
                                                               for name in self.test_case_names]
                                                      )),
                                            *self.matchers
                                     )
                            )
               ).matches(report)

    # TODO better describe
    def describe_to(self, description):
        description.append_text('test_case has group')


def has_same_container(*args):
    """
    >>> from hamcrest import assert_that

    >>> class Report(object):
    ...     test_cases = [
    ...         {
    ...              'fullName': 'first_test_case',
    ...              'uuid': 'first_test_case_uuid'
    ...         },
    ...         {
    ...              'fullName': 'second_test_case',
    ...              'uuid': 'second_test_case_uuid'
    ...         },
    ...         {
    ...              'fullName': 'third_test_case',
    ...              'uuid': 'third_test_case_uuid'
    ...         }
    ...     ]
    ...     test_containers = [
    ...         {
    ...             'children' : ['first_test_case_uuid', 'second_test_case_uuid'],
    ...         },
    ...         {
    ...             'children' : ['first_test_case_uuid', 'third_test_case_uuid'],
    ...         }
    ...     ]

    >>> assert_that(Report,
    ...             has_same_container('first_test_case', 'second_test_case')
    ... )

    >>> assert_that(Report,
    ...             has_same_container('second_test_case', 'third_test_case')
    ... ) # doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    AssertionError: ...
    Expected: ...
         but: ...
    <BLANKLINE>
    """
    return HasSameContainer(*args)


def has_fixture(section, name, *matchers):
    return has_entry(section,
                     has_item(
                         all_of(
                             has_entry('name', equal_to(name)),
                             *matchers
                         )
                     ))


def has_before(name, *matchers):
    return has_fixture('befores', name, *matchers)


def has_after(name, *matchers):
    return has_fixture('afters', name, *matchers)