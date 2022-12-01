from hamcrest import assert_that, has_entry, has_length
from allure_commons_test.report import has_only_n_test_cases
from allure_commons_test.result import has_step
from allure_commons_test.result import with_status

def test_steps_could_be_run_cuncurrently_with_asyncio(executed_docstring_source):
    """
    >>> import allure
    >>> import pytest
    >>> import asyncio

    >>> async def run_steps(name, to_set, to_wait):
    ...     with allure.step(f"{name}-step"):
    ...         to_set.set()
    ...         await to_wait.wait()

    >>> async def run_tasks():
    ...     task1_fence = asyncio.Event()
    ...     task2_fence = asyncio.Event()
    ...     await asyncio.gather(
    ...         run_steps("task1", task2_fence, task1_fence),
    ...         run_steps("task2", task1_fence, task2_fence)
    ...     )

    >>> def test_asyncio_concurrency():
    ...     asyncio.get_event_loop().run_until_complete(
    ...         run_tasks()
    ...     )
    """

    assert_that(
        executed_docstring_source.allure_report,
        has_only_n_test_cases(
            "test_asyncio_concurrency",
            1,
            with_status("passed"),
            has_entry("steps", has_length(2)),
            has_step(
                "task1-step",
                with_status("passed")
            ),
            has_step(
                "task2-step",
                with_status("passed")
            )
        ),
        "Should contain a single test with two non-nested steps"
    )

