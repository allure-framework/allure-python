"""
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
... )
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
... )
Traceback (most recent call last):
   ...
AssertionError: ...
Expected: ...
     but: property 'test_cases' was <[{...}]>
<BLANKLINE>

"""

from hamcrest import all_of
from hamcrest import has_item
from hamcrest import has_property
from hamcrest import has_entry
from hamcrest import ends_with


def has_test_case(name, *matchers):
    return has_property('test_cases',
                        has_item(
                                 all_of(has_entry('fullName', ends_with(name)),
                                        *matchers
                                        )
                                 )
                        )
