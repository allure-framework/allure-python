from __future__ import absolute_import
from re import search
from allure_commons.model2 import Status, Label, Parameter, Link
from allure_commons.types import LabelType
from allure_robotframework.types import RobotStatus
from allure_commons.mapping import parse_tag, labels_set, allure_tag_sep


def get_allure_status(status):
    if status == RobotStatus.PASSED:
        return Status.PASSED
    elif status == RobotStatus.SKIPPED:
        return Status.SKIPPED
    else:
        return Status.FAILED


def get_allure_parameters(parameters):
    return [Parameter(name="arg{}".format(i + 1), value=param) for i, param in enumerate(parameters)]


def get_allure_suites(longname):
    """
    >>> get_allure_suites('Suite1.Test')
    [Label(name='suite', value='Suite1')]
    >>> get_allure_suites('Suite1.Suite2.Test') # doctest: +NORMALIZE_WHITESPACE
    [Label(name='suite', value='Suite1'), Label(name='subSuite', value='Suite2')]
    >>> get_allure_suites('Suite1.Suite2.Suite3.Test') # doctest: +NORMALIZE_WHITESPACE
    [Label(name='parentSuite', value='Suite1'),
    Label(name='suite', value='Suite2'),
    Label(name='subSuite', value='Suite3')]
    """
    labels = []
    suites = longname.split('.')
    if len(suites) > 3:
        labels.append(Label(LabelType.PARENT_SUITE, suites.pop(0)))
    labels.append(Label(LabelType.SUITE, suites.pop(0)))
    if len(suites) > 1:
        labels.append(Label(LabelType.SUB_SUITE, '.'.join(suites[:-1])))
    return labels


def allure_tags(attributes):
    return [Label(LabelType.TAG, tag) for tag in attributes.get('tags', ()) if not allure_tag_sep(tag)]


def allure_labels(tags):
    parsed = [parse_tag(item) for item in tags]
    return labels_set(list(filter(lambda x: isinstance(x, Label),  parsed)))


def allure_links(attributes, prefix):
    tags = attributes.get('tags', ())

    def is_link(link):
        return link.startswith("{link}:".format(link=prefix))

    def parse_link(link):
        lnk_val = link.split(':', 1)[1] or 'unknown'
        lnk_label = search(r'\[.+\]', lnk_val)
        if lnk_label:
            lnk_label = lnk_label.group(0)
            lnk_val = lnk_val.strip(lnk_label)
            lnk_label = lnk_label.strip('[]')
        else:
            lnk_label = lnk_val

        return {'name': lnk_label, 'value': lnk_val}

    return [Link(type=prefix, url=parse_link(tag).get('value'), name=parse_link(tag).get('name')) for tag in tags if
            is_link(tag)]
