def test_two_runs_no_clean():
    """
    >>> report_fixture = getfixture('allure_report_with_params')
    >>> allure_report_first_run = report_fixture(cache=False)
    >>> allure_report_second_run = report_fixture(cache=False)
    >>> assert_that(allure_report_second_run,
    ...             has_only_n_test_cases('test_two_runs_no_clean', 2)
    ... )
    """
    assert True
