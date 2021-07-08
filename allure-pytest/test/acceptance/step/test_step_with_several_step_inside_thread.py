from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step
from hamcrest import assert_that


def test_step_with_thread(allured_testdir):
    allured_testdir.testdir.makepyfile(
        """
    from concurrent.futures import ThreadPoolExecutor

    import allure
    import pytest

    @allure.step("thread {x}")
    def parallel_step(x=1):
        pass


    def test_thread():
        with allure.step("Start in thread"):
            with ThreadPoolExecutor(max_workers=2) as executor:
                f_result = executor.map(parallel_step, [1, 2])
    """
    )

    allured_testdir.run_with_allure()

    assert_that(allured_testdir.allure_report,
                has_test_case("test_thread",
                              has_step("Start in thread",
                                       has_step("thread 1"), has_step("thread 2")
                                       )
                              )
                )
