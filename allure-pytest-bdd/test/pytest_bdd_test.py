import pytest
from pytest_bdd import scenario


# @scenario('../features/scenario.feature', 'Default labels')
# def test_conftest():
#     pass


@pytest.mark.skip
@scenario('../features/outline.feature', 'Default labels')
def test_pytest_bdd_background():
    pass
