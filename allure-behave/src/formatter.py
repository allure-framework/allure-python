from behave.model import ScenarioOutline
from behave.formatter.base import Formatter
import allure_commons
from allure_commons.logger import AllureFileLogger
from allure_behave.listener import AllureListener


class AllureFormatter(Formatter):
    def __init__(self, stream_opener, config):
        super(AllureFormatter, self).__init__(stream_opener, config)

        self.listener = AllureListener(config)
        file_logger = AllureFileLogger(self.stream_opener.name)

        allure_commons.plugin_manager.register(self.listener)
        allure_commons.plugin_manager.register(file_logger)

    def _wrap_scenario(self, scenarios):
        for scenario in scenarios:
            if isinstance(scenario, ScenarioOutline):
                self._wrap_scenario(scenario)
            else:
                scenario.run = allure_commons.test(scenario.run, context={'scenario': scenario})

    def feature(self, feature):
        self._wrap_scenario(feature.scenarios)
        self.listener.start_feature()

    def step(self, step):
        self.listener.schedule_step(step)

    def match(self, match):
        self.listener.match_step(match)

    def result(self, result):
        self.listener.stop_behave_step(result)

    def eof(self):
        self.listener.stop_feature()
