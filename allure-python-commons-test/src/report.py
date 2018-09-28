"""
>>> from hamcrest import assert_that

>>> class Report(object):
...     def __init__(self):
...         self.test_cases = [
...             {
...                 'fullName': 'package.module.test',
...                 'id': '1'
...             },
...             {
...                 'fullName': 'package.module.test[param]',
...                 'id': '2'
...             },
...             {
...                 'fullName': 'package.module.Class#test[param]',
...                 'id': '3'
...             }
...         ]


>>> assert_that(Report(),
...     has_test_case('test')
... )


>>> assert_that(Report(),
...     has_test_case('test[param]')
... )


>>> assert_that(Report(),
...     has_test_case('Class#test[param]')
... )


>>> assert_that(Report(),
...     has_test_case('wrong_test_case_name')
... ) # doctest: +ELLIPSIS
Traceback (most recent call last):
   ...
AssertionError: ...
Expected: ...
     but: property 'test_cases' was <[{...}]>
<BLANKLINE>


>>> assert_that(Report(),
...     has_test_case('test',
...         has_entry('id', '1')
...     )
... )


>>> assert_that(Report(),
...     has_test_case('Class#test[param]',
...         has_entry('id', '2')
...     )
... ) # doctest: +ELLIPSIS
Traceback (most recent call last):
   ...
AssertionError: ...
Expected: ...
     but: property 'test_cases' was <[{...}]>
<BLANKLINE>

"""

import sys
import os
import json
import fnmatch
from hamcrest import all_of, any_of
from hamcrest import has_property
from hamcrest import has_item
from hamcrest import has_entry
from hamcrest import ends_with, starts_with
from hamcrest.core.base_matcher import BaseMatcher

if sys.version_info[0] < 3:
    from io import open


class AllureReport(object):
    def __init__(self, result):
            self.result_dir = result
            self.test_cases = [json.load(item) for item in self._report_items(result, '*result.json')]
            self.test_containers = [json.load(item) for item in self._report_items(result, '*container.json')]
            self.attachments = [item.read() for item in self._report_items(result, '*attachment.*')]

    @staticmethod
    def _report_items(report_dir, glob):
        for _file in os.listdir(report_dir):
            if fnmatch.fnmatch(_file, glob):
                with open(os.path.join(report_dir, _file), encoding="utf-8") as report_file:
                    yield report_file


def has_test_case(name, *matchers):
    return has_property('test_cases',
                        has_item(
                                 all_of(
                                        any_of(
                                               has_entry('fullName', ends_with(name)),
                                               has_entry('name', starts_with(name))
                                               ),
                                        *matchers
                                        )
                                 )
                        )


class ContainsExactly(BaseMatcher):

    def __init__(self, num, matcher):
        self.matcher = matcher
        self.count = 0
        self.num = num

    def _matches(self, item):
        self.count = 0
        for subitem in item:
            if self.matcher.matches(subitem):
                self.count += 1

        if self.count == self.num:
            return True
        else:
            return False

    def describe_to(self, description):
        description.append_text('exactly {} item(s) matching '.format(self.num)).append_text(self.matcher)


def has_only_n_test_cases(name, num, *matchers):
    return has_property('test_cases',
                        ContainsExactly(num,
                                        all_of(
                                                any_of(
                                                        has_entry('fullName', ends_with(name)),
                                                        has_entry('name', ends_with(name))
                                                        ),
                                                *matchers
                                              )
                                        )
                        )

