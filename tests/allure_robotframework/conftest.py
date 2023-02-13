import shutil
import robot
import json
from pathlib import Path
from pytest import FixtureRequest, Pytester, MonkeyPatch, fixture
from tests.conftest import fake_logger
from typing import Sequence, Mapping
from tests.conftest import RstExampleTable
from allure_robotframework import allure_robotframework

class AllureRobotRunner:
    LOGGER_PATH = "allure_robotframework.robot_listener.AllureFileLogger"

    def __init__(
        self,
        request: FixtureRequest,
        pytester: Pytester,
        monkeypatch: MonkeyPatch
    ) -> None:
        self.request = request
        self.pytester = pytester
        self.monkeypatch = monkeypatch
        self.allure_results = None

    def run_robotframework(
        self,
        suite_paths: Sequence[str|Path] = None,
        suite_literals: Mapping[str, str] = None,
        suite_rst_ids: Sequence[str] = None,
        library_paths: Sequence[str|Path] = None,
        library_literals: Mapping[str, str] = None,
        library_rst_ids: Sequence[str] = None,
        testplan: Mapping[str, any] = None,
        testplan_path: str|Path = None,
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
            suite_paths (Sequence[str|Path]): a sequence of path-like objects
                pointing to .robot files.
            suite_literals (Mapping[str, str]): a mapping from a file name to
                the content of a .robot file (.robot extension can be omitted).
            suite_rst_ids (Mapping[str, str]): a mapping from a file name to an
                ID of a .robot file content from the .rst document, associated
                with current node.
            library_paths (Sequence[str|Path]): a sequence of path-like objects
                pointing to .py library files.
            library_literals (Mapping[str, str]): a mapping from a file name to
                the content of a .py library file (.py extension can be
                omitted).
            library_rst_ids (Mapping[str, str]): a mapping from a file name to
                an IDs of a .py library file content from the .rst document,
                associated with current node.
            testplan (Mapping[str, any]): a testplan content.
            testplan_path (str|Path): a path to a testplan.
            testplan_rst_id (str): a testplan ID from the .rst document,
                associated with current node.
            options (Mapping[str, any]): robot framework options.

        The result of the run is accessible through the :code:`allure_results`
        attribute.
        """

        suites, testplan_path = self.__prepare_example(
            suite_literals=suite_literals,
            suite_paths=suite_paths,
            suite_rst_ids=suite_rst_ids,
            library_literals=library_literals,
            library_paths=library_paths,
            library_rst_ids=library_rst_ids,
            testplan=testplan,
            testplan_path=testplan_path,
            testplan_rst_id=testplan_rst_id,
        )
        if testplan_path:
            self.__run_with_testplan(suites, testplan_path, options)
        else:
            self.__run(suites, options)

    def __resolve_options(self, options):
        return {
            ** {
                "listener": allure_robotframework(None),
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
        library_rst_ids,
        testplan,
        testplan_path,
        testplan_rst_id
    ):
        suites = self.__make_files_from_literals(".robot", suite_literals)
        suites.extend(
            self.__copy_files(suite_paths)
        )
        suites.extend(
            self.__make_all_files_from_rst(".robot", suite_rst_ids)
        )
        self.__make_files_from_literals(".py", library_literals)
        self.__copy_files(library_paths)
        self.__make_all_files_from_rst(".py", library_rst_ids)
        testplan_path = self.__prepare_testplan(
            testplan_path,
            testplan,
            testplan_rst_id
        )
        return suites, testplan_path

    def __run_with_testplan(self, suites, testplan_path, options):
        with self.monkeypatch.setenv("ALLURE_TESTPLAN_PATH", str(testplan_path)):
            self.__run(suites, options)

    def __run(self, suites, options):
        with fake_logger(AllureRobotRunner.LOGGER_PATH) as results:
            options = self.__resolve_options(options)
            robot.run(*suites, **options)
            self.allure_results = results

    def __make_files_from_literals(self, extension, literals):
        return [
            self.pytester.makefile(
                extension,
                **{name: content}
            ) for name, content in (literals or {}).items()
        ]

    def __copy_files(self, src_paths):
        dst_paths = []
        for p in src_paths or []:
            src = self.request.path / p
            dst = self.pytester.path / Path(p).name
            shutil.copyfile(src, dst)
            dst_paths.append(dst)
        return dst_paths

    def __make_all_files_from_rst(self, extension, rst_name_to_id):
        return [
            self.__make_file_from_rst(
                extension,
                name, rst_id
            ) for name, rst_id in (rst_name_to_id or {}).items()
        ]

    def __make_file_from_rst(self, extension, name, rst_id):
        return self.pytester.makefile(
            extension, **{
                name: self.__get_from_rst(rst_id)
            }
        )

    def __get_from_rst(self, rst_id):
        return RstExampleTable.find_examples(self.request)[rst_id]

    def __prepare_testplan(self, content, path, rst_id):
        if content:
            path = self.pytester.makefile(
                ".json",
                json.dumps(content)
            )
        elif rst_id:
            path = self.pytester.makefile(
                ".json",
                self.__get_from_rst(rst_id)
            )
        return path


@fixture
def robot_runner(request, pytester, monkeypatch):
    return AllureRobotRunner(request, pytester, monkeypatch)