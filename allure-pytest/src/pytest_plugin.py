import argparse

import pytest


from allure import AllureTestHelper
from listener import AllureListener
from constants import Severity
from constants import Label
from utils import allure_labels
from six import text_type


def pytest_addoption(parser):
    parser.getgroup("reporting").addoption('--alluredir',
                                           action="store",
                                           dest="allure_report_dir",
                                           metavar="DIR",
                                           default=None,
                                           help="Generate Allure report in the specified directory (may not exist)")

    def label_type(name, legal_values=set()):
        def a_label_type(string):
            atoms = set(string.split(','))
            if legal_values and not atoms < legal_values:
                raise argparse.ArgumentTypeError('Illegal {} values: {}, only [{}] are allowed'.format(
                    name, ', '.join(atoms - legal_values), ', '.join(legal_values)))
            return set((name, v) for v in atoms)
        return a_label_type

    severities = [x.value for x in list(Severity)]
    parser.getgroup("general").addoption('--allure-severities',
                                         action="store",
                                         dest="allure_severities",
                                         metavar="SEVERITIES_SET",
                                         default={},
                                         type=label_type(name=Label.SEVERITY, legal_values=set(severities)),
                                         help="""Comma-separated list of severity names.
                                         Tests only with these severities will be run.
                                         Possible values are: %s.""" % ', '.join(severities))

    parser.getgroup("general").addoption('--allure-features',
                                         action="store",
                                         dest="allure_features",
                                         metavar="FEATURES_SET",
                                         default={},
                                         type=label_type(name=Label.FEATURE),
                                         help="""Comma-separated list of feature names.
                                         Run tests that have at least one of the specified feature labels.""")

    parser.getgroup("general").addoption('--allure-stories',
                                         action="store",
                                         dest="allure_stories",
                                         metavar="STORIES_SET",
                                         default={},
                                         type=label_type(name=Label.STORY),
                                         help="""Comma-separated list of story names.
                                         Run tests that have at least one of the specified story labels.""")


def pytest_configure(config):
    report_dir = config.option.allure_report_dir

    if report_dir:
        test_listener = AllureListener(config)
        config.pluginmanager.register(test_listener)

        test_helper = AllureTestHelper(config)
        config.pluginmanager.register(test_helper)


def pytest_runtest_setup(item):
    item_labels = set((name, value) for name, value in allure_labels(item))

    arg_labels = set().union(item.config.option.allure_features,
                             item.config.option.allure_stories,
                             item.config.option.allure_severities)

    if arg_labels and not item_labels & arg_labels:
        pytest.skip('Not suitable with selected labels: %s.' % ', '.join(text_type(l) for l in sorted(arg_labels)))


def pytest_addhooks(pluginmanager):
    import hooks
    # avoid warnings with pytest-2.8
    method = getattr(pluginmanager, "add_hookspecs", None)
    if method is None:
        method = pluginmanager.addhooks
    method(hooks)
