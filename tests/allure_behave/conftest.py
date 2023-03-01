from pytest import fixture
from .behave_runner import AllureBehaveRunner


@fixture
def behave_runner(request, pytester):
    return AllureBehaveRunner(request, pytester)
