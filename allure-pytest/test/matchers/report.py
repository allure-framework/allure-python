"""
>>> from hamcrest import assert_that

>>> class Report(object):
...     def __init__(self):
...         self.test_cases = [
...             {
...                 'name':'test_case_name',
...                 'id': '1'
...             }
...         ]


>>> assert_that(Report(),
...     has_test_case('test_case_name')
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
...     has_test_case('test_case_name',
...         has_entry('id', '1')
...     )
... )


>>> assert_that(Report(),
...     has_test_case('test_case_name',
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


def has_test_case(name, *matchers):
    return has_property('test_cases',
                        has_item(
                            all_of(has_entry('name', name), *matchers)
                        ))
