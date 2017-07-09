"""
>>> allure_report = getfixture('allure_report')


>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(8)),
...                 has_property('test_groups', has_length(0))
...             ))  # doctest: +SKIP


SEQUENCE OF STEPS
>>> for test_case_name in ['test_sequence_of_inside_steps',
...                        'test_sequence_of_outside_steps']:
...
...     for first_step_fail, second_step_fail in true_false:
...         test_case = '{name}[{first}-{second}]'.format(name=test_case_name,
...                                                       first=first_step_fail,
...                                                       second=second_step_fail)
...
...         if not first_step_fail:
...             assert_that(allure_report,
...                         has_test_case(test_case,
...                             has_step('First step', with_status('passed')),
...                             has_step('Second step', with_status('failed' if second_step_fail else 'passed'))
...                         ))
...
...         if first_step_fail:
...             assert_that(allure_report,
...                         has_test_case(test_case,
...                             has_step('First step', with_status('failed')),
...                             is_not(has_step('Second step'))
...                         ))
"""


import pytest
import allure

from itertools import product


true_false = [variants for variants in product([True, False], [True, False])]


@pytest.mark.parametrize("first_step_fail, second_step_fail", true_false)
def test_sequence_of_inside_steps(first_step_fail, second_step_fail):
    with allure.step('First step'):
        assert not first_step_fail
    with allure.step('Second step'):
        assert not second_step_fail


@allure.step("First step")
def first_step(step_fail):
    assert not step_fail


@allure.step("Second step")
def second_step(step_fail):
    assert not step_fail


@pytest.mark.parametrize("first_step_fail, second_step_fail", true_false)
def test_sequence_of_outside_steps(first_step_fail, second_step_fail):
    first_step(first_step_fail)
    second_step(second_step_fail)
