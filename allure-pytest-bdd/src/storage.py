import pytest
from .types import AllurePytestBddTestData


ALLURE_PYTEST_BDD_HASHKEY = pytest.StashKey()


def save_test_data(item, feature, scenario, pytest_params):
    item.stash[ALLURE_PYTEST_BDD_HASHKEY] = AllurePytestBddTestData(
        feature=feature,
        scenario=scenario,
        pytest_params=pytest_params,
    )


def save_excinfo(item, excinfo):
    test_data = get_test_data(item)
    if test_data:
        test_data.excinfo = excinfo


def save_reported_step(item, step_uuid):
    test_data = get_test_data(item)
    if test_data:
        test_data.reported_steps.add(step_uuid)


def get_test_data(item):
    return item.stash.get(ALLURE_PYTEST_BDD_HASHKEY, (None, None))
