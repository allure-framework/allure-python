import allure
import pytest
from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status


@allure.issue("140")
@allure.feature("Integration")
@pytest.mark.parametrize("countdown", [2, 4])
def test_pytest_rerunfailures(allured_testdir, countdown):
    allured_testdir.testdir.makepyfile("""
        import threading
        import pytest

        back_to_normal = threading.local()

        @pytest.mark.flaky(reruns={countdown})
        def test_pytest_rerunfailures_example():
            countdown = getattr(back_to_normal, "countdown", 3)
            back_to_normal.countdown = countdown - 1
            assert not countdown > 0

    """.format(countdown=countdown))

    allured_testdir.run_with_allure()

    assert_that(allured_testdir.allure_report,
                has_test_case("test_pytest_rerunfailures_example",
                              with_status("failed" if countdown == 2 else "passed"))
                )
