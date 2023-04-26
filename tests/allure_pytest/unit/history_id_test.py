from allure_pytest.utils import get_history_id
from allure_commons.model2 import Parameter


def test_no_dependency_on_parameters_order():
    assert get_history_id("my-full-name", [
        Parameter(name="a", value="1"),
        Parameter(name="b", value="2")
    ], {}) == get_history_id("my-full-name", [
        Parameter(name="b", value="2"),
        Parameter(name="a", value="1")
    ], {})


def test_original_values_are_used():
    assert get_history_id("my-full-name", [
        Parameter(name="a", value="1")
    ], {"a": "b"}) == get_history_id("my-full-name", [
        Parameter(name="a", value="b")
    ], {})


def test_excluded_values_are_ignored():
    assert get_history_id("my-full-name", [
        Parameter(name="a", value="1")
    ], {}) == get_history_id("my-full-name", [
        Parameter(name="a", value="1"),
        Parameter(name="b", value="2", excluded=True)
    ], {})
