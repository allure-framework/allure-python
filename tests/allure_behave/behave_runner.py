import behave.step_registry
import sys

from behave import matchers
from behave.configuration import Configuration
from behave.formatter.base import StreamOpener
from behave.formatter.pretty import PrettyFormatter
from behave.parser import parse_feature
from behave.runner import Context, Runner
from behave.step_registry import setup_step_decorators
from behave.step_registry import StepRegistry
from pytest import FixtureRequest, Pytester
from typing import Sequence
from tests.e2e import AllureFrameworkRunner, PathlikeT

from allure_behave.formatter import AllureFormatter


def __fix_behave_in_memory_run():
    # Behave has poor support for consecutive prigrammatic runs. This is due to
    # how step decorators are cached.
    # There are three ways to introduce behave step decorators (i.e., @given)
    # into a step definition module:
    #   1. from behave import given (most common use)
    #   2. Without any import (just as if they are globally defined, less
    #      common)
    #   3. from behave.step_regostry import given (rarely)
    # The decorators are associated with a StepRegistry instance. This
    # association is first created when behave.step_registry module is imported.
    # They are then introduced as the behave package attributes and basically
    # are cached on a package level. Even if we replace the decorators from
    # behave.step_registry with new ones associated with a new StepRegistry with
    # the behave.step_registry.setup_step_decorators function, the decorators in
    # the behave package remains the same and remains attached to the old step
    # registry.
    # We need to create a new StepRegistry before a run to prevent step
    # duplication error, but if step definitions are created with the decorators
    # introduced with (1), they will be added to the old registry and will be
    # never matched.
    # To fix that we force decorators to use the global instance of the
    # StepRegistry.
    original_add_step_definition = StepRegistry.add_step_definition

    def __fixed_add_step_definition(self, *args, **kwargs):
        return original_add_step_definition(
            behave.step_registry.registry,
            *args,
            **kwargs
        )

    StepRegistry.add_step_definition = __fixed_add_step_definition


class _InMemoryBehaveRunner(Runner):
    def __init__(self, features, steps, environment, args=None):
        if args is None:
            args = []
        config = Configuration(
            ["--no-snippets"] + list(args),
            load_config=False
        )
        super().__init__(config)
        self.__features = features
        self.__steps = steps
        self.__environment = environment

    def load_hooks(self, filename=None):
        if self.__environment:
            exec(self.__environment, self.hooks)
        if "before_all" not in self.hooks:
            self.hooks["before_all"] = self.before_all_default_hook

    def load_step_definitions(self, extra_step_paths=None):
        behave.step_registry.registry = self.step_registry = StepRegistry()
        step_globals = {
            "use_step_matcher": matchers.use_step_matcher,
        }

        # To support the decorators (e.g., @given) with no imports
        setup_step_decorators(step_globals, self.step_registry)

        for step in self.__steps:
            step_module_globals = step_globals.copy()
            exec(step, step_module_globals)

    def load_features(self):
        self.features.extend(
            parse_feature(f) for f in self.__features
        )

    def load_formatter(self):
        opener = StreamOpener(stream=sys.stdout)
        allure_formatter = AllureFormatter(opener, self.config)
        pretty_formatter = PrettyFormatter(opener, self.config)
        self.formatters.append(allure_formatter)
        self.formatters.append(pretty_formatter)

    def run(self):
        self.context = Context(self)
        self.load_hooks()
        self.load_step_definitions()
        self.load_features()
        self.load_formatter()
        self.run_model()


class AllureBehaveRunner(AllureFrameworkRunner):
    """The runner to test allure-behave integration."""

    LOGGER_PATH = "allure_behave.formatter.AllureFileLogger"

    def __init__(self, request: FixtureRequest, pytester: Pytester):
        super().__init__(request, pytester, AllureBehaveRunner.LOGGER_PATH)

    def run_behave(
        self,
        feature_paths: Sequence[PathlikeT] = None,
        feature_literals: Sequence[str] = None,
        feature_rst_ids: Sequence[str] = None,
        step_paths: Sequence[PathlikeT] = None,
        step_literals: Sequence[str] = None,
        step_rst_ids: Sequence[str] = None,
        environment_path: PathlikeT = None,
        environment_literal: str = None,
        environment_rst_id: str = None,
        testplan_content: dict = None,
        testplan_path: PathlikeT = None,
        testplan_rst_id: str = None,
        options: Sequence[str] = None,
    ):
        """Executes behave in memory and returns the allure results of the run.

        Arguments:
            feature_paths (Sequence[str | Path]): paths to feature files
                relative to the current test module folder.
            feature_literals (Sequence[str]): content of feature files.
            feature_rst_ids (Sequence[str]): IDs of .rst code blocks containing
                feature file content.
            step_paths (Sequence[str | Path]): paths to step definition files
                relative to the current test module folder.
            step_literals (Sequence[str]): content of step definition files.
            step_rst_ids (Sequence[str]): IDs of .rst code blocks containing
                step definitions.
            environment_path (str | Path): a path to en environment file
                relative to the current test module folder.
            environment_literal (str): content of an environment file.
            environment_rst_id (str): an ID of a .rst code block containing an
                environment file content.
            testplan_content (dict): an allure testplan content.
            testplan_path (str | Path): a path to an allure testplan file
                relative to the current test module folder.
            testplan_rst_id (str): an ID of a .rst code block containing an
                allure testplan.
            options (Sequence[str]): behave CLI options

        Returns:
            allure_commons.logger.AllureMemoryLogger: the allure results of the
                run. The results of the last run are also accessible through the
                :attr:`allure_results` attribute.

        """
        return self._run(
            self._get_all_content(
                paths=feature_paths,
                literals=feature_literals,
                rst_ids=feature_rst_ids
            ),
            self._get_all_content(
                paths=step_paths,
                literals=step_literals,
                rst_ids=step_rst_ids
            ),
            self._resolve_content(
                path=environment_path,
                literal=environment_literal,
                rst_id=environment_rst_id
            ),
            testplan_content=testplan_content,
            testplan_path=testplan_path,
            testplan_rst_id=testplan_rst_id,
            options=options
        )

    def _run_framework(self, features, steps, environment, options):
        _InMemoryBehaveRunner(features, steps, environment, options).run()


__fix_behave_in_memory_run()

__all__ = ["AllureBehaveRunner"]
