import os
import sys
import inspect
from itertools import product

from allure.types import ALLURE_UNIQUE_LABELS

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
            if label_type.value in ALLURE_UNIQUE_LABELS:
                yield (label_type.value, marker.args[0])
            else:
                for value in marker.args:
                    yield (label_type.value, value)


def allure_links(item):
    for keyword in item.keywords.keys():
        if keyword.startswith(ALLURE_LINK_PREFIX):
            marker = item.get_marker(keyword)
            link_type = marker.name.split('.', 1)[-1]
            url = marker.args[0]
            name = marker.kwargs['name']
            yield (link_type, url, name)


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


def step_parameters(func, *a, **kw):
    if sys.version_info.major < 3:
        all_names = inspect.getargspec(func).args
        defaults = inspect.getargspec(func).defaults
    else:
        all_names = inspect.getfullargspec(func).args
        defaults = inspect.getfullargspec(func).defaults
    args_part = [(n, str(v)) for n, v in zip(all_names, a)]
    kwarg_part = [(n, str(kw[n]) if n in kw else str(defaults[i])) for i, n in enumerate(all_names[len(a):])]
    return args_part + kwarg_part
