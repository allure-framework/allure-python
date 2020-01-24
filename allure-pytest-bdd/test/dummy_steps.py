import pytest
from pytest_bdd import given, then, when


@given('passed step1')
def given_passed_step1():
    pass


@given('passed step')
def given_passed_step():
    pass


@when('passed step')
def when_passed_step():
    pass


@then('passed step')
def then_passed_step():
    pass


@given('skipped step')
def given_skipped_step():
    pytest.skip()


@when('skipped step')
def when_skipped_step():
    pytest.skip()


@then('skipped step')
def then_skipped_step():
    pytest.skip()


@given('failed step')
def given_failed_step():
    assert False


@when('failed step')
def when_failed_step():
    assert False


@then('failed step')
def then_failed_step():
    assert False


@when('<status> step')
def when_sfailed_step():
    pass
    assert False
