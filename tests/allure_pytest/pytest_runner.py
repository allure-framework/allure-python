from doctest import script_from_examples
from pathlib import Path
from pytest import FixtureRequest, Pytester, StashKey
from tests.e2e import AllureFrameworkRunner, altered_env, PathlikeT
from typing import Sequence, Tuple, Union

from allure_commons.logger import AllureMemoryLogger


class AllurePytestRunner(AllureFrameworkRunner):
    """A runner for allure_pytest integration.

    Note:
        Automatic plugin loading is disabled for all test runs initiated using
        an instance of this class. If you need to test allure compatibility with
        some pytest plugin, use :method:`AllurePytestRunner` or
        :method:`AllurePytestRunner` to explicitly request its loading.

    """

    LOGGER_PATH = "allure_pytest.plugin.AllureFileLogger"
    DOCTEST_RESULT_KEY = StashKey()

    def __init__(self, request: FixtureRequest, pytester: Pytester):
        super().__init__(request, pytester, AllurePytestRunner.LOGGER_PATH)
        self.select_plugins("allure_pytest")

    def enable_plugins(self, *plugins: str) -> None:
        """Request loading of pytest plugins on subsequent runs. Those plugins
        are added into the list of the previously requested ones.

        """

        self.enabled_plugins.update(plugins)

    def select_plugins(self, *plugins: str) -> None:
        """Request loading of pytest plugins on subsequent runs. All other
        plugins will not be loaded.

        Note:
            Don't forget to add an allure integration plugin as well (i.e.,
            allure_pytest).

        """

        self.enabled_plugins = set(plugins)

    def run_docstring(
        self,
        *cli_args: str,
        filename: PathlikeT = None,
        testplan: dict = None
    ) -> AllureMemoryLogger:
        """Runs a doctest from a docstring of the current test node (or one of its
        parents).

        Arguments:
            *cli_args (str): pytest CLI arguments

        Keyword Arguments:
            filename (str | Path): an optional file name where the doctest is
                saved before pytest is run. This should be a relative name.
            testplan (dict): an optional allure testplan data.

        Returns:
            allure_commons.logger.AllureMemoryLogger: allure results that were
                collected during the test run.
        """
        docstring = self._find_docstring()
        testfile_content = script_from_examples(docstring)
        return self.run_pytest(
            (filename, testfile_content),
            cli_args=cli_args,
            testplan=testplan
        )

    def run_docpath_examples(
        self,
        *cli_args: str,
        filename: PathlikeT = None,
        testplan: dict = None,
        cache: bool = False
    ) -> AllureMemoryLogger:
        """Runs a doctest from a document denoted by a path in docstring of
        the current test node (or one of its parents).

        If the path is relative, it is prepended with the rootdir.

        Arguments:
            *cli_args (str): pytest CLI arguments.

        Keyword Arguments:
            filename (str | Path): an optional file name where the doctest is
                saved before pytest is run. This should be a relative name.
            testplan (dict): an optional allure testplan data.
            cache (bool): set this flag if the allure results should be cached
                on a node which docstring was originally used as the path. This
                improves the performance if you have multiple tests on the same
                document. Be careful though, this may lead to unexpected results
                if the tests are relied upon different environments (i.e., the
                CLI arguments are different). Only one run can be cached for
                any given test.

        Returns:
            allure_commons.logger.AllureMemoryLogger: allure results that were
                collected during the test run.
        """

        if cache:
            return self._cache_docstring_test_result(
                AllurePytestRunner.DOCTEST_RESULT_KEY,
                self.__test_docpath_examples,
                filename,
                cli_args,
                testplan
            )
        return self.__test_docpath_examples(
            filename=filename,
            cli_args=cli_args,
            testplan=testplan,
            docpath=self._find_docstring()
        )

    def run_pytest(
        self,
        *testfile_literals: Union[str, Tuple[PathlikeT, str]],
        conftest_literal: str = None,
        cli_args: Sequence[str] = None,
        testplan: dict = None
    ) -> AllureMemoryLogger:
        """Runs a nested pytest session in an isolated allure context.

        Arguments:
            *testfile_literals (str | Tuple[str | Path, str]): test files to
                run. Each test file is represented either as a content string or
                as a tuple of a path and a string. The path should be relative
                to the pytester's path.

        Keyword arguments:
            conftest_literal (str): an optional conftest.py content.
            cli_args (Sequence[str]): pytest CLI arguments.
            testplan (dict): an optional allure testplan data.

        Returns:
            allure_commons.logger.AllureMemoryLogger: allure results that were
                collected during the test run.
        """

        if conftest_literal:
            self.pytester.makeconftest(conftest_literal)
        if cli_args is None:
            cli_args = ()
        plugin_args = self.__iter_plugin_args()
        pytest_args = [
            "--alluredir",
            self.pytester.path,
            *plugin_args,
            *cli_args
        ]
        self.__generate_testfiles(testfile_literals)
        return self._run(pytest_args, testplan_content=testplan)

    def _run_framework(self, options):
        with altered_env(PYTEST_DISABLE_PLUGIN_AUTOLOAD="true"):
            self.pytester.runpytest(*options)

    def __generate_testfiles(self, testfiles):
        for testfile in testfiles:
            filepath = None
            content = testfile
            if not isinstance(testfile, str):
                filepath, content = testfile
            if filepath:
                extension = Path(filepath).suffix or ".py"
                self.pytester.makefile(
                    extension,
                    **{str(filepath): content}
                )
            else:
                self.pytester.makepyfile(content)

    def __test_docpath_examples(
        self,
        filename,
        cli_args,
        testplan,
        docpath,
    ):
        docpath = docpath.strip()
        doc_content = self._read_file(docpath, self.request.config.rootpath)
        testfile_content = script_from_examples(doc_content)
        return self.run_pytest(
            (filename, testfile_content),
            cli_args=cli_args,
            testplan=testplan
        )

    def __iter_plugin_args(self):
        for plugin_package in self.enabled_plugins:
            yield "-p"
            yield plugin_package


__all__ = ["AllurePytestRunner"]
