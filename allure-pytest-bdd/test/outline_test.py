from pytest_bdd import scenario
import pytest


@pytest.mark.skip(reason="https://github.com/pytest-dev/pytest-bdd/issues/447")
@scenario("../features/outline.feature", "Scenario outline")
def test_scenario_outline():
    pass
