import pytest


def test_skip_in_step():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_skip_in_step',
    ...                           with_status('skipped'),
    ...                           has_step('Step1',
    ...                                    with_status('skipped')
    ...                            )
    ...             )
    ... )
    """
    with pytest.allure.step('Step1'):
        pytest.skip()


def test_skip_in_deep_step():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_skip_in_deep_step',
    ...                           with_status('skipped'),
    ...                           has_step('Step1',
    ...                                    with_status('skipped'),
    ...                                    has_step('Step2',
    ...                                             with_status('skipped')
    ...                                    )
    ...                            )
    ...             )
    ... )
    """
    with pytest.allure.step('Step1'):
        with pytest.allure.step('Step2'):
            pytest.skip()


def test_fail_in_step_after_step():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_fail_in_step_after_step',
    ...                           with_status('failed'),
    ...                           has_step('Step1',
    ...                                    with_status('failed'),
    ...                                    has_step('Step2',
    ...                                             with_status('passed')
    ...                                    )
    ...                            )
    ...             )
    ... )
    """
    with pytest.allure.step('Step1'):
        with pytest.allure.step('Step2'):
            pass
        assert False
