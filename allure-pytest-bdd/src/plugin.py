import argparse

import allure_commons
import os
from allure_commons.logger import AllureFileLogger
from .pytest_bdd_listener import PytestBDDListener
from .utils import ALLURE_DESCRIPTION_MARK, ALLURE_DESCRIPTION_HTML_MARK
from .utils import ALLURE_LABEL_MARK, ALLURE_LINK_MARK

from .helper import AllureTestHelper, AllureTitleHelper

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

    parser.getgroup("general").addoption('--allure-environmant-vars-to-tag',
                                         action="store",
                                         dest="env_vars_to_tag",
                                         help="Comma-separated list of environment varibales to add as tags")

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

def pytest_addhooks(pluginmanager):
    # Need register title hooks before conftest init
    title_helper = AllureTitleHelper()
    allure_commons.plugin_manager.register(title_helper)

def pytest_configure(config):
    report_dir = config.option.allure_report_dir
    clean = config.option.clean_alluredir

    test_helper = AllureTestHelper(config)
    allure_commons.plugin_manager.register(test_helper)
    config.add_cleanup(cleanup_factory(test_helper))

    if report_dir:
        report_dir = os.path.abspath(report_dir)

        pytest_bdd_listener = PytestBDDListener(config)
        config.pluginmanager.register(pytest_bdd_listener)
        allure_commons.plugin_manager.register(pytest_bdd_listener)
        config.add_cleanup(cleanup_factory(pytest_bdd_listener))

        file_logger = AllureFileLogger(report_dir, clean)
        allure_commons.plugin_manager.register(file_logger)
        config.add_cleanup(cleanup_factory(file_logger))

    config.addinivalue_line("markers", "{mark}: allure label marker".format(mark=ALLURE_LABEL_MARK))
    config.addinivalue_line("markers", "{mark}: allure link marker".format(mark=ALLURE_LINK_MARK))
    config.addinivalue_line("markers", "{mark}: allure description".format(mark=ALLURE_DESCRIPTION_MARK))
    config.addinivalue_line("markers", "{mark}: allure description html".format(mark=ALLURE_DESCRIPTION_HTML_MARK))
