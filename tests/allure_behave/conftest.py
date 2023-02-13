import sys
import behave.step_registry
from itertools import chain
from pathlib import Path
from pytest import FixtureRequest, fixture, Pytester
from tests.conftest import fake_logger
from tests.conftest import RstExampleTable
from behave.runner import Runner
from behave.step_registry import StepRegistry
from typing import Sequence
from behave.configuration import Configuration
from behave.formatter.base import StreamOpener
from behave.runner import Context, Runner
from behave import matchers
from behave.step_registry import setup_step_decorators
from behave.parser import parse_feature
from behave.formatter.pretty import PrettyFormatter
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
            "step_matcher":     matchers.step_matcher,
        }

        # To support the decorators (i.e., @given) with no imports
        setup_step_decorators(step_globals, self.step_registry)

        default_matcher = matchers.current_matcher
        for step in self.__steps:
            step_module_globals = step_globals.copy()
            exec(step, step_module_globals)
            matchers.current_matcher = default_matcher

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


class AllureBehaveRunner:
    def __init__(self, pytester: Pytester, request: FixtureRequest):
        self.pytester = pytester
        self.request = request
        self.exit_code = None
        self.allure_results = None

    def run_behave(
        self,
        *,
        features: Sequence[str] = None,
        steps: Sequence[str] = None,
        environment: str = None,
        feature_paths: Sequence[str|Path] = None,
        step_paths: Sequence[str|Path] = None,
        environment_path: str|Path = None,
        cli_args: Sequence[str] = None
    ) -> None:
        """Runs behave against specific set of features, steps and an
        environment each specified either as a string literal or as a path to a
        file.

        Arguments:
            features (Sequence[str]): a sequence of strings each representing
                a .feature file content.
            steps (Sequence[str]): a sequence of strings each representing
                content of a step definition file.
            environment (str): a string representing content of the
                environment.py file.
            feature_paths (Sequence[str|Path]): a sequence of feature files.
            step_paths (Sequence[str|Path]): a sequence of step definition
                files.
            environment_path (str|Path): a path to the environment.py file.
            cli_args (Sequence[str]): a CLI arguments passed to behave.

        The result of the run is accessible through the :code:`allure_results`
        attribute.
        """

        path_to_fake = "allure_behave.formatter.AllureFileLogger"
        testdir = self.request.path.parent
        features = self.__extend_content_seq(testdir, features, feature_paths)
        steps = self.__extend_content_seq(testdir, steps, step_paths)
        environment = self.__resolve_content(
            testdir,
            environment,
            environment_path
        )
        with fake_logger(path_to_fake) as allure_results:
            _InMemoryBehaveRunner(features, steps, environment, cli_args).run()
        self.allure_results = allure_results

    def run_rst_example(
        self,
        *features: str,
        steps: Sequence[str] = None,
        feature_literals: Sequence[str] = None,
        step_literals: Sequence[str] = None,
        environment: str = None,
        environment_literal: str = None,
        cli_args: Sequence[str] = None
    ) -> None:
        """Loads code blocks from reStructuredText document and executes behave
        against them.

        Arguments:
            *features (str): names of the feature code blocks

        Keyword arguments:
            feature_literals (Sequence[str]): a sequence of strings, each
                representing a .feature file content.
            steps (Sequence[str]): names of the code blocks defining steps.
            step_literals (Sequence[str]): a sequence of strings, each
                representing a step definition file content.
            environment (str): an optional name of the environment.py code
                block.
            environment_literal (str): an optional string, representing the
                environment.py file content.

        Note:
            See :class:`RstExampleTable` for more details.

        Note:
            Uses in-memory execution model. See :meth:`run_behave_in_memory` for
            more details.

        The results of the run could be accessed through the
        :code:`allure_results` attribute.
        """

        examples_table = RstExampleTable.find_examples(self.request)
        self.run_behave(
            features=self.__resolve_code_blocks(
                examples_table,
                features,
                feature_literals
            ),
            steps=self.__resolve_code_blocks(
                examples_table,
                steps,
                step_literals
            ),
            environment=examples_table[environment] if environment else\
                        environment_literal,
            cli_args=cli_args
        )

    @staticmethod
    def __extend_content_seq(testdir, content_seq, paths):
        if content_seq is None:
            content_seq = []
        if paths is None:
            paths = []
        return chain(
            content_seq,
            (AllureBehaveRunner.__read_test_file(testdir, p) for p in paths)
        )

    @staticmethod
    def __read_test_file(testdir, path):
        fullpath = testdir.joinpath(path)
        with open(fullpath, encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def __resolve_content(testdir, content, path):
        if content is None and path is not None:
            content = AllureBehaveRunner.__read_test_file(testdir, path)
        return content

    @staticmethod
    def __pick_examples(table, example_names): return (
        table[n] for n in example_names
    )

    @staticmethod
    def __resolve_code_blocks(table, code_block_names, literals):
        code_block_names = code_block_names or []
        literals = literals or []
        return chain(
            AllureBehaveRunner.__pick_examples(table, code_block_names),
            literals
        )


@fixture
def behave_runner(pytester: Pytester, request: FixtureRequest):
    return AllureBehaveRunner(pytester, request)


__fix_behave_in_memory_run()
