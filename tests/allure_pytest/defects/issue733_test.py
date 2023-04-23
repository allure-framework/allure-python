import allure
from allure_pytest.utils import allure_title


@allure.issue("733", name="Issue 733")
def test_no_allure_title_error_if_item_obj_missing():
    item_with_no_obj_attr_stub = object()

    assert allure_title(item_with_no_obj_attr_stub) is None
