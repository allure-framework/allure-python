import os
import datetime
from itertools import zip_longest
from robot.libraries.BuiltIn import BuiltIn

import allure_commons
from allure_commons.utils import now
from allure_commons.utils import uuid4
from allure_commons.utils import md5
from allure_commons.utils import platform_label
from allure_commons.utils import host_tag
from allure_commons.utils import format_exception, format_traceback
from allure_commons.model2 import Label, Link
from allure_commons.model2 import Status, StatusDetails
from allure_commons.model2 import Parameter
from allure_commons.types import LabelType, AttachmentType, Severity, LinkType
from allure_robotframework.utils import get_allure_status
from allure_robotframework.utils import get_allure_suites
from allure_robotframework.utils import get_allure_parameters
from allure_robotframework.utils import allure_labels, allure_links, allure_tags
from allure_robotframework.types import RobotStatus, RobotLogLevel


def get_status(exception):
    if exception and isinstance(exception, AssertionError):
        return Status.FAILED
    elif exception:
        return Status.BROKEN
    return Status.PASSED


def get_status_details(exc_type, exception, exc_traceback):
    if exception:
        return StatusDetails(message=format_exception(exc_type, exception),
                             trace=format_traceback(exc_traceback))


DEFAULT_POOL_ID = "default-" + uuid4()


def pool_id():
    pabot_pool_id = BuiltIn().get_variable_value('${PABOTEXECUTIONPOOLID}')
    pabot_caller_id = BuiltIn().get_variable_value('${CALLER_ID}')
    return "{}-{}".format(pabot_pool_id, pabot_caller_id) \
        if all([pabot_pool_id, pabot_caller_id]) else DEFAULT_POOL_ID


def get_message_time(timestamp):
    s_time = datetime.datetime.strptime(timestamp, "%Y%m%d %H:%M:%S.%f")
    return int(s_time.timestamp() * 1000)


LOG_MESSAGE_FORMAT = '<p><b>[{level}]</b>&nbsp;{message}</p>'
FAIL_MESSAGE_FORMAT = '<p style="color: red"><b>[{level}]</b>&nbsp;{message}</p>'
MAX_STEP_MESSAGE_COUNT = int(os.getenv('ALLURE_MAX_STEP_MESSAGE_COUNT', 0))


