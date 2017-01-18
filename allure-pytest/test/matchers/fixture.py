from hamcrest import all_of
from hamcrest import equal_to
from hamcrest import has_entry, has_item


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
