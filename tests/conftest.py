import pytest
from pytest import FixtureRequest
from .e2e import find_node_with_docstring_or_throw, RstExampleTable

pytest_plugins = "pytester"


@pytest.fixture(autouse=True)
def reset_testplan_cache():
    from allure_commons.utils import _load_testplan

    _load_testplan.cache_clear()
    yield
    _load_testplan.cache_clear()


@pytest.fixture
def rst_examples(request: FixtureRequest) -> RstExampleTable:
    return RstExampleTable.find_examples(request)


@pytest.fixture
def docstring(request: FixtureRequest) -> str:
    return find_node_with_docstring_or_throw(request)[1]
