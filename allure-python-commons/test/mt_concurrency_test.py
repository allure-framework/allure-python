import pytest
import allure_commons
from concurrent.futures import ThreadPoolExecutor
from allure_commons.reporter import AllureReporter
from allure_commons.utils import uuid4
from allure_commons.model2 import TestResult, TestStepResult
from allure_commons.logger import AllureMemoryLogger


@pytest.fixture
def allure_results():
    logger = AllureMemoryLogger()
    plugin_id = allure_commons.plugin_manager.register(logger)
    yield logger
    allure_commons.plugin_manager.unregister(plugin_id)

def __generate_test(name, start):
    return {
        "uuid": uuid4(),
        "name": name,
        "fullName": f"module#{name}",
        "status": "passed",
        "start": start,
        "stop": start + 100,
        "historyId": uuid4(),
        "testCaseId": uuid4(),
        "steps": [
            {
                "name": f"step-1 of {name}",
                "status": "passed",
                "start": start + 10,
                "stop": start + 40
            },
            {
                "name": f"step-1 of {name}",
                "status": "passed",
                "start": start + 50,
                "stop": start + 90
            }
        ]
    }

def test_state_not_corrupted_in_mt_env(allure_results):
    reporter = AllureReporter()

    def run_tests(thread, test_count):
        for index, start in enumerate(range(0, 100 * test_count, 100), 1):
            test = __generate_test(f"thread_{thread}_test_{index}", start)
            reporter.schedule_test(
                test["uuid"],
                TestResult(
                    name=test["name"],
                    status=test["status"],
                    start=test["start"],
                    stop=test["stop"],
                    uuid=test["uuid"],
                    fullName=test["fullName"],
                    historyId=test["historyId"],
                    testCaseId=test["testCaseId"]
                )
            )
            for step in test["steps"]:
                step_uuid = uuid4()
                reporter.start_step(
                    None,
                    step_uuid,
                    TestStepResult(
                        name=step["name"],
                        start=step["start"]
                    )
                )
                reporter.stop_step(
                    step_uuid,
                    stop=step["stop"],
                    status=step["status"]
                )
            reporter.close_test(test["uuid"])

    futures = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures.extend([
            pool.submit(run_tests, 1, 2),
            pool.submit(run_tests, 2, 2)
        ])
        pool.shutdown(True)

    for future in futures:
        assert future.done()
        assert future.result() is None
    assert len(allure_results.test_cases) == 4
