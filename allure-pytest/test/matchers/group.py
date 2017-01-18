"""
>>> from hamcrest import assert_that, is_not
>>> from report import has_test_case
>>> from fixture import has_before

>>> class Report(object):
...     def __init__(self):
...         self.test_cases = [
...                 {
...                     'name': 'ideal_case',
...                     'parentIds': ['gid-1', 'gid-2'],
...                     'steps': [
...                         {'name': 'step_one'}
...                     ]
...                 },
...                 {
...                     'name': 'like_ideal_case_by_group',
...                     'parentIds': ['gid-1', 'gid-2'],
...                 },
...                 {
...                     'name': 'has_wrong_group_case',
...                     'parentIds': ['gid-1', 'gid-2', 'gid-3'],
...                 }
...         ]
...
...         self.test_groups = [
...                 {
...                     'id': 'gid-1',
...                     'befores': [
...                         {'name': 'before_#1_gid1'},
...                         {'name': 'before_#2_gid1'}
...                     ]
...                 },
...                 {
...                     'id': 'gid-2'
...                 }
...         ]

>>> report = Report()

EACH TEST CASE GROUP IN GROUPS +

>>> assert_that(report,
...             has_test_case('ideal_case',
...                 has_each_group_in(report.test_groups)
...             ))


EACH TEST CASE GROUP IN GROUPS -
>>> assert_that(report,
...             has_test_case('has_wrong_group_case',
...                 has_each_group_in(report.test_groups)
...             ))
Traceback (most recent call last):
    ...
AssertionError: ...
Expected: an object with a property 'test_cases' ... containing ['name': 'has_wrong_group_case'] ...
     but: property 'test_cases' was <[{...}]>
<BLANKLINE>


HAS GROUP IN +
>>> assert_that(report,
...             has_test_case('ideal_case',
...                           has_group_in(report.test_groups,
...                               has_before('before_#1_gid1')
...                           )
...             ))


HAS GROUP IN ++
>>> assert_that(report,
...             has_test_case('ideal_case',
...                           has_group_in(report.test_groups,
...                               has_before('before_#1_gid1'),
...                                has_before('before_#2_gid1')
...                           )
...             ))


HAS GROUP IN -
>>> assert_that(report,
...             has_test_case('ideal_case',
...                           has_group_in(report.test_groups,
...                               has_before('before_#3_gid1')
...                           )
...             ))
Traceback (most recent call last):
   ...
AssertionError: ...
Expected: ...
     but: property 'test_cases' was ...
<BLANKLINE>


HAS GROUP IN --
>>> assert_that(report,
...             has_test_case('ideal_case',
...                           has_group_in(report.test_groups,
...                               has_before('before_#1_gid1'),
...                               has_before('before_#3_gid1')
...                           )
...             ))
Traceback (most recent call last):
   ...
AssertionError: ...
Expected: ...
     but: property 'test_cases' was ...
<BLANKLINE>


HAS EQUAL GROUPS WITH +
>>> assert_that(report,
...             has_equal_groups('ideal_case', 'like_ideal_case_by_group')
...             )


HAS EQUAL GROUPS WITH -
>>> assert_that(report,
...             has_equal_groups('ideal_case', 'has_wrong_group_case')
...             )
Traceback (most recent call last):
   ...
AssertionError: ...
Expected: ...
     but: ...
<BLANKLINE>


HAS EQUAL GROUPS WITH --
>>> assert_that(report,
...             has_equal_groups('has_wrong_group_case', 'ideal_case')
...             )
Traceback (most recent call last):
   ...
AssertionError: ...
Expected: ...
     but: ...
<BLANKLINE>


HAS EQUAL GROUPS WITH ++
>>> assert_that(report,
...             is_not(has_equal_groups('has_wrong_group_case', 'ideal_case'))
...             )
"""


from hamcrest import all_of
from hamcrest import equal_to, not_none, empty, is_not
from hamcrest import has_entry, has_item
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest import any_of


class HasEachGroupInReport(BaseMatcher):

    def __init__(self, groups):
        self.groups = groups

    def _matches(self, item):
        return all_of(
            has_entry('parentIds',
                      all_of(
                          not_none(),
                          is_not(empty()),
                      ))
        ).matches(item) and all_of(
            *[has_item(
                has_entry('id', equal_to(key))) for key in item['parentIds']]).matches(self.groups)

    # TODO better describe
    def describe_to(self, description):
        description.append_text('test_case has group')


def has_each_group_in(groups):
    return HasEachGroupInReport(groups)


class HasGroupInGroups(BaseMatcher):

    def __init__(self, groups, *matchers):
        self.groups = groups
        self.matchers = matchers

    def _matches(self, item):
        return any_of(
            *[has_item(
                all_of(
                    has_entry('id', pid),
                    *self.matchers
                )
            ) for pid in item['parentIds']]
        ).matches(self.groups)

    def describe_to(self, description):
        description.append_text('test_case has group')


def has_group_in(groups, *matchers):
    return HasGroupInGroups(groups, *matchers)


class HasSameGroups(BaseMatcher):

    def __init__(self, left_test_case_name, right_test_case_name):
        self.left_test_case = left_test_case_name
        self.right_test_case = right_test_case_name

    def _test_case_by_name(self, report, test_case_name):
        for test_case in report.test_cases:
            if test_case['name'] == test_case_name:
                return test_case['parentIds']

    def _matches(self, report):
        return equal_to(
            self._test_case_by_name(report,
                                    self.left_test_case)
        ).matches(self._test_case_by_name(report,
                                          self.right_test_case))

    # TODO better describe
    def describe_to(self, description):
        description.append_text('test_case has group')


# TODO make in easy
def has_equal_groups(left_test_case_name, right_test_case_name):
    return HasSameGroups(left_test_case_name, right_test_case_name)
