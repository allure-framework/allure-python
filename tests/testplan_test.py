import json
from unittest.mock import patch

import pytest

from allure_commons.utils import get_testplan


@pytest.mark.parametrize("selection", [None, []])
def test_excluded_plan_loading(tmp_path, monkeypatch, selection):
    plan = {"excludedTests": [{"id": 101}]}
    if selection is not None:
        plan["tests"] = selection
    path = tmp_path / "testplan.json"
    path.write_text(json.dumps(plan))
    monkeypatch.setenv("ALLURE_TESTPLAN_PATH", str(path))

    excluded = get_testplan("excludedTests")

    assert excluded == [{"id": 101}]
    assert get_testplan() == []


def test_testplan_parsed_once_for_both_fields(tmp_path, monkeypatch):
    path = tmp_path / "testplan.json"
    path.write_text('{"tests": [{"id": 1}], "excludedTests": [{"id": 2}]}')
    monkeypatch.setenv("ALLURE_TESTPLAN_PATH", str(path))

    with patch("allure_commons.utils.json.load", wraps=json.load) as load:
        selected = get_testplan()
        excluded = get_testplan("excludedTests")
        repeated = get_testplan("excludedTests")

    assert selected == [{"id": 1}]
    assert excluded == repeated == [{"id": 2}]
    assert load.call_count == 1


@pytest.mark.parametrize("entries,ids,selector,expected", [
    ([{"id": 101}], ("101",), None, True),
    ([{"id": "101"}], (101,), None, True),
    ([{"id": "101"}], ("other", "101"), None, True),
    ([{"selector": "file#test[case]"}], (), "file#test[case]", True),
    ([{"selector": "file#test[case]"}], (), "file#testc", False),
    ([{"selector": "file#test"}], (), "other#test", False),
    ([{"id": 101, "selector": "different"}], ("101",), "file#test", True),
    ([{"id": "different", "selector": "file#test"}], ("101",), "file#test", True),
    ([{}], (), None, False),
    ([{"id": None, "selector": None}], (None,), None, False),
    ([{"id": "None"}], (), None, False),
    ([], ("101",), "file#test", False),
])
def test_matching_nonmissing_id_or_exact_selector(entries, ids, selector, expected):
    from allure_commons.utils import matches_testplan

    matched = matches_testplan(entries, allure_ids=ids, selector=selector)

    assert matched is expected
