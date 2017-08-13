# -*- coding: utf-8 -*-
import os
import traceback
from allure_commons.utils import now
from allure import fixture
from collections import deque

import nose
import allure_commons
import unittest
import unittest2
import threading

from enum import Enum
from allure_commons.reporter import AllureReporter
from allure_commons.model2 import TestResultContainer, TestBeforeResult, TestAfterResult, \
    TestStepResult, Parameter, Status, TestResult, Link, Label, StatusDetails
from allure_commons.utils import uuid4
from allure_commons.logger import AllureFileLogger
from allure_commons.types import LabelType
from nose.plugins.base import Plugin
from nose.plugins.attrib import AttributeSelector

ATTRIBUTE_OPTIONS = ['feature', 'story', 'severity']


class ContextType(str, Enum):
    CLASS = 'class'
    MODULE = 'module'
    PACKAGE = 'package'


SETUP_FIXTURES = ['setup_class', 'setup_all', 'setupClass', 'setupAll', 'setUpClass', 'setUpAll',
                  'setup_module', 'setupModule', 'setUpModule', 'setup', 'setUp', 'setup_package',
                  'setupPackage', 'setUpPackage']

TEARDOWN_FIXTURES = ['teardown_class', 'teardown_all', 'teardownClass', 'teardownAll', 'tearDownClass',
                     'tearDownAll', 'teardown_module', 'teardownModule', 'tearDownModule', 'teardown',
                     'tearDown', 'teardown_package', 'teardownPackage', 'tearDownPackage']


