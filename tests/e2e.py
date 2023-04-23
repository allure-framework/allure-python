"""Utility functions and classes for end-to-end testing of allure integrations
with python testing frameworks.

"""

import docutils
import docutils.nodes
import docutils.parsers.rst
import json
import mock
import pytest
import shutil
import warnings
from abc import abstractmethod
from contextlib import contextmanager, ExitStack
from pathlib import Path
from pytest import FixtureRequest, Pytester, MonkeyPatch
from typing import Tuple, Mapping, TypeVar, Generator, Callable, Union

import allure_commons
from allure_commons.logger import AllureMemoryLogger
from allure_commons_test.report import AllureReport


PathlikeT = Union[str, Path]


@contextmanager
def altered_env(**kwargs) -> Generator[MonkeyPatch, None, None]:
    mp = MonkeyPatch()
    for n, v in kwargs.items():
        if v is None:
            mp.delenv(n, False)
        else:
            mp.setenv(n, str(v))
    yield mp
    mp.undo()


@contextmanager
def allure_plugin_context():
    """Separates an allure integration under test from currently active
    allure integration (if eny).

    """

    outer_context_plugins = __pop_all_allure_plugins()

    yield

    __pop_all_allure_plugins()
    __restore_allure_plugins(outer_context_plugins)


@contextmanager
def allure_in_memory_context(
    *paths: str
) -> Generator[AllureMemoryLogger, None, None]:
    """Creates a context to test an allure integration.

    While a testing context is active the following conditions hold:

    #. Allure's output is stored in memory instead of being written to the file
       system.
    #. Allure plugins of an integration under test are isolated from the
       allure plugins of the executing environment (if allure is active).

    When the testing context is deactivated, all allure plugins registered
    during the test are removed and the plugins of the execution environment are
    restored.

    Arguments:
        *paths (str): paths to classes to replace with the in-memory logger in
            addition to :code:`"allure_commons.logger.AllureFileLogger"`.
            Provide these if the integration under test imports the logger using
            the :code:`from allure_commons.logger import AllureFileLogger`
            syntax.

    Yields:
        AllureMemoryLogger: an instance of the in-memory logger, where the
            output is collected.

    """

    # Plugin context must be set first, because mock patching may cause
    # module loading, thus, side effects, including allure decorators evaluation
    # (and that requires all plugins of nested allure to already be in place).
    paths = ("allure_commons.logger.AllureFileLogger",) + paths
    with allure_plugin_context():
        logger = AllureMemoryLogger()
        with ExitStack() as stack:
            for path in paths:
                stack.enter_context(
                    mock.patch(path)
                ).return_value = logger
            yield logger


class AllureFileContextValue:
    def __init__(self):
        self.allure_results = None


@contextmanager
def allure_file_context(
    alluredir: PathlikeT
) -> Generator[AllureFileContextValue, None, None]:
    """Creates a context to test an allure integration.

    It behaves in a way similar to :func:`allure_in_memory_context` except that
    the result is created from the actual allure output files. It is useful
    if the result files are generated in a separate process.

    Arguments:
        alluredir (str | Path): a path to allure results directory.

    The report can be accessed through the :attr:`AllureFileContextValue.output`
    attribute once the context is exited.

    Example:

        >>> with allure_file_context("./allure-results") as v:
        ...     # run framework with allure integration
        >>> # use v.allure_results to access the results

    """

    with allure_plugin_context():
        value = AllureFileContextValue()
        yield value
        value.allure_results = AllureReport(alluredir)


def find_node_with_docstring(
    request: FixtureRequest
) -> Union[Tuple[pytest.Item, str], Tuple[None, None]]:
    """Find a docstring associated with a test function.

    It first checks the function itself and then, if no docstring was found,
    moves up the hierarchy until either a docstring is found or no parent nodes
    left.

    Returns:
        A tuple of a node and its docstring or :code:`(None, None)` if no
            docstring is found.

    """

    node = request.node
    while node:
        docstring = getattr(node, "obj", None).__doc__
        if docstring:
            break
        node = node.parent
    return node, docstring


