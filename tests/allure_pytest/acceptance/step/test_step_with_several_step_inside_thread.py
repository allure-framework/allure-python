from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step, not_


def test_step_with_thread(allure_pytest_runner: AllurePytestRunner):
    """
    >>> from concurrent.futures import ThreadPoolExecutor
    >>> import allure

    >>> @allure.step("thread {x}")
    ... def parallel_step(x=1):
    ...     with allure.step("Sub-step in thread"):
    ...         pass

    >>> def test_thread():
    ...     with allure.step("Start in thread"):
    ...         with ThreadPoolExecutor(max_workers=2) as executor:
    ...             executor.map(parallel_step, [1, 2])
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_thread",
            has_step(
                "Start in thread",
                has_step(
                    "thread 1",
                    has_step("Sub-step in thread")
                ),
                has_step("thread 2")
            )
        )
    )


def test_step_with_reused_threads(allure_pytest_runner: AllurePytestRunner):
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

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
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


def test_step_within_thread_nested(allure_pytest_runner: AllurePytestRunner):
    """
    >>> from concurrent.futures import ThreadPoolExecutor
    ... import allure
    ... import time
    ...
    ...
    ... def session_on_node(node_id, session):
    ...     with allure.step(f"Session#{session} on Node#{node_id}"):
    ...         pass
    ...
    ...
    ... def parallel_task_for_specific_node(node_id):
    ...     with allure.step(f"Node#{node_id}") as step:
    ...         with ThreadPoolExecutor(initializer=step.get_thread_initializer()) as executor:
    ...             for session in range(100):
    ...                 executor.submit(session_on_node, node_id, session)
    ...
    ...             executor.shutdown(wait=True)
    ...
    ...
    ... def test_multithreaded():
    ...     with allure.step("Root") as step:
    ...         with ThreadPoolExecutor(initializer=step.get_thread_initializer()) as executor:
    ...             for node_id in range(2):
    ...                 executor.submit(parallel_task_for_specific_node, node_id)
    ...
    ...             executor.shutdown(wait=True)
    ...
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_multithreaded",
            has_step(
                "Root",
                has_step(
                    "Node#0",
                    *[has_step(f"Session#{s} on Node#0") for s in range(100)],
                    *[not_(has_step(f"Session#{s} on Node#1")) for s in range(100)],
                ),
                has_step(
                    "Node#1",
                    *[has_step(f"Session#{s} on Node#1") for s in range(100)],
                    *[not_(has_step(f"Session#{s} on Node#0")) for s in range(100)],
                ),
            ),
        )
    )
