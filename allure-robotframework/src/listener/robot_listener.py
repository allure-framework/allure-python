import os
import allure_commons

from allure_commons.lifecycle import AllureLifecycle
from allure_commons.logger import AllureFileLogger
from allure_robotframework.allure_listener import AllureListener
from allure_robotframework.types import RobotKeywordType


DEFAULT_OUTPUT_PATH = os.path.join('output', 'allure')


# noinspection PyPep8Naming
class allure_robotframework(object):
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, logger_path=DEFAULT_OUTPUT_PATH):
        self.messages = Messages()

        self.logger = AllureFileLogger(logger_path)
        self.lifecycle = AllureLifecycle()
        self.listener = AllureListener(self.lifecycle)

        allure_commons.plugin_manager.register(self.logger)
        allure_commons.plugin_manager.register(self.listener)

    def start_suite(self, name, attributes):
        self.messages.start_context()
        self.listener.start_suite_container(name, attributes)

    def end_suite(self, name, attributes):
        self.messages.stop_context()
        self.listener.stop_suite_container(name, attributes)

    def start_test(self, name, attributes):
        self.messages.start_context()
        self.listener.start_test_container(name, attributes)
        self.listener.start_test(name, attributes)

    def end_test(self, name, attributes):
        messages = self.messages.stop_context()
        self.listener.stop_test(name, attributes, messages)
        self.listener.stop_test_container(name, attributes)

    def start_keyword(self, name, attributes):
        self.messages.start_context()
        keyword_type = attributes.get('type')
        # Todo fix value assign
        keyword_name = '{} = {}'.format(attributes.get('assign')[0], name) if attributes.get('assign') else name
        if keyword_type.upper() == RobotKeywordType.SETUP:
            self.listener.start_before_fixture(keyword_name)
        elif keyword_type.upper() == RobotKeywordType.TEARDOWN:
            self.listener.start_after_fixture(keyword_name)
        else:
            self.listener.start_keyword(name)

    def end_keyword(self, _, attributes):
        messages = self.messages.stop_context()
        keyword_type = attributes.get('type')
        if keyword_type.upper() == RobotKeywordType.SETUP:
            self.listener.stop_before_fixture(attributes, messages)
        elif keyword_type.upper() == RobotKeywordType.TEARDOWN:
            self.listener.stop_after_fixture(attributes, messages)
        else:
            self.listener.stop_keyword(attributes, messages)

    def log_message(self, message):
        self.messages.push(message)

    def close(self):
        for plugin in [self.logger, self.listener]:
            name = allure_commons.plugin_manager.get_name(plugin)
            allure_commons.plugin_manager.unregister(name=name)


class Messages(object):
    def __init__(self):
        self._stack = []

    def start_context(self):
        self._stack.append([])

    def stop_context(self):
        return self._stack.pop() if self._stack else list()

    def push(self, message):
        self._stack[-1].append(message) if self._stack else self._stack.append([message])