def find_node_with_docstring_or_throw(
    request: FixtureRequest
) -> Tuple[pytest.Item, str]:
    """Find a docstring associated with a test function.

    It first checks the function itself and then, if no docstring was found,
    moves up the hierarchy until either a docstring is found or no parent nodes
    left.

    Raises:
        ValueError: if the docstring doesn't exist.

    Returns:
        A tuple of a node and its docstring.

    """
    node, docstring = find_node_with_docstring(request)
    if node is None:
        nodeid = request.node.nodeid
        raise ValueError(f"Unable to get docstring for node {nodeid}")
    return node, docstring


def get_path_from_docstring(request: FixtureRequest) -> Path:
    """Extract a path to a file or folder from a docstring of a test function or
    one of its parents.

    The path is joined to the rootpath.

    Raises:
        ValueError: if no docstring specified.

    Returns:
        Path: a full path path denoted by the docstring.

    """
    return request.config.rootpath.joinpath(
        find_node_with_docstring_or_throw(request)[1].strip()
    )


RstExampleTableT = TypeVar("RstExampleTableT", bound="RstExampleTable")


class RstExampleTable:
    """Examples from a .rst document associated with a test.

    Attributes:
        STASH_KEY (pytest.StashKey): (class attribute) a pytest stash key to
            cache an instance of this class on node, that established the
            association with the document.
        source (str | Path): a path to a document the table was created from.
        examples (Mapping[str, str]): a mapping from an example name to its
            content.

    """

    STASH_KEY = pytest.StashKey()

    def __init__(self, filepath: PathlikeT) -> None:
        """Create a table of examples from a .rst document.

        Arguments:
            filepath (str | Path): a path to a .rst document to parse.

        """
        self.source = filepath
        self.examples = self.__load_examples(filepath)

    def __getitem__(self, name: str) -> str:
        """Find an example in the document by its name.

        An example is represented by a code block in the original document. The
        name of the example is specified using the :code:`:name:` option of the
        code block.

        Arguments:
            name (str): a name of an example.

        Raises:
            KeyError: the required example doesn't exist in the document.

        Returns:
            str: the content of the example.
        """
        if name not in self.examples:
            raise KeyError(f"Code block {name!r} not found in {self.source}")
        return self.examples[name]

    @staticmethod
    def find_examples(request: FixtureRequest) -> RstExampleTableT:
        """Loads code examples, associated with the test node or one of its
        parents.

        Arguments:
            request (FixtureRequest): the request fixture.

        Returns (RstExampleTable): A table containing the examples, indexed by
            their names from the .rst document

        Notes:
            It first finds a docstring defined on the function, class, module or
            package associated with the node. If multiple docstrings exist,
            the one defined on a lower level wins.

            The docstring content is used then as the path to the
            reStructuredText document. The document is parsed and all its code
            blocks are combined in a dictionary that maps their names to the
            code block content. The mapping can be accessed through the returned
            instance of RstExampleTable class.

            The table is then cached in a stash of the same node from which the
            original docstring was loaded. This prevents from parsing the same
            document several times if multiple tests from the same module/package
            (or parametrizations of the same metafunc) are testing the examples
            from the same document.
        """

        node, docstring = find_node_with_docstring_or_throw(
            request
        )
        examples = RstExampleTable.__get_from_cache(node)
        if examples is None:
            examples = RstExampleTable.__create_and_cache(node, docstring)
        return examples

    @staticmethod
    def __load_examples(filepath: PathlikeT) -> Mapping[str, str]:
        document = RstExampleTable.parse_rst(filepath)
        return {
            name: code_block.astext()
            for code_block in document.findall(
                RstExampleTable.__filter
            ) for name in code_block["names"]
        }

    @staticmethod
    def parse_rst(filepath: PathlikeT) -> docutils.nodes.document:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            parser = docutils.parsers.rst.Parser()
            components = (docutils.parsers.rst.Parser,)
            settings = docutils.frontend.OptionParser(
                components=components
            ).get_default_values()
            document = docutils.utils.new_document(
                str(filepath),
                settings=settings
            )
            with open(filepath, encoding="utf-8") as f:
                content = f.read()
            parser.parse(content, document)
            return document

    @staticmethod
    def __get_from_cache(node):
        if RstExampleTable.STASH_KEY in node.stash:
            return node.stash[RstExampleTable.STASH_KEY]

    @staticmethod
    def __create_and_cache(node, path):
        filepath = node.config.rootpath.joinpath(path.strip())
        if not filepath.exists() or filepath.is_dir():
            raise ValueError(
                f"Document, referred by {node.nodeid}, "
                f"doesn't exist at {filepath}"
            )
        table = RstExampleTable(filepath)
        node.stash[RstExampleTable.STASH_KEY] = table
        return table

    @staticmethod
    def __filter(node):
        return isinstance(
            node,
            docutils.nodes.literal_block
        ) and "code" in node["classes"] and node["names"]


