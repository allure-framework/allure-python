from __future__ import absolute_import

import os
from collections import OrderedDict
import allure_commons

from allure_commons.model2 import TestResultContainer, TestResult, TestStepResult, TestAfterResult, TestBeforeResult, \
    StatusDetails, Label, Link
from allure_commons.reporter import AllureReporter
from allure_commons.utils import now, uuid4, md5, host_tag
from allure_commons.logger import AllureFileLogger
from allure_commons.types import AttachmentType, LabelType, LinkType
from allure_commons.types import Severity
from allure_commons.utils import platform_label
from robot.libraries.BuiltIn import BuiltIn
from allure_robotframework.types import RobotKeywordType, RobotLogLevel
from allure_robotframework import utils
from allure_robotframework.allure_listener import AllureListener

from allure_robotframework.utils import allure_tags, allure_labels, allure_links


# noinspection PyPep8Naming
class allure_robotframework(object):
    ROBOT_LISTENER_API_VERSION = 2
    DEFAULT_OUTPUT_PATH = os.path.join('output', 'allure')
    LOG_MESSAGE_FORMAT = '{full_message}<p><b>[{level}]</b> {message}</p>'
    FAIL_MESSAGE_FORMAT = '{full_message}<p style="color: red"><b>[{level}]</b> {message}</p>'

    def __init__(self, logger_path=DEFAULT_OUTPUT_PATH):
        self.stack = []
        self.items_log = {}
        self.pool_id = None
        self.links = OrderedDict()
        self._previous_keyword_failed = False
        self._traceback_message = None

        self.reporter = AllureReporter()
        self.listener = AllureListener(self.reporter)
        self.logger = AllureFileLogger(logger_path)

        allure_commons.plugin_manager.register(self.logger)
        allure_commons.plugin_manager.register(self.listener)

    def start_suite(self, name, attributes):
        if not self.pool_id:
            self.pool_id = BuiltIn().get_variable_value('${PABOTEXECUTIONPOOLID}')
            self.pool_id = int(self.pool_id) if self.pool_id else 0
        self.start_new_group(name, attributes)

    def end_suite(self, name, attributes):
        self.stop_current_group()

    def start_test(self, name, attributes):
        self.start_new_group(name, attributes)
        self.start_new_test(name, attributes)

    def end_test(self, name, attributes):
        self.stop_current_test(name, attributes)
        self.stop_current_group()

    def start_keyword(self, name, attributes):
        self.start_new_keyword(name, attributes)

    def end_keyword(self, name, attributes):
        self.end_current_keyword(name, attributes)

    def log_message(self, message):
        level = message.get('level')
        if self._previous_keyword_failed:
            self._traceback_message = message.get('message')
            self._previous_keyword_failed = False
        if level == RobotLogLevel.FAIL:
            self._previous_keyword_failed = True
            self.reporter.get_item(self.stack[-1]).statusDetails = StatusDetails(message=message.get('message'))
        self.append_message_to_last_item_log(message, level)

    def start_new_group(self, name, attributes):
        uuid = uuid4()
        self.set_suite_link(attributes.get('metadata'), uuid)
        if self.stack:
            parent_suite = self.reporter.get_last_item(TestResultContainer)
            parent_suite.children.append(uuid)
        self.stack.append(uuid)
        suite = TestResultContainer(uuid=uuid,
                                    name=name,
                                    description=attributes.get('doc'),
                                    start=now())
        self.reporter.start_group(uuid, suite)

    def stop_current_group(self):
        uuid = self.stack.pop()
        self.remove_suite_link(uuid)
        self.reporter.stop_group(uuid, stop=now())

    def start_new_test(self, name, attributes):
        uuid = uuid4()
        self.reporter.get_last_item(TestResultContainer).children.append(uuid)
        self.stack.append(uuid)
        test_case = TestResult(uuid=uuid,
                               historyId=md5(attributes.get('longname')),
                               name=name,
                               fullName=attributes.get('longname'),
                               start=now())
        self.reporter.schedule_test(uuid, test_case)

    def stop_current_test(self, name, attributes):
        uuid = self.stack.pop()
        test = self.reporter.get_test(uuid)
        test.status = utils.get_allure_status(attributes.get('status'))
        test.labels.extend(utils.get_allure_suites(attributes.get('longname')))

        test.labels.extend(allure_tags(attributes))
        for label_type in (LabelType.EPIC, LabelType.FEATURE, LabelType.STORY):
            test.labels.extend(allure_labels(attributes, label_type))
        for link_type in (LinkType.ISSUE, LinkType.TEST_CASE, LinkType.LINK):
            test.links.extend(allure_links(attributes, link_type))
        test.labels.append(Label(name=LabelType.THREAD, value=self.pool_id))
        test.labels.append(Label(name=LabelType.HOST, value=host_tag()))
        test.labels.append(Label(name=LabelType.FRAMEWORK, value='robotframework'))
        test.labels.append(Label(name=LabelType.LANGUAGE, value=platform_label()))
        test.statusDetails = StatusDetails(message=attributes.get('message'), trace=self.get_traceback_message())
        test.description = attributes.get('doc')
        last_link = list(self.links.values())[-1] if self.links else None
        if attributes.get(Severity.CRITICAL, 'no') == 'yes':
            test.labels.append(Label(name=LabelType.SEVERITY, value=Severity.CRITICAL))
        if last_link:
            test.links.append(Link(LinkType.LINK, last_link, 'Link'))
        test.stop = now()
        self.reporter.close_test(uuid)

    def start_new_keyword(self, name, attributes):
        uuid = uuid4()
        parent_uuid = self.stack[-1]
        step_name = '{} = {}'.format(attributes.get('assign')[0], name) if attributes.get('assign') else name
        args = {
            'name': step_name,
            'description': attributes.get('doc'),
            'parameters': utils.get_allure_parameters(attributes.get('args')),
            'start': now()
        }
        keyword_type = attributes.get('type')
        last_item = self.reporter.get_last_item()
        if keyword_type in RobotKeywordType.FIXTURES and not isinstance(last_item, TestStepResult):
            if isinstance(last_item, TestResult):
                parent_uuid = self.stack[-2]
            if keyword_type == RobotKeywordType.SETUP:
                self.reporter.start_before_fixture(parent_uuid, uuid, TestBeforeResult(**args))
            elif keyword_type == RobotKeywordType.TEARDOWN:
                self.reporter.start_after_fixture(parent_uuid, uuid, TestAfterResult(**args))
            self.stack.append(uuid)
            return
        self.stack.append(uuid)
        self.reporter.start_step(parent_uuid=parent_uuid,
                                 uuid=uuid,
                                 step=TestStepResult(**args))

    def end_current_keyword(self, name, attributes):
        uuid = self.stack.pop()
        if uuid in self.items_log:
            self.reporter.attach_data(uuid=uuid4(),
                                      body=self.items_log.pop(uuid).replace('\n', '<br>'),
                                      name='Keyword Log',
                                      attachment_type=AttachmentType.HTML)
        args = {
            'uuid': uuid,
            'status': utils.get_allure_status(attributes.get('status')),
            'stop': now()
        }
        keyword_type = attributes.get('type')
        parent_item = self.reporter.get_last_item()
        if keyword_type in RobotKeywordType.FIXTURES and not isinstance(parent_item, TestStepResult):
            if keyword_type == RobotKeywordType.SETUP:
                self.reporter.stop_before_fixture(**args)
                return
            elif keyword_type == RobotKeywordType.TEARDOWN:
                self.reporter.stop_after_fixture(**args)
                return
        self.reporter.stop_step(**args)

    def append_message_to_last_item_log(self, message, level):
        full_message = self.items_log[self.stack[-1]] if self.stack[-1] in self.items_log else ''
        message_format = self.FAIL_MESSAGE_FORMAT if level in RobotLogLevel.CRITICAL_LEVELS else self.LOG_MESSAGE_FORMAT
        self.items_log[self.stack[-1]] = message_format.format(full_message=full_message,
                                                               level=message.get('level'),
                                                               message=message.get('message'))

    def set_suite_link(self, metadata, uuid):
        if metadata:
            link = metadata.get('Link')
            if link:
                self.links[uuid] = link

    def remove_suite_link(self, uuid):
        if self.links.get(uuid):
            self.links.pop(uuid)

    def get_traceback_message(self):
        if BuiltIn().get_variable_value('${LOG LEVEL}') in (RobotLogLevel.DEBUG, RobotLogLevel.TRACE):
            return self._traceback_message
        return None

    def close(self):
        for plugin in [self.logger, self.listener]:
            name = allure_commons.plugin_manager.get_name(plugin)
            allure_commons.plugin_manager.unregister(name=name)
