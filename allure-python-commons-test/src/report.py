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

import os
import json
import fnmatch
from hamcrest import all_of, any_of
from hamcrest import has_property
from hamcrest import has_item
from hamcrest import has_entry
from hamcrest import ends_with


class AllureReport(object):
    def __init__(self, result):
            self.test_cases = [json.load(item) for item in self._report_items(result, '*result.json')]
            self.test_containers = [json.load(item) for item in self._report_items(result, '*container.json')]
            self.attachments = [item.read() for item in self._report_items(result, '*attachment.*')]

    @staticmethod
    def _report_items(report_dir, glob):
        for _file in os.listdir(report_dir):
            if fnmatch.fnmatch(_file, glob):
                with open(os.path.join(report_dir, _file)) as report_file:
                    yield report_file


def has_test_case(name, *matchers):
    return has_property('test_cases',
                        has_item(
                                 all_of(
                                        any_of(
                                               has_entry('fullName', ends_with(name)),
                                               has_entry('name', ends_with(name))
                                               ),
                                        *matchers
                                        )
                                 )
                        )
