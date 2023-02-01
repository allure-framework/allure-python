import shutil
from pytest import FixtureRequest, fixture, Pytester
from tests.conftest import AllureIntegrationRunner
from tests.conftest import get_path_from_docstring
from behave.runner import Runner
import behave.step_registry
from behave.step_registry import StepRegistry


def __fix_behave_multirun():
    # behave doesn't play nicely with consecutive programmatic runs, so we
    # force it to do a proper reset here
    original_run_model = Runner.run_model
    def __fixed_run_model(self, *args, **kwargs):
        # Originally, the runner caches the instance of step_registry on a
        # module level and reuse that same registry on each run, resulting in
        # disparity between step registration and step matching.
        # Here we force the runner to use the newest instance of registry.
        self.step_registry = behave.step_registry.registry
        return original_run_model(self, *args, **kwargs)
    Runner.run_model = __fixed_run_model

    original_add_step_definition = StepRegistry.add_step_definition
    def __fixed_add_step_definition(self, *args, **kwargs):
        # The same happens with step registration mechanism embedded into
        # bdd declarators (given, then, etc).
        # Here we redirect add_step_definition method to the newest instance of
        # registry.
        return original_add_step_definition(
            behave.step_registry.registry,
            *args,
            **kwargs
        )
    StepRegistry.add_step_definition = __fixed_add_step_definition


class AllureBehaveRunner:
    def __init__(self, pytester: Pytester, request: FixtureRequest):
        self.pytester = pytester
        self.request = request
        self.runner = AllureIntegrationRunner("behave")
        self.exit_code = None
        self.allure_results = None

    def run_allure_behave(self, *args: str):
        result = self.runner.run_allure_integration((
            "--no-snippets",
            "-f", "allure_behave.formatter:AllureFormatter",
            "-o", "allure-results",
            *args
        ))
        self.exit_code = result["return-value"]
        self.allure_results = result["allure-results"]

    def run_feature_by_docstring_path(self):
        self.run_allure_behave(
            get_path_from_docstring(self.request)
        )

    def run_feature_of_current_test(self, **fmt_kwargs):
        test_folder = self.request.node.path.parent
        self.__generate_test_features(test_folder, fmt_kwargs)
        self.__copy_test_feature_steps(test_folder)
        self.run_allure_behave(self.pytester.path)

    def __generate_test_features(self, test_folder, fmt_kwargs):
        for feature_path in test_folder.glob("*.feature"):
            dst_path = self.pytester.path.joinpath(feature_path.name)
            with open(feature_path, "r", encoding="utf-8") as src:
                with open(dst_path, "w+", encoding="utf-8") as dst:
                    dst.writelines(
                        line.format_map(fmt_kwargs) for line in src.readlines()
                    )

    def __copy_test_feature_steps(self, test_folder):
        tmp_steps_folder = self.pytester.path.joinpath("steps")
        tmp_steps_folder.mkdir(exist_ok=True)
        for step_path in test_folder.glob("*_steps.py"):
            if not step_path.name.startswith("test_"):
                dst_path = tmp_steps_folder.joinpath(step_path.name)
                shutil.copyfile(step_path, dst_path)

@fixture
def allure_behave_runner(pytester: Pytester, request: FixtureRequest):
    return AllureBehaveRunner(pytester, request)


@fixture
def executed_docstring_path(allure_behave_runner):
    allure_behave_runner.run_feature_by_docstring_path()
    return allure_behave_runner

__fix_behave_multirun()