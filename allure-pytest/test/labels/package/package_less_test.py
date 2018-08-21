def test_with_no_package(testdir, request):
    """
    Test where parent package is None
    >>> allure_report = getfixture('allure_report_with_params')('-p pytester')
    >>> assert_that(allure_report,
    ...             has_test_case('test_with_no_package',
    ...                           with_status('passed')
    ...             )
    ... )
    """
    testdir.makepyfile('''
    def test_simple(request):
        pass
    ''')
    result = testdir.runpytest_subprocess('--alluredir=allure')
    assert result.ret == 0

