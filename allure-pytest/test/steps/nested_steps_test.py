"""
>>> getfixture('inject_matchers')
>>> allure_report = getfixture('allure_report')

>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(32)),
...                 has_property('test_groups', has_length(0))
...             )) # doctest: +SKIP


>>> for test_case_name in ['test_nested_steps_inside_test',
...                        'test_nested_steps_outside_test',
...                        'test_mixed_nested_steps',
...                        'test_again_mixed_nested_steps']:
...
...     for first_fail_before_second, first_fail_after_second, second_fail in fruit_machine:
...         test_case = '{name}[{first_fail_before}-{first_fail_after}-{second_fail}]'.format(
...             name=test_case_name,
...             first_fail_before=first_fail_before_second,
...             first_fail_after=first_fail_after_second,
...             second_fail=second_fail)
...
...         if first_fail_before_second:
...             assert_that(allure_report,
...                         has_test_case(test_case,
...                             has_step('First step',
...                                 with_status('failed')
...                             )),
...                         is_not(has_step('Second step'))
...                         )
...
...         if not first_fail_before_second:
...             assert_that(allure_report,
...                         has_test_case(test_case,
...                             has_step('First step',
...                                 with_status('failed' if (first_fail_after_second or second_fail) else 'passed'),
...                                 has_step('Second step',
...                                     with_status('failed' if second_fail else 'passed')
...                                 )
...                             )
...                         ))

"""
import pytest
import allure
from itertools import product


fruit_machine = [variants for variants in product([True, False], [True, False],  [True, False])]


@pytest.mark.parametrize("first_fail_before_second, first_fail_after_second, second_fail", fruit_machine)
def test_nested_steps_inside_test(first_fail_before_second, first_fail_after_second, second_fail):
    with allure.step('First step'):
        assert not first_fail_before_second
        with allure.step('Second step'):
            assert not second_fail
        assert not first_fail_after_second


@allure.step("Second step")
def second_step(second_fail):
    assert not second_fail


@allure.step("First step")
def another_first_step(first_fail_before_second, first_fail_after_second, second_fail):
    assert not first_fail_before_second
    second_step(second_fail)
    assert not first_fail_after_second


@pytest.mark.parametrize("first_fail_before_second, first_fail_after_second, second_fail", fruit_machine)
def test_nested_steps_outside_test(first_fail_before_second, first_fail_after_second, second_fail):
    another_first_step(first_fail_before_second, first_fail_after_second, second_fail)


@allure.step("First step")
def yet_another_first_step(first_fail_before_second, first_fail_after_second, second_fail):
    assert not first_fail_before_second
    with allure.step('Second step'):
        assert not second_fail
    assert not first_fail_after_second


@pytest.mark.parametrize("first_fail_before_second, first_fail_after_second, second_fail", fruit_machine)
def test_mixed_nested_steps(first_fail_before_second, first_fail_after_second, second_fail):
    yet_another_first_step(first_fail_before_second, first_fail_after_second, second_fail)


@pytest.mark.parametrize("first_fail_before_second, first_fail_after_second, second_fail", fruit_machine)
def test_again_mixed_nested_steps(first_fail_before_second, first_fail_after_second, second_fail):
    with allure.step('First step'):
        assert not first_fail_before_second
        second_step(second_fail)
        assert not first_fail_after_second
