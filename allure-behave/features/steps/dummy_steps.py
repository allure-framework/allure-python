from behave import given


@given(u'passed step')
@given(u'{what} passed step')
@given(u'passed step {where}')
@given(u'{what} passed step {where}')
def step_impl(*args, **kwargs):
    pass


@given(u'failed step')
@given(u'{what} failed step')
@given(u'failed step {where}')
@given(u'{what} failed step {where}')
def step_impl(*args, **kwargs):
    assert False, 'Assert message'


@given(u'broken step')
@given(u'{what} broken step')
@given(u'broken step {where}')
@given(u'{what} broken step {where}')
def step_impl(*args, **kwargs):
    raise ZeroDivisionError()
