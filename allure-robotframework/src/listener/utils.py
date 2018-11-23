from __future__ import absolute_import
from allure_commons.model2 import Status, Label, Parameter
from allure_commons.types import LabelType
from allure_robotframework.types import RobotStatus


def get_allure_status(status):
    return Status.PASSED if status == RobotStatus.PASSED else Status.FAILED


def get_allure_parameters(parameters):
    return [Parameter(name="arg{}".format(i + 1), value=param) for i, param in enumerate(parameters)]


def get_allure_suites(longname):
    """
    >>> get_allure_suites('Suite1.Test')
    [Label(name=<LabelType.SUITE: 'suite'>, value='Suite1')]
    >>> get_allure_suites('Suite1.Suite2.Test') # doctest: +NORMALIZE_WHITESPACE
    [Label(name=<LabelType.SUITE: 'suite'>, value='Suite1'),
    Label(name=<LabelType.SUB_SUITE: 'subSuite'>, value='Suite2')]
    >>> get_allure_suites('Suite1.Suite2.Suite3.Test') # doctest: +NORMALIZE_WHITESPACE
    [Label(name=<LabelType.PARENT_SUITE: 'parentSuite'>, value='Suite1'),
    Label(name=<LabelType.SUITE: 'suite'>, value='Suite2'),
    Label(name=<LabelType.SUB_SUITE: 'subSuite'>, value='Suite3')]
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
    return [Label(LabelType.TAG, tag) for tag in attributes.get('tags', ())]


def allure_labels(attributes, prefix):
    tags = attributes.get('tags', ())

    def is_label(label):
        return label.startswith("{label}:".format(label=prefix))

    def label_value(label):
        return label.split(':')[1] or 'unknown'

    return [Label(name=prefix, value=label_value(tag)) for tag in tags if is_label(tag)]
