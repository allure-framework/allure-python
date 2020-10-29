from nose2.events import Plugin
from allure_commons import plugin_manager
from allure_commons.logger import AllureFileLogger
from allure_nose2.listener import AllureListener
from allure_commons.lifecycle import AllureLifecycle
from nose2 import result
from allure_commons.model2 import Status
from allure_commons.model2 import StatusDetails
from allure_commons.model2 import Label
from allure_commons.types import LabelType
from allure_commons.utils import host_tag, thread_tag

from allure_commons.utils import platform_label, md5


from .utils import timestamp_millis, status_details, update_attrs, labels, name, fullname, params
import allure_commons


class DecoratorsHelper(object):
    @classmethod
    @allure_commons.hookimpl
    def decorate_as_label(cls, label_type, labels):
        # ToDo functools.update_wrapper
        def wrapper(test):
            update_attrs(test, label_type, labels)
            return test

        return wrapper

    @classmethod
    def register(cls):
        if cls not in plugin_manager.get_plugins():
            plugin_manager.register(cls)

    @classmethod
    def unregister(cls):
        if cls in plugin_manager.get_plugins():
            plugin_manager.unregister(plugin=cls)


DecoratorsHelper.register()


class Allure(Plugin):
    configSection = 'allure'
    commandLineSwitch = (None, "allure", "Generate an Allure report")

    def __init__(self, *args, **kwargs):
        super(Allure, self).__init__(*args, **kwargs)
        self._host = host_tag()
        self._thread = thread_tag()
        self.lifecycle = AllureLifecycle()
        self.logger = AllureFileLogger("allure-result")
        self.listener = AllureListener(self.lifecycle)

    def registerInSubprocess(self, event):
        self.unregister_allure_plugins()
        event.pluginClasses.append(self.__class__)

    def startSubprocess(self, event):
        self.register_allure_plugins()

    def stopSubprocess(self, event):
        self.unregister_allure_plugins()

    def register_allure_plugins(self):
        plugin_manager.register(self.listener)
        plugin_manager.register(self.logger)

    def unregister_allure_plugins(self):
        plugin_manager.unregister(plugin=self.listener)
        plugin_manager.unregister(plugin=self.logger)

    def is_registered(self):
        return all([plugin_manager.is_registered(self.listener),
                    plugin_manager.is_registered(self.logger)])

    def startTestRun(self, event):
        self.register_allure_plugins()

    def afterTestRun(self, event):
        self.unregister_allure_plugins()

    def startTest(self, event):
        if self.is_registered():
            with self.lifecycle.schedule_test_case() as test_result:
                test_result.name = name(event)
                test_result.start = timestamp_millis(event.startTime)
                test_result.fullName = fullname(event)
                test_result.testCaseId = md5(test_result.fullName)
                test_result.historyId = md5(event.test.id())
                test_result.labels.extend(labels(event.test))
                test_result.labels.append(Label(name=LabelType.HOST, value=self._host))
                test_result.labels.append(Label(name=LabelType.THREAD, value=self._thread))
                test_result.labels.append(Label(name=LabelType.FRAMEWORK, value='nose2'))
                test_result.labels.append(Label(name=LabelType.LANGUAGE, value=platform_label()))
                test_result.parameters = params(event)

    def stopTest(self, event):
        if self.is_registered():
            with self.lifecycle.update_test_case() as test_result:
                test_result.stop = timestamp_millis(event.stopTime)
            self.lifecycle.write_test_case()

    def testOutcome(self, event):
        if self.is_registered():
            with self.lifecycle.update_test_case() as test_result:
                if event.outcome == result.PASS and event.expected:
                    test_result.status = Status.PASSED
                elif event.outcome == result.PASS and not event.expected:
                    test_result.status = Status.PASSED
                    test_result.statusDetails = StatusDetails(message="test passes unexpectedly")
                elif event.outcome == result.FAIL and not event.expected:
                    test_result.status = Status.FAILED
                    test_result.statusDetails = status_details(event)
                elif event.outcome == result.ERROR:
                    test_result.status = Status.BROKEN
                    test_result.statusDetails = status_details(event)
                elif event.outcome == result.SKIP:
                    test_result.status = Status.SKIPPED
                    test_result.statusDetails = status_details(event)
                # Todo default status and other cases
                # elif event.outcome == result.FAIL and event.expected:
                #     pass
                    # self.skipped += 1
                    # skipped = ET.SubElement(testcase, 'skipped')
                    # skipped.set('message', 'expected test failure')
                    # skipped.text = msg
