from collections import deque
from behave.formatter.base import Formatter
from allure_behave.listener import AllureListener


class AllureFormatter(Formatter):
    def __init__(self, stream_opener, config):
        super(AllureFormatter, self).__init__(stream_opener, config)
        result_dir = self.stream_opener.name if self.stream_opener.name else "allure-result"
        self.listener = AllureListener(result_dir)
        self.current_feature = None
        self.current_background = None
        self.current_scenario = None
        self.before_started = False
        self.step_queue = deque()

    def _start_step(self, step):
        if step in self.current_scenario.background_steps and not self.before_started:
            self.listener.start_before(self.current_scenario, self.current_background)
            self.before_started = True

        elif step in self.current_scenario.steps and self.before_started:
            self.listener.stop_before(self.current_scenario, self.current_background)
            self.before_started = False

        self.listener.start_step(step)

    def _stop_step(self, step):
        self.listener.stop_step(step)

    def _flush_scenario(self):
        while self.step_queue:
            step = self.step_queue.popleft()
            self._start_step(step)
            self._stop_step(step)

        if self.current_scenario:
            self.listener.stop_scenario(self.current_scenario)
            self.current_scenario = None

        if self.current_background:
            self.listener.stop_group()

    def feature(self, feature):
        pass

    def background(self, background):
        self.current_background = background

    def scenario(self, scenario):
        self._flush_scenario()
        self.current_scenario = scenario
        if self.current_background:
            self.listener.start_group()
        self.listener.start_scenario(self.current_scenario)

    def step(self, step):
        self.step_queue.append(step)

    def match(self, match):
        step = self.step_queue.popleft()
        self._start_step(step)

    def result(self, result):
        self._stop_step(result)

    def eof(self):
        self._flush_scenario()
        self.current_background = None
        self.current_feature = None