class AllureFrameworkRunner:
    """An abstract base class for framework test runners to test allure
    integrations.

    Attributes:
        request (FixtureRequest): an instance of the request fixture.
        pytester (Pytester): an instance of the pytester fixture.
        allure_results (AllureMemoryLogger | AllureReport): the latest collected
            allure results.
        in_memory (bool): if `True`, the next run collects the results in memory
            (:attr:`AllureFrameworkRunner.allure_results` is AllureMemoryLogger).
            Otherwise, the next run creates allure result files and collects the
            report from them
            (:attr:`AllureFrameworkRunner.allure_results` is AllureReport).
        *imported_logger_paths: a sequence of paths to provide to
            :func:`allure_in_memory_context`.

    """
    def __init__(
        self,
        request: FixtureRequest,
        pytester: Pytester,
        *imported_logger_paths
    ):
        self.request = request
        self.pytester = pytester
        self.allure_results = None
        self.in_memory = True
        self.imported_logger_paths = list(imported_logger_paths)

    def _run(
        self,
        *args,
        testplan_content: dict = None,
        testplan_path: PathlikeT = None,
        testplan_rst_id: str = None,
        **kwargs
    ) -> AllureMemoryLogger:
        """Runs the framework and collect the allure results.

        Prepares the testplan (if any), replace the allure file logger with the
        in-memory logger and runs the :method:`_run_framework` method.

        Arguments:
            *args: positional arguments for the underlying call.

        Keyword arguments:
            testplan_content (dict): the content of the allure testplan.
            testplan_path (str | Path): the path to the allure testplan
                relative to the current test folder.
            testplan_rst_id (str): the ID of the allure testplan code block.
            **kwargs: keyword arguments for the underlying call.

        Returns:
            AllureMemoryLogger: the collected allure results. The results of the
                last call are also available in the :attr:`allure_results`
                attribute.

        """
        testplan_path = self.__prepare_testplan(
            content=testplan_content,
            path=testplan_path,
            rst_id=testplan_rst_id
        )
        with altered_env(ALLURE_TESTPLAN_PATH=testplan_path):
            output = self.__run_and_collect_results_in_memory(
                args,
                kwargs
            ) if self.in_memory else self.__run_and_collect_results_from_fs(
                args,
                kwargs
            )
            self.allure_results = output
            return output

    @abstractmethod
    def _run_framework(self, *args, **kwargs):
        """Override this method and invoke the actual framework.

        This method is invoked by the :method:`_run`. Arguments (args and kwargs
        are the same as were provided to the :method:`_run`.

        """

    def _find_docstring(self):
        """Find a docstring, associated with the test ot throw."""
        return find_node_with_docstring_or_throw(self.request)[1]

    def _get_all_content(self, paths=None, literals=None, rst_ids=None):
        """Return a list of content denoted by files, literals and IDs of the
            .rst document code blocks.

        Arguments:
            paths (Sequence[str | Path]): a sequence of file paths (relative to
                the current test's directory) to load content from.
            literals (Sequence[str]): a sequence of literals to use as content.
            rst_ids (Sequence[str]): a sequence of code blocks from the .rst
                document.

        Returns:
            List[str]: a list of strings, each representing a file content.

        """

        return [
            self._read_file(p) for p in (paths or [])
        ] + list(literals or []) + [
            self.__get_from_rst(rst_id) for rst_id in (rst_ids or [])
        ]

    def _resolve_content(self, path=None, literal=None, rst_id=None):
        """Return content denoted either by a literal or a path (relative to
            the test folder) or an ID of the .rst document code block in that
            order. The first content source wins.

        """
        if literal:
            return literal
        if path:
            return self._read_file(path)
        if rst_id:
            return self.__get_from_rst(rst_id)

    def _create_files(
        self,
        extension=".py",
        paths=None,
        literals=None,
        rst_examples=None
    ):
        """Create and/or copy files in the pytester directory.

        Arguments:
            extension (str): an output files extension.
            paths (Sequence[str | Path]): a sequence of paths to copy,
                relative to the current test directory.
            literals (Mapping[str, str]): a mapping from a name of a file to
                its content (an extension can be omitted).
            rst_examples (Mapping[str, str]): a mapping from a file name (an
                extension may be omitted) to its ID in the .rst document.

        Returns:
            List[Path]: a list of the newly created file paths.
        """
        return self._copy_files(paths) + self._make_files_from_literals(
            extension,
            literals
        ) + self._make_files_from_rst(extension, rst_examples)

    def _make_files_from_literals(self, extension, literals):
        """Create files in the pytester directory.

        Arguments:
            extension (str): an output files extension.
            literals (Mapping[str, str]): a mapping from a name of a file to
                its content (an extension can be omitted).

        Returns:
            List[Path]: a list of the newly created file paths.
        """

        return [
            self.pytester.makefile(
                extension,
                **{name: content}
            ) for name, content in (literals or {}).items()
        ]

    def _copy_files(self, src_paths):
        """Copy files denoted by paths into the pytester directory.

        Arguments:
            src_paths (Sequence[str | Path]): a sequence of paths to copy,
                relative to the current test directory.

        Returns:
            List[Path]: a list of the newly created file paths.
        """
        dst_paths = []
        for p in src_paths or []:
            src = self.request.path.parent / p
            dst = self.pytester.path / Path(p).name
            shutil.copyfile(src, dst)
            dst_paths.append(dst)
        return dst_paths

    def _make_files_from_rst(
        self,
        extension: str,
        rst_name_to_id: Mapping[str, str]
    ):
        """Copy code blocks from the .rst document to the pytester dir.

        Arguments:
            extension (str): an output files extension.
            rst_name_to_id (Mapping[str, str]): a mapping from a file name (an
                extension may be omitted) to its ID in the .rst document.

        Returns:
            List[Path]: a list of the newly created file paths.
        """

        return [
            self.__make_single_file_from_rst(
                extension,
                name, rst_id
            ) for name, rst_id in (rst_name_to_id or {}).items()
        ]

    def _read_file(self, path: PathlikeT, basepath: PathlikeT = None):
        """Read file content.

        Arguments:
            path (str | Path): a path to a file. If it's a relative path, it's
                prepended by the basepath.
            basepath (str | Path): a basepath. The path to the folder of the
                current test by default.

        """
        if basepath is None:
            basepath = self.request.path.parent
        path = basepath / path
        with open(path, mode="r", encoding="utf-8") as f:
            return f.read()

    def _cache_docstring_test_result(
        self,
        cache_key: pytest.StashKey,
        test_fn: Callable,
        *args: any,
        **kwargs: any
    ):
        """Gets docstring run results from the cache of the node associated with
        the docstring. In case of a cache miss, returns
        :code:`run_fn(*args, docstring, **kwargs)`. The result is cached to
        avoid future calls.

        Arguments:
            cache_key (pytest.StashKey): a pytest stash key used to cache the
                result.
            run_fn (Callable): a function to call in case of a cache miss. The
                docstring is appended to the positional arguments.
            *args: positional arguments of the :param:`run_fn`.
            **kwargs: keyword arguments of the :param:`run_fn`.

        Returns:
            The result of the :code:`run_fn(*args, docstring, **kwargs)` call,
            either from the cache or from the actual call.
        """

        node, docstring = find_node_with_docstring_or_throw(self.request)
        if cache_key in node.stash:
            return node.stash[cache_key]
        result = test_fn(*args, docstring, **kwargs)
        node.stash[cache_key] = result
        return result

    def __run_and_collect_results_in_memory(self, args, kwargs):
        with allure_in_memory_context(*self.imported_logger_paths) as output:
            self._run_framework(*args, **kwargs)
            return output

    def __run_and_collect_results_from_fs(self, args, kwargs):
        with allure_file_context(self.pytester.path) as v:
            self._run_framework(*args, **kwargs)
        return v.allure_results

    def __make_single_file_from_rst(self, extension, name, rst_id):
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


def __pop_all_allure_plugins():
    name_plugin_tuples = allure_commons.plugin_manager.list_name_plugin()
    for name, plugin in name_plugin_tuples:
        allure_commons.plugin_manager.unregister(plugin=plugin, name=name)
    return name_plugin_tuples


def __restore_allure_plugins(name_plugin_tuples):
    for name, plugin in name_plugin_tuples:
        allure_commons.plugin_manager.register(plugin, name)
