import robot
from pytest import FixtureRequest, Pytester
from tests.e2e import AllureFrameworkRunner, PathlikeT
from typing import Sequence, Mapping
from allure_robotframework import allure_robotframework


class AllureRobotRunner(AllureFrameworkRunner):
    """The runner to test allure-robotframework integration."""

    LOGGER_PATH = "allure_robotframework.robot_listener.AllureFileLogger"

    def __init__(self, request: FixtureRequest, pytester: Pytester):
        super().__init__(request, pytester, AllureRobotRunner.LOGGER_PATH)

    def run_robotframework(
        self,
        suite_paths: Sequence[PathlikeT] = None,
        suite_literals: Mapping[str, str] = None,
        suite_rst_ids: Sequence[str] = None,
        library_paths: Sequence[PathlikeT] = None,
        library_literals: Mapping[str, str] = None,
        library_rst_ids: Sequence[str] = None,
        testplan_content: dict = None,
        testplan_path: PathlikeT = None,
        testplan_rst_id: str = None,
        options: Mapping[str, any] = None
    ) -> None:
        """Runs the robotframework against an example.

        The example consists of suite(s), i.e., .robot files, libraries,
        i.e., .py files and, optionaly, a testplan. All types of files can be
        specified either as paths or as a mapping from a file name to its content
        or as a mapping from a file name to an ID in the associated .rst
        document.

        Arguments:
            suite_paths (Sequence[str | Path]): a sequence of path-like objects
                pointing to .robot files relative to the current test`s folder.
            suite_literals (Mapping[str, str]): a mapping from a file name to
                the content of a .robot file (.robot extension can be omitted).
            suite_rst_ids (Mapping[str, str]): a mapping from a file name to an
                ID of a .robot file content from the .rst document, associated
                with current node.
            library_paths (Sequence[str | Path]): a sequence of path-like
                objects pointing to .py library files relative to the current
                test`s folder.
            library_literals (Mapping[str, str]): a mapping from a file name to
                the content of a .py library file (.py extension can be
                omitted).
            library_rst_ids (Mapping[str, str]): a mapping from a file name to
                an IDs of a .py library file content from the .rst document,
                associated with current node.
            testplan (dict): a testplan content.
            testplan_path (str | Path): a path to a testplan relative to the
                current test`s folder.
            testplan_rst_id (str): a testplan ID from the .rst document,
                associated with current node.
            options (Mapping[str, any]): robot framework options.

        Returns:
            allure_commons.logger.AllureMemoryLogger: the allure results of the
                run. The results of the last run are also accessible through the
                :attr:`allure_results` attribute.
        """
        return self._run(
            self.__prepare_example(
                suite_literals=suite_literals,
                suite_paths=suite_paths,
                suite_rst_ids=suite_rst_ids,
                library_literals=library_literals,
                library_paths=library_paths,
                library_rst_ids=library_rst_ids
            ),
            testplan_content=testplan_content,
            testplan_path=testplan_path,
            testplan_rst_id=testplan_rst_id,
            options=self.__resolve_options(options)
        )

    def _run_framework(self, suites, options):
        robot.run(*suites, listener=allure_robotframework(None), **options)

    def __resolve_options(self, options):
        return {
            ** {
                "log": None,
                "loglevel": "DEBUG",
                "report": None,
                "output": None,
                "extension": "robot",
                "outputdir": str(self.pytester.path)
            },
            ** (options or {})
        }

    def __prepare_example(
        self,
        suite_literals,
        suite_paths,
        suite_rst_ids,
        library_literals,
        library_paths,
        library_rst_ids
    ):
        suites = self._create_files(
            extension=".robot",
            paths=suite_paths,
            literals=suite_literals,
            rst_examples=suite_rst_ids
        )
        self._create_files(
            paths=library_paths,
            literals=library_literals,
            rst_examples=library_rst_ids
        )
        return suites


__all__ = ["AllureRobotRunner"]
