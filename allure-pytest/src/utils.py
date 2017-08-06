# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from allure_commons.utils import represent

ALLURE_UNIQUE_LABELS = ['severity', 'thread', 'host']
ALLURE_LABEL_PREFIX = 'allure_label'
ALLURE_LINK_PREFIX = 'allure_link'


def allure_labels(item):
    for keyword in item.keywords.keys():
        if keyword.startswith(ALLURE_LABEL_PREFIX):
            marker = item.get_marker(keyword)
            label_type = marker.kwargs['label_type']
            if label_type in ALLURE_UNIQUE_LABELS:
                yield (label_type, marker.args[0])
            else:
                for value in marker.args:
                    yield (label_type, value)


def allure_links(item):
    for keyword in item.keywords.keys():
        if keyword.startswith(ALLURE_LINK_PREFIX):
            marker = item.get_marker(keyword)
            link_type = marker.kwargs['link_type']
            url = marker.args[0]
            name = marker.kwargs['name']
            yield (link_type, url, name)


def pytest_markers(item):
    for keyword in item.keywords.keys():
        if not any((keyword.startswith(ALLURE_LINK_PREFIX),
                    keyword.startswith(ALLURE_LABEL_PREFIX),
                    keyword == 'parametrize')):
            marker = item.get_marker(keyword)
            if marker:
                yield mark_to_str(marker)


def mark_to_str(marker):
    args = [represent(arg) for arg in marker.args]
    kwargs = ['{name}={value}'.format(name=key, value=represent(marker.kwargs[key])) for key in marker.kwargs]
    if args or kwargs:
        parameters = ', '.join(args + kwargs)
        return '@pytest.mark.{name}({parameters})'.format(name=marker.name, parameters=parameters)
    else:
        return '@pytest.mark.{name}'.format(name=marker.name)


def allure_package(nodeid):
    parts = nodeid.split('::')
    path = parts[0].split('.')[0]
    return path.replace(os.sep, '.')


def allure_full_name(nodeid):
    parts = nodeid.split('::')
    package = allure_package(nodeid)
    clazz = '.{clazz}'.format(clazz=parts[1]) if len(parts) > 2 else ''
    test = parts[-1]
    return '{package}{clazz}#{test}'.format(package=package, clazz=clazz, test=test)
