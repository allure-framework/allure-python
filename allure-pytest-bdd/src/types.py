from collections import namedtuple


class AllurePytestBddTestData:

    def __init__(self, feature, scenario, pytest_params):
        self.feature = feature
        self.scenario = scenario
        self.pytest_params = pytest_params
        self.excinfo = None
        self.reported_steps = set()
