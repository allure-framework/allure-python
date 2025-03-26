import argparse
import os

import allure_commons
from allure_commons.logger import AllureFileLogger
from allure_commons.lifecycle import AllureLifecycle

from .allure_api_listener import AllurePytestBddApiHooks
from .pytest_bdd_listener import PytestBDDListener

from .utils import ALLURE_DESCRIPTION_MARK
from .utils import ALLURE_DESCRIPTION_HTML_MARK
from .utils import ALLURE_LABEL_MARK
from .utils import ALLURE_LINK_MARK


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

    def link_pattern(string):
        pattern = string.split(':', 1)
        if not pattern[0]:
            raise argparse.ArgumentTypeError("A link type is mandatory")

        if len(pattern) != 2:
            raise argparse.ArgumentTypeError("A link pattern is mandatory")
        return pattern

    parser.getgroup("general").addoption(
        "--allure-link-pattern",
        action="append",
        dest="allure_link_pattern",
        metavar="LINK_TYPE:LINK_PATTERN",
        default=[],
        type=link_pattern,
        help="""A URL pattern for a link type. Allows short links in tests,
        e.g., 'issue-1'. `pattern.format(short_url)` will be called to get
        the full URL"""
    )


def cleanup_factory(plugin):
    def clean_up():
        name = allure_commons.plugin_manager.get_name(plugin)
        allure_commons.plugin_manager.unregister(name=name)
    return clean_up


def register_marks(config):
    config.addinivalue_line("markers", f"{ALLURE_DESCRIPTION_MARK}: allure description")
    config.addinivalue_line("markers", f"{ALLURE_DESCRIPTION_HTML_MARK}: allure description in HTML")
    config.addinivalue_line("markers", f"{ALLURE_LABEL_MARK}: allure label marker")
    config.addinivalue_line("markers", f"{ALLURE_LINK_MARK}: allure link marker")


def pytest_configure(config):
    register_marks(config)

    report_dir = config.option.allure_report_dir
    clean = False if config.option.collectonly else config.option.clean_alluredir

    if report_dir:
        report_dir = os.path.abspath(report_dir)

        lifecycle = AllureLifecycle()

        pytest_bdd_listener = PytestBDDListener(lifecycle)
        config.pluginmanager.register(pytest_bdd_listener)
        allure_commons.plugin_manager.register(pytest_bdd_listener)
        config.add_cleanup(cleanup_factory(pytest_bdd_listener))

        allure_api_impl = AllurePytestBddApiHooks(config, lifecycle)
        allure_commons.plugin_manager.register(allure_api_impl)
        config.add_cleanup(cleanup_factory(allure_api_impl))

        file_logger = AllureFileLogger(report_dir, clean)
        allure_commons.plugin_manager.register(file_logger)
        config.add_cleanup(cleanup_factory(file_logger))
