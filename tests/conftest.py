import pytest
from pytest import FixtureRequest
from .e2e import find_node_with_docstring_or_throw, RstExampleTable

pytest_plugins = "pytester"


@pytest.fixture
def rst_examples(request: FixtureRequest) -> RstExampleTable:
    return RstExampleTable.find_examples(request)


@pytest.fixture
def docstring(request: FixtureRequest) -> str:
    return find_node_with_docstring_or_throw(request)[1]
