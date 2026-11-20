from behave.model import ScenarioOutline
from behave.formatter.base import Formatter
import allure_commons
from allure_commons.logger import AllureFileLogger
from allure_behave.listener import AllureListener
from allure_commons.utils import get_testplan
from allure_behave.utils import is_planned_scenario, get_fullname, scenario_labels, TEST_PLAN_SKIP_REASON
from allure_commons.utils import matches_testplan, MUTED_TEST_REASON
from allure_commons.types import LabelType


class AllureFormatter(Formatter):
    def __init__(self, stream_opener, config):
        super(AllureFormatter, self).__init__(stream_opener, config)

        self.listener = AllureListener(config)
        self.file_logger = AllureFileLogger(self.stream_opener.name)

        allure_commons.plugin_manager.register(self.listener)
        allure_commons.plugin_manager.register(self.file_logger)

        self.testplan = get_testplan()
        self.muted_tests = get_testplan("excludedTests")

    def _wrap_scenario(self, scenarios):
        for scenario in scenarios:
            if isinstance(scenario, ScenarioOutline):
                self._wrap_scenario(scenario)
            else:
                scenario.run = allure_commons.test(scenario.run, context={"scenario": scenario})
            is_planned_scenario(scenario, self.testplan)
            if not isinstance(scenario, ScenarioOutline) and scenario.skip_reason != TEST_PLAN_SKIP_REASON:
                ids = [label.value for label in scenario_labels(scenario) if label.name == LabelType.ID]
                if matches_testplan(self.muted_tests, allure_ids=ids, selector=get_fullname(scenario)):
                    scenario.skip(reason=MUTED_TEST_REASON)

    def uri(self, uri):
        self.listener.start_file()

    def feature(self, feature):
        self._wrap_scenario(feature.scenarios)

    def step(self, step):
        self.listener.schedule_step(step)

    def match(self, match):
        self.listener.match_step(match)

    def result(self, result):
        self.listener.stop_behave_step(result)

    def eof(self):
        self.listener.stop_feature()

    def close(self):
        try:
            super().close()
        finally:
            for plugin in [self.file_logger, self.listener]:
                name = allure_commons.plugin_manager.get_name(plugin)
                if allure_commons.plugin_manager.has_plugin(name):
                    allure_commons.plugin_manager.unregister(name=name)

    def close_stream(self):
        self.listener.stop_session()
