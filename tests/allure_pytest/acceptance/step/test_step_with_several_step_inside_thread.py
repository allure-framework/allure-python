from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step
from hamcrest import assert_that


def test_step_with_thread(allured_testdir):
    allured_testdir.testdir.makepyfile(
        """
    from concurrent.futures import ThreadPoolExecutor

    import allure

    @allure.step("thread {x}")
    def parallel_step(x=1):
        with allure.step("Sub-step in thread"):
            pass


    def test_thread():
        with allure.step("Start in thread"):
            with ThreadPoolExecutor(max_workers=2) as executor:
                executor.map(parallel_step, [1, 2])
    """
    )

    allured_testdir.run_with_allure()

    assert_that(allured_testdir.allure_report,
                has_test_case("test_thread",
                              has_step("Start in thread",
                                       has_step("thread 1", has_step("Sub-step in thread")),
                                       has_step("thread 2")
                                       )
                              )
                )


def test_step_with_reused_threads(executed_docstring_source):
    """
    >>> from concurrent.futures import ThreadPoolExecutor
    >>> from threading import Event
    >>> from random import shuffle
    >>> from time import sleep
    >>> import allure

    >>> def parallel_step(data):
    ...     event, index = data
    ...     with allure.step(f"thread {index}"):
    ...         event.wait()

    >>> def __execute_randomly(executor):
    ...     events = [Event() for i in range(1, 4)]
    ...     executor.map(parallel_step, zip(events, range(1, 4)))
    ...     shuffle(events)
    ...     for e in events:
    ...         e.set()

    >>> def test_thread():
    ...     with ThreadPoolExecutor(max_workers=2) as executor:
    ...         __execute_randomly(executor)
    ...     with allure.step("Reuse previous threads"):
    ...         with ThreadPoolExecutor(max_workers=2) as executor:
    ...             __execute_randomly(executor)
    """

    assert_that(
        executed_docstring_source.allure_report,
        has_test_case(
            "test_thread",
            has_step("thread 1"),
            has_step("thread 2"),
            has_step("thread 3"),
            has_step(
                "Reuse previous threads",
                has_step("thread 1"),
                has_step("thread 2"),
                has_step("thread 3"),
            )
        )
    )