class Allure(Plugin):
    @allure_commons.hookimpl
    def start_step(self, uuid, title, params):
        parameters = [Parameter(name=name, value=value) for name, value in params]
        step = TestStepResult(name=title, start=now(), parameters=parameters)
        self.allure.start_step(None, uuid, step)

    @allure_commons.hookimpl
    def stop_step(self, uuid, exc_type, exc_val, exc_tb):
        status = Status.PASSED
        if exc_type is not None:
            if exc_type in [unittest.case.SkipTest, unittest2.case.SkipTest, nose.SkipTest]:
                status = Status.SKIPPED
            else:
                status = Status.FAILED

        self.allure.stop_step(uuid, stop=now(), status=status)

    @allure_commons.hookimpl
    def start_fixture(self, parent_uuid, uuid, name):
        if not self._context_queue:
            # we are in the multiprocess mode, starting new container
            context_uuid = uuid4()
            self._context_queue.append(context_uuid)
            group = TestResultContainer(uuid=context_uuid)
            self.allure.start_group(context_uuid, group)
            self.allure.update_group(context_uuid, start=now())
        if name in SETUP_FIXTURES:
            before_fixture = TestBeforeResult(name=name, start=now())
            self.allure.start_before_fixture(self._context_queue[-1], uuid, before_fixture)
        elif name in TEARDOWN_FIXTURES:
            after_fixture = TestAfterResult(name=name, start=now())
            self.allure.start_after_fixture(self._context_queue[-1], uuid, after_fixture)
        if name == 'tearDown' and self._current_test_uuid:
            self.allure.update_test(self._current_test_uuid, stop=now())

    @allure_commons.hookimpl
    def stop_fixture(self, uuid, name, exc_type, exc_val, exc_tb):
        if name in SETUP_FIXTURES:
            self.allure.stop_before_fixture(uuid, stop=now())
        elif name in TEARDOWN_FIXTURES:
            self.allure.stop_after_fixture(uuid, stop=now())
        if name == 'setUp' and self._current_test_uuid:
            self.allure.update_test(self._current_test_uuid, start=now())

    def options(self, parser, env):
        super(Allure, self).options(parser, env)

        parser.add_option('--results-dir', dest='results_dir')
        parser.add_option('--clear', dest='clear',
                          action='store_true', default=True)
        parser.add_option('--feature', dest='feature')
        parser.add_option('--story', dest='story')
        parser.add_option('--severity', dest='severity')
        parser.add_option('--epic', dest='epic')

    def configure(self, options, conf):
        super(Allure, self).configure(options, conf)
        self.options = options
        self._context_queue = deque()
        self._current_test_uuid = None

        if options.results_dir:
            expanded = os.path.expanduser(os.path.expandvars(options.results_dir))
            results_dir = os.path.normpath(os.path.abspath(expanded))

            if not os.path.isdir(results_dir):
                os.makedirs(results_dir)
            else:
                # Need to provide an option to skip dir cleaning due to multiprocess
                # plugin usage can lead to results dir cleaning at the end of testing.
                # Unfortunately not possible to detect is it child process or parent.
                # Otherwise possible to clean results dir only in parent process always.
                if options.clear:
                    for file_name in os.listdir(results_dir):
                        file_path = os.path.join(results_dir, file_name)
                        if os.path.isfile(file_path):
                            os.unlink(file_path)

            self.allure = nose.allure = AllureReporter()
            file_logger = AllureFileLogger(results_dir)
            allure_commons.plugin_manager.register(file_logger)
            allure_commons.plugin_manager.register(self)

        self._configure_attributes(options, conf)

    def begin(self):
        if not self.conf.options.results_dir:
            raise LookupError('Provide "--results-dir" argument with a path to store Allure results!')

    def startContext(self, context):
        patch_fixtures(context)
        context_uuid = uuid4()
        self._context_queue.append(context_uuid)
        group = TestResultContainer(uuid=context_uuid)
        self.allure.start_group(context_uuid, group)
        self.allure.update_group(context_uuid, start=now())

    def stopContext(self, context):
        context_uuid = self._context_queue.pop()
        self.allure.stop_group(context_uuid, stop=now())

    def beforeTest(self, test):
        patch_fixtures(test.test)

    def startTest(self, test):
        self._current_test_uuid = uuid4()
        if hasattr(test.test, "test"):
            method = test.test.test
        else:
            method = getattr(test.test, test.test._testMethodName)
        self.allure.update_group(self._context_queue[-1], children=self._current_test_uuid)
        test_case = TestResult(name=method.__name__, uuid=self._current_test_uuid)
        test_case.description = test.shortDescription()
        self.allure.schedule_test(self._current_test_uuid, test_case)

    def stopTest(self, test):
        self.allure.close_test(self._current_test_uuid)
        self._current_test_uuid = None

    def addError(self, test, err):
        message, trace = self._parse_tb(err)
        details = StatusDetails(message=message, trace=trace)
        self.allure.update_test(uuid=self._current_test_uuid, status=Status.BROKEN, statusDetails=details)

    def addFailure(self, test, err):
        message, trace = self._parse_tb(err)
        details = StatusDetails(message=message, trace=trace)
        self.allure.update_test(uuid=self._current_test_uuid, status=Status.FAILED, statusDetails=details)

    def addSuccess(self, test):
        self.allure.update_test(uuid=self._current_test_uuid, status=Status.PASSED)

    def addSkip(self, test):
        self.allure.update_test(uuid=self._current_test_uuid, status=Status.SKIPPED)

    @staticmethod
    def _parse_tb(trace):
        message = ''.join(
            traceback.format_exception_only(trace[0], trace[1])).strip()
        trace = ''.join(traceback.format_exception(*trace)).strip()
        return message, trace

    def _configure_attributes(self, options, conf):
        if not getattr(options, 'attr', None):
            options.attr = []

        for label in ATTRIBUTE_OPTIONS:
            if getattr(options, label, None):
                values = getattr(options, label).split(',')
                label_key = getattr(LabelType, label.upper())
                pairs = ["{}={}".format(label_key, v.strip()) for v in values]
                options.attr.extend(pairs)

        attribute_selector = next((p for p in self.conf.plugins.plugins
                                   if isinstance(p, AttributeSelector)), None)
        if options.attr and attribute_selector:
            attribute_selector.configure(options, conf)

    @allure_commons.hookimpl
    def attach_data(self, body, name, attachment_type, extension):
        self.allure.attach_data(uuid4(), body, name=name, attachment_type=attachment_type, extension=extension)

    @allure_commons.hookimpl
    def attach_file(self, source, name, attachment_type, extension):
        self.allure.attach_file(uuid4(), source, name=name, attachment_type=attachment_type, extension=extension)

    @allure_commons.hookimpl
    def add_link(self, url, link_type, name):
        self.allure.update_test(None, links=[Link(link_type, url, name)])

    @allure_commons.hookimpl
    def add_label(self, label_type, labels):
        for label in labels:
            self.allure.update_test(None, labels=Label(label_type, label))


def patch_fixtures(context):
    for f in SETUP_FIXTURES + TEARDOWN_FIXTURES:
        if hasattr(context, f) and not isinstance(getattr(context, f), fixture):
            setattr(context, f, fixture(getattr(context, f)))
