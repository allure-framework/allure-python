from pytest import fixture
from .robot_runner import AllureRobotRunner


@fixture
def robot_runner(request, pytester):
    return AllureRobotRunner(request, pytester)
