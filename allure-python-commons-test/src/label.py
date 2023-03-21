from hamcrest import all_of
from hamcrest import has_entry, has_item


def has_label(name, value):
    return has_entry('labels',
                     has_item(
                         all_of(
                             has_entry('name', name),
                             has_entry('value', value)
                         )
                     ))


def has_severity(level):
    return has_label('severity', level)


def has_epic(feature):
    return has_label('epic', feature)


def has_feature(feature):
    return has_label('feature', feature)


def has_story(story):
    return has_label('story', story)


def has_tag(tag):
    return has_label('tag', tag)


def has_package(package):
    return has_label('package', package)


def has_suite(suite):
    return has_label('suite', suite)


def has_parent_suite(parent_suite):
    return has_label('parentSuite', parent_suite)


def has_sub_suite(sub_suite):
    return has_label('subSuite', sub_suite)
