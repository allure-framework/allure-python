from .nose2_runner import AllureNose2Runner
from pytest import fixture


@fixture
def nose2_runner(request, pytester):
    yield AllureNose2Runner(request, pytester)
