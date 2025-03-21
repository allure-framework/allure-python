import pytest


ALLURE_PYTEST_BDD_HASHKEY = pytest.StashKey()


class AllurePytestBddTestData:

    def __init__(self, feature, scenario, params):
        self.feature = feature
        self.scenario = scenario
        self.params = params
        self.excinfo = None
        self.reported_steps = set()


def save_test_data(item, feature, scenario, params):
    item.stash[ALLURE_PYTEST_BDD_HASHKEY] = AllurePytestBddTestData(
        feature=feature,
        scenario=scenario,
        params=params,
    )


def get_test_data(item):
    return item.stash.get(ALLURE_PYTEST_BDD_HASHKEY, (None, None))


def get_saved_params(item):
    return get_test_data(item).params


def save_excinfo(item, excinfo):
    test_data = get_test_data(item)
    if test_data:
        test_data.excinfo = excinfo


def save_reported_step(item, step_uuid):
    test_data = get_test_data(item)
    if test_data:
        test_data.reported_steps.add(step_uuid)
