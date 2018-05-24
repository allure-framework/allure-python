import argparse

import allure
import allure_commons

from allure_commons.types import LabelType
from allure_commons.logger import AllureFileLogger

from allure_pytest.utils import allure_labels
from allure_pytest.helper import AllureTestHelper
from allure_pytest.listener import AllureListener


def pytest_addoption(parser):
    parser.getgroup("reporting").addoption('--alluredir',
                                           action="store",
                                           dest="allure_report_dir",
                                           metavar="DIR",
                                           default=None,
                                           help="Generate Allure report in the specified directory (may not exist)")

    parser.getgroup("reporting").addoption('--clean-alluredir',
                                           action="store_true",
                                           dest="clean_alluredir",
                                           help="Clean alluredir folder if it exists")

    def label_type(type_name, legal_values=set()):
        def a_label_type(string):
            atoms = set(string.split(','))
            if type_name is LabelType.SEVERITY:
                if not atoms < legal_values:
                    raise argparse.ArgumentTypeError('Illegal {} values: {}, only [{}] are allowed'.format(
                        type_name, ', '.join(atoms - legal_values), ', '.join(legal_values)))
                return set((type_name, allure.severity_level(atom)) for atom in atoms)
            return set((type_name, atom) for atom in atoms)
        return a_label_type

    severities = [x.value for x in list(allure.severity_level)]
    parser.getgroup("general").addoption('--allure-severities',
                                         action="store",
                                         dest="allure_severities",
                                         metavar="SEVERITIES_SET",
                                         default={},
                                         type=label_type(LabelType.SEVERITY, legal_values=set(severities)),
                                         help="""Comma-separated list of severity names.
                                         Tests only with these severities will be run.
                                         Possible values are: %s.""" % ', '.join(severities))

    parser.getgroup("general").addoption('--allure-epics',
                                         action="store",
                                         dest="allure_epics",
                                         metavar="EPICS_SET",
                                         default={},
                                         type=label_type(LabelType.EPIC),
                                         help="""Comma-separated list of epic names.
                                         Run tests that have at least one of the specified feature labels.""")

    parser.getgroup("general").addoption('--allure-features',
                                         action="store",
                                         dest="allure_features",
                                         metavar="FEATURES_SET",
                                         default={},
                                         type=label_type(LabelType.FEATURE),
                                         help="""Comma-separated list of feature names.
                                         Run tests that have at least one of the specified feature labels.""")

    parser.getgroup("general").addoption('--allure-stories',
                                         action="store",
                                         dest="allure_stories",
                                         metavar="STORIES_SET",
                                         default={},
                                         type=label_type(LabelType.STORY),
                                         help="""Comma-separated list of story names.
                                         Run tests that have at least one of the specified story labels.""")

    def link_pattern(string):
        pattern = string.split(':', 1)
        if not pattern[0]:
            raise argparse.ArgumentTypeError('Link type is mandatory.')

        if len(pattern) != 2:
            raise argparse.ArgumentTypeError('Link pattern is mandatory')
        return pattern

    parser.getgroup("general").addoption('--allure-link-pattern',
                                         action="append",
                                         dest="allure_link_pattern",
                                         metavar="LINK_TYPE:LINK_PATTERN",
                                         default=[],
                                         type=link_pattern,
                                         help="""Url pattern for link type. Allows short links in test,
                                         like 'issue-1'. Text will be formatted to full url with python
                                         str.format().""")


def cleanup_factory(plugin):
    def clean_up():
        name = allure_commons.plugin_manager.get_name(plugin)
        allure_commons.plugin_manager.unregister(name=name)
    return clean_up


def pytest_configure(config):
    report_dir = config.option.allure_report_dir
    clean = config.option.clean_alluredir

    test_helper = AllureTestHelper(config)
    # TODO: Why helper is present anyway?
    allure_commons.plugin_manager.register(test_helper)
    config.add_cleanup(cleanup_factory(test_helper))

    if report_dir:
        test_listener = AllureListener(config)
        config.pluginmanager.register(test_listener)
        allure_commons.plugin_manager.register(test_listener)
        config.add_cleanup(cleanup_factory(test_listener))

        file_logger = AllureFileLogger(report_dir, clean)
        allure_commons.plugin_manager.register(file_logger)
        config.add_cleanup(cleanup_factory(file_logger))


def pytest_collection_modifyitems(items, config):
    arg_labels = set().union(config.option.allure_epics,
                             config.option.allure_features,
                             config.option.allure_stories,
                             config.option.allure_severities)

    items[:] = filter(lambda item: arg_labels & set(allure_labels(item)) if arg_labels else True, items)


def pytest_namespace():
    return {"allure": allure}