class AllureListener(object):
    def __init__(self, lifecycle):
        self.lifecycle = lifecycle
        self._platform = platform_label()
        self._host = host_tag()
        self._current_msg = None
        self._current_tb = None

    def start_suite_container(self, name, attributes):
        with self.lifecycle.start_container():
            pass

    def stop_suite_container(self, name, attributes):
        suite_status = get_allure_status(attributes.get('status'))
        suite_message = attributes.get('message')

        with self.lifecycle.update_container() as container:
            for uuid in container.children:
                with self.lifecycle.update_test_case(uuid) as test_result:
                    if test_result and test_result.status == Status.PASSED and suite_message:
                        test_result.status = suite_status
                        test_result.statusDetails = StatusDetails(message=self._current_msg or suite_message,
                                                                  trace=self._current_tb)
                self.lifecycle.write_test_case(uuid)
        self._current_tb, self._current_msg = None, None
        self.lifecycle.write_container()

    def start_test_container(self, name, attributes):
        with self.lifecycle.start_container():
            pass

    def stop_test_container(self, name, attributes):
        suite_status = get_allure_status(attributes.get('status'))
        suite_message = attributes.get('message')

        with self.lifecycle.schedule_test_case() as test_result:
            if test_result.status == Status.PASSED and suite_message:
                test_result.status = suite_status
                test_result.statusDetails = StatusDetails(message=self._current_msg or suite_message,
                                                          trace=self._current_tb)

        self._current_tb, self._current_msg = None, None
        self.lifecycle.write_container()

    def start_before_fixture(self, name):
        with self.lifecycle.start_before_fixture() as fixture:
            fixture.name = name

    def stop_before_fixture(self, attributes, messages):
        self._report_messages(messages)
        with self.lifecycle.update_before_fixture() as fixture:
            fixture.status = get_allure_status(attributes.get('status'))
            fixture.statusDetails = StatusDetails(message=self._current_msg, trace=self._current_tb)
        self.lifecycle.stop_before_fixture()

    def start_after_fixture(self, name):
        with self.lifecycle.start_after_fixture() as fixture:
            fixture.name = name

    def stop_after_fixture(self, attributes, messages):
        self._report_messages(messages)
        with self.lifecycle.update_after_fixture() as fixture:
            fixture.status = get_allure_status(attributes.get('status'))
            fixture.statusDetails = StatusDetails(message=self._current_msg, trace=self._current_tb)
        self.lifecycle.stop_after_fixture()

    def start_test(self, name, attributes):
        uuid = uuid4()
        with self.lifecycle.schedule_test_case(uuid=uuid) as test_result:
            long_name = attributes.get('longname')
            test_result.name = name
            test_result.fullName = long_name
            test_result.historyId = md5(long_name)
            test_result.start = now()

        for container in self.lifecycle.containers():
            container.children.append(uuid)

    def stop_test(self, _, attributes, messages):
        self._report_messages(messages)

        if 'skipped' in [tag.lower() for tag in attributes['tags']]:
            attributes['status'] = RobotStatus.SKIPPED

        with self.lifecycle.update_test_case() as test_result:
            test_result.stop = now()
            test_result.description = attributes.get('doc')
            test_result.status = get_allure_status(attributes.get('status'))
            test_result.labels.extend(get_allure_suites(attributes.get('longname')))
            test_result.labels.append(Label(name=LabelType.FRAMEWORK, value='robotframework'))
            test_result.labels.append(Label(name=LabelType.LANGUAGE, value=self._platform))
            test_result.labels.append(Label(name=LabelType.HOST, value=self._host))
            test_result.labels.append(Label(name=LabelType.THREAD, value=pool_id()))
            test_result.labels.extend(allure_tags(attributes))
            tags = attributes.get('tags', ())
            test_result.labels.extend(allure_labels(tags))
            test_result.statusDetails = StatusDetails(message=attributes.get('message'),
                                                      trace=self._current_tb)

            if attributes.get('critical') == 'yes':
                test_result.labels.append(Label(name=LabelType.SEVERITY, value=Severity.CRITICAL))

            for link_type in (LinkType.ISSUE, LinkType.TEST_CASE, LinkType.LINK):
                test_result.links.extend(allure_links(attributes, link_type))

        self._current_tb, self._current_msg = None, None

    def start_keyword(self, name):
        with self.lifecycle.start_step() as step:
            step.name = name

    def stop_keyword(self, attributes, messages):
        self._report_messages(messages)
        with self.lifecycle.update_step() as step:
            step.status = get_allure_status(attributes.get('status'))
            step.parameters = get_allure_parameters(attributes.get('args'))
            step.statusDetails = StatusDetails(message=self._current_msg, trace=self._current_tb)
        self.lifecycle.stop_step()

    def _report_messages(self, messages):
        has_trace = BuiltIn().get_variable_value("${LOG LEVEL}") in (RobotLogLevel.DEBUG, RobotLogLevel.TRACE)
        attachment = ""

        for message, next_message in zip_longest(messages, messages[1:]):
            name = message.get('message')
            level = message.get('level')
            message_format = FAIL_MESSAGE_FORMAT if level in RobotLogLevel.CRITICAL_LEVELS else LOG_MESSAGE_FORMAT

            if level == RobotLogLevel.FAIL:
                self._current_msg = name or self._current_msg
                self._current_tb = next_message.get("message") if has_trace and next_message else self._current_tb

            if len(messages) > MAX_STEP_MESSAGE_COUNT:
                attachment += message_format.format(level=level, message=name.replace('\n', '<br>'))
            else:
                with self.lifecycle.start_step() as step:
                    step.name = name
                    step.start = step.stop = get_message_time(message.get("timestamp"))
                    step.status = Status.FAILED if level in RobotLogLevel.CRITICAL_LEVELS else Status.PASSED
                self.lifecycle.stop_step()

        if attachment:
            self.lifecycle.attach_data(uuid=uuid4(), body=attachment, name='Keyword Log',
                                       attachment_type=AttachmentType.HTML)

    @allure_commons.hookimpl
    def decorate_as_label(self, label_type, labels):
        def deco(func):
            def wrapper(*args, **kwargs):
                self.add_label(label_type, labels)
                func(*args, **kwargs)
            return wrapper
        return deco

    @allure_commons.hookimpl
    def add_label(self, label_type, labels):
        with self.lifecycle.update_test_case() as case:
            for label in labels if case else ():
                case.labels.append(Label(label_type, label))

    @allure_commons.hookimpl
    def add_link(self, url, link_type, name):
        with self.lifecycle.update_test_case() as case:
            link = Link(url=url, type=link_type, name=name)
            if case and link not in case.links:
                case.links.append(Link(url=url, type=link_type, name=name))

    @allure_commons.hookimpl
    def attach_data(self, body, name, attachment_type, extension):
        self.lifecycle.attach_data(uuid4(), body, name=name, attachment_type=attachment_type, extension=extension)

    @allure_commons.hookimpl
    def attach_file(self, source, name, attachment_type, extension):
        self.lifecycle.attach_file(uuid4(), source, name=name, attachment_type=attachment_type, extension=extension)

    @allure_commons.hookimpl
    def start_step(self, uuid, title, params):
        with self.lifecycle.start_step() as step:
            step.name = title
            step.start = now()
            step.parameters = [Parameter(name=name, value=value) for name, value in params.items()]

    @allure_commons.hookimpl
    def stop_step(self, uuid, exc_type, exc_val, exc_tb):
        with self.lifecycle.update_step() as step:
            step.stop = now()
            step.status = get_status(exc_val)
            step.statusDetails = get_status_details(exc_type, exc_val, exc_tb)
        self.lifecycle.stop_step()
