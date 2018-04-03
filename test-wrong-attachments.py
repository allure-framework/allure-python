import allure
import pytest
import time

@pytest.fixture(scope="module", params=["a","b","c","d","e","f"])
def letter(request):
    timestamp = time.ctime()
    name = "Log {}".format(request.param)
    allure.attach(str(timestamp), name, attachment_type=allure.attachment_type.TEXT)
    return request.param

def test_letter(letter):
    time.sleep(1)
    assert True
