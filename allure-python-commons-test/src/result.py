"""
>>> from hamcrest import assert_that
>>> from hamcrest import is_not

>>> testcases = {
...     'ideal_case': {
...         'name': 'ideal_case',
...         'parentIds': ['gid-1', 'gid-2'],
...         'steps': [
...             {'name': 'step_one'}
...         ]
...     },
...     'like_ideal_case_by_group': {
...         'name': 'like_ideal_case_by_group',
...         'parentIds': ['gid-1', 'gid-2'],
...     },
...     'has_wrong_group_case': {
...         'name': 'anoher_case',
...         'parentIds': ['gid-1', 'gid-3'],
...     }
... }

>>> testgroups = {
...     'gid-1': {
...         'id': 'gid-1',
...         'befores': [
...             {'name': 'before_#1_gid1'},
...             {'name': 'before_#2_gid1'}
...         ]
...     },
...     'gid-2': {
...         'id': 'gid-2'
...     }
... }


>>> assert_that(testcases['ideal_case'], has_step('step_one'))


>>> assert_that(testcases['ideal_case'],
...                  has_step('ideal_case'),
...                  is_not(has_step('step_one'))
...             ) # doctest: +ELLIPSIS
Traceback (most recent call last):
    ...
AssertionError: ...
Expected: ...
     but: ...
<BLANKLINE>


>>> assert_that(testcases['ideal_case'],
...                 has_step('wrong_step_name')
...             ) # doctest: +ELLIPSIS
Traceback (most recent call last):
    ...
AssertionError: ...
Expected: ...
     but: ...
<BLANKLINE>


"""

from hamcrest import all_of, anything, not_, any_of
from hamcrest import equal_to, none, not_none
from hamcrest import has_entry, has_item
from hamcrest import contains_string
from hamcrest import contains_exactly
from allure_commons_test.lookup import maps_to


def has_title(title):
    return has_entry('name', title)


def has_title_path(*matchers):
    return has_entry(
        "titlePath",
        contains_exactly(*matchers),
    )


def has_description(*matchers):
    return has_entry('description', all_of(*matchers))


def has_description_html(*matchers):
    return has_entry('descriptionHtml', all_of(*matchers))


def has_step(name, *matchers):
    return has_entry(
        'steps',
        has_item(
            all_of(
                has_entry('name', equal_to(name)),
                *matchers
            )
        )
    )


def with_steps(*matchers):
    return has_entry(
        "steps",
        contains_exactly(*matchers),
    )


def get_parameter_matcher(name, *matchers):
    return has_entry(
        'parameters',
        has_item(
            all_of(
                has_entry('name', equal_to(name)),
                *matchers
            )
        )
    )


def has_parameter(name, value, *matchers):
    return get_parameter_matcher(
        name,
        has_entry('value', equal_to(value)),
        *matchers
    )


def doesnt_have_parameter(name):
    return not_(
        has_entry(
            "parameters",
            has_item(
                has_entry("name", name),
            ),
        ),
    )


def resolve_link_attr_matcher(key, value):
    return has_entry(key, value) if value is not None else any_of(
        not_(has_entry(key)),
        none(),
    )


def has_link(url, link_type=None, name=None):
    return has_entry(
        'links',
        has_item(
            all_of(
                *[
                    resolve_link_attr_matcher(key, value) for key, value in zip(
                        ('url', 'type', 'name'),
                        (url, link_type, name)
                    ) if value is not None
                ]
            )
        )
    )


def has_issue_link(url, name=None):
    return has_link(url, link_type='issue', name=name)


def has_test_case_link(url, name=None):
    return has_link(url, link_type='tms', name=name)


def has_attachment(attach_type=None, name=None):
    return has_entry(
        'attachments',
        has_item(
            all_of(
                has_entry('source', anything()),
                has_entry('type', attach_type) if attach_type else anything(),
                has_entry('name', name) if name else anything()
            )
        )
    )


def has_attachment_with_content(
    attachments,
    content_matcher,
    attach_type=None,
    name=None
):
    return has_entry(
        'attachments',
        has_item(
            all_of(
                has_entry('name', name) if name else anything(),
                has_entry('type', attach_type) if attach_type else anything(),
                has_entry('source', maps_to(attachments, content_matcher))
            )
        )
    )


def with_id():
    return has_entry('uuid', not_none())


def with_status(status):
    return has_entry('status', status)


def has_status_details(*matchers):
    return has_entry('statusDetails', all_of(*matchers))


def with_message_contains(string):
    return has_entry('message', contains_string(string))


def with_trace_contains(string):
    return has_entry('trace', contains_string(string))


def with_excluded():
    return has_entry('excluded', True)


def with_mode(mode):
    return has_entry('mode', mode)


def has_history_id(matcher=None):
    return has_entry('historyId', matcher or anything())


def has_test_case_id(matcher=None):
    return has_entry('testCaseId', matcher or anything())


def has_full_name(matcher):
    return has_entry("fullName", matcher)
