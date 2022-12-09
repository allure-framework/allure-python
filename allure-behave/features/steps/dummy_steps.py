import allure
from behave import given


@given('passed step')
@given('{what} passed step')
@given('passed step {where}')
@given('{what} passed step {where}')
def step_impl(*args, **kwargs):
    if 'with attachment' in kwargs.values():
        allure.attach('Hi there!', name='user attachment', attachment_type=allure.attachment_type.TEXT)
    pass


@given('failed step')
@given('{what} failed step')
@given('failed step {where}')
@given('{what} failed step {where}')
def step_impl(*args, **kwargs):
    assert False, 'Assert message'


@given('провальный шаг')
def step_impl(*args, **kwargs):
    assert False, 'Фиаско!'


@given('провальный шаг с ascii')
def step_impl(*args, **kwargs):
    assert False, 'Фиаско!'


@given('проходящий шаг')
def step_impl(*args, **kwargs):
    pass


@given('broken step')
@given('{what} broken step')
@given('broken step {where}')
@given('{what} broken step {where}')
def step_impl(*args, **kwargs):
    raise ZeroDivisionError()


@given('всегда будет <это>')
@given('всегда буду я')
def step_impl(*args, **kwargs):
    pass
