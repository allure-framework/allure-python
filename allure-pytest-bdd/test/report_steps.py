from pytest_bdd import then
from pytest_bdd import parsers
import pytest


@then(parsers.parse("it has result for {scenario} scenario"))
def has_result(allured_testdir, scenario):
    pass
