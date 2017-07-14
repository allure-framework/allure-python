# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from itertools import product
from allure_commons.utils import represent

ALLURE_UNIQUE_LABELS = ['severity', 'thread', 'host']
ALLURE_LABEL_PREFIX = 'allure_label'
ALLURE_LINK_PREFIX = 'allure_link'


def allure_parameters(fixturedef, request):
    parameters = {}
    param_name = request.fixturename

    if hasattr(request, 'param'):
        parameters = {'name': fixturedef.ids[request.param_index] if fixturedef.ids else param_name,
                      'value': str(request.param)}

    if 'parametrize' in request.node.keywords.keys():
        param_map = list()
        for mark_info in request.node.keywords['parametrize']:

            _ids = mark_info.kwargs['ids'] if 'ids' in mark_info.kwargs.keys() else None
            _args = mark_info.args[0]
            if not isinstance(_args, (tuple, list)):
                _args = [x.strip() for x in _args.split(",") if x.strip()]

            param_map.append({'args': _args,
                              'has_ids': _ids is not None,
                              'ids': _ids if _ids else mark_info.args[1],
                              'values': list()})

        for variant in product(*[item['ids'] for item in param_map]):
            for i, item in enumerate(param_map):
                item['values'].append(variant[i])

        for item in param_map:
            if param_name in item['args'] and item['has_ids']:
                ids = item['values'][request.param_index]
                if len(item['args']) == 1:
                    parameters = {'name': ids, 'value': str(request.param)}
                else:
                    param_name = '{ids}::{param}'.format(ids=ids, param=param_name)
                    parameters = {'name': param_name, 'value': str(request.param)}

    return parameters


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
