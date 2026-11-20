import json
import os
from pathlib import Path
import subprocess
import sys


def test_muted_tests_in_subprocesses(tmp_path):
    (tmp_path / "test_muting.py").write_text("""
import allure
from unittest import TestCase
@allure.id("12")
class TestMuted(TestCase):
    def test_muted(self):
        raise AssertionError("muted body ran")
def test_active():
    pass
""")
    plan = tmp_path / "plan.json"
    plan.write_text(json.dumps({"excludedTests": [{"id": 12}]}))

    run = subprocess.run(
        [sys.executable, "-m", "nose2", "--plugin", "allure_nose2.plugin", "--allure",
         "--plugin", "nose2.plugins.mp", "-N2"],
        cwd=tmp_path, env={**os.environ, "ALLURE_TESTPLAN_PATH": str(plan)},
        capture_output=True, text=True,
    )
    results = [json.loads(path.read_text()) for path in Path(tmp_path / "allure-result").glob("*-result.json")]

    assert run.returncode == 0, run.stdout + run.stderr
    assert len(results) == 2
    muted = next(result for result in results if result["name"] == "test_muted")
    assert muted["status"] == "skipped"
    assert muted["statusDetails"]["muted"] is True
    assert next(result for result in results if result["name"] == "test_active")["status"] == "passed"
