# -*- coding: utf-8 -*-

import allure
from behave import given


@given(u'passed step')
@given(u'{what} passed step')
@given(u'passed step {where}')
@given(u'{what} passed step {where}')
def step_impl(*args, **kwargs):
    if 'with attachment' in kwargs.values():
        allure.attach('Hi there!', name='user attachment', attachment_type=allure.attachment_type.TEXT)
    pass


@given(u'failed step')
@given(u'{what} failed step')
@given(u'failed step {where}')
@given(u'{what} failed step {where}')
def step_impl(*args, **kwargs):
    assert False, 'Assert message'


@given(u'провальный шаг')
def step_impl(*args, **kwargs):
    assert False, u'Фиаско!'


@given(u'провальный шаг с ascii')
def step_impl(*args, **kwargs):
    assert False, 'Фиаско!'


@given(u'проходящий шаг')
def step_impl(*args, **kwargs):
    pass


@given(u'broken step')
@given(u'{what} broken step')
@given(u'broken step {where}')
@given(u'{what} broken step {where}')
def step_impl(*args, **kwargs):
    raise ZeroDivisionError()


@given(u'всегда будет <это>')
@given(u'всегда буду я')
def step_impl(*args, **kwargs):
    pass
