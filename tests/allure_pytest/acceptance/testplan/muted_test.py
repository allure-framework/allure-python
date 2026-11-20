import pytest


@pytest.mark.parametrize("selection", [None, []])
@pytest.mark.parametrize("entry", [{"id": 12}, {"selector": "test_muted_sample#test_muted"}])
def test_muted_body_is_not_run(allure_pytest_runner, entry, selection):
    """
    >>> import allure
    >>> import pytest
    >>> @pytest.mark.parametrize("value", [1, 2])
    ... @allure.id("12")
    ... def test_muted(value):
    ...     raise AssertionError("muted body ran")
    >>> def test_active():
    ...     pass
    >>> @pytest.mark.skip(reason="user")
    ... def test_user_skip():
    ...     pass
    """
    plan = {"excludedTests": [entry]}
    if selection is not None:
        plan["tests"] = selection

    results = allure_pytest_runner.run_docstring(filename="test_muted_sample", testplan=plan)

    muted = [result for result in results.test_cases if result["name"].startswith("test_muted")]
    assert len(results.test_cases) == 4
    assert len(muted) == 2
    assert all(result["status"] == "skipped" and result["statusDetails"]["muted"] is True for result in muted)
    assert next(result for result in results.test_cases if result["name"] == "test_active")["status"] == "passed"
    assert not next(result for result in results.test_cases if result["name"] == "test_user_skip")[
        "statusDetails"
    ].get("muted", False)


@pytest.mark.parametrize("inverted,expected", [(False, "test_selected"), (True, "test_outside")])
def test_muting_does_not_change_selection(allure_pytest_runner, inverted, expected):
    """
    >>> def test_selected():
    ...     pass
    >>> def test_outside():
    ...     raise AssertionError("muted body ran")
    """
    results = allure_pytest_runner.run_docstring(
        *(["--inversion", "true"] if inverted else []),
        filename="test_muted_sample",
        testplan={"tests": [{"selector": "test_muted_sample#test_selected"}],
                  "excludedTests": [{"selector": "test_muted_sample#test_outside"}]}
    )

    assert len(results.test_cases) == 1
    assert results.test_cases[0]["name"] == expected
    assert results.test_cases[0]["status"] == ("skipped" if inverted else "passed")
