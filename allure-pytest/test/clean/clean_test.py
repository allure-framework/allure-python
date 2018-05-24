def test_two_runs_clean():
    """
    >>> report_fixture = getfixture('allure_report_with_params')
    >>> allure_report_first_run = report_fixture('--clean-alluredir', cache=False)
    >>> allure_report_second_run = report_fixture('--clean-alluredir', cache=False)
    >>> assert_that(allure_report_second_run,
    ...             has_only_n_test_cases('test_two_runs_clean', 1)
    ... )
    """
    assert True
