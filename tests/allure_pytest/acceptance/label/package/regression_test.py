import textwrap
from hamcrest import assert_that
from hamcrest import ends_with
from tests.conftest import AlluredTestdir
from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_package


def test_path_with_dots_test(allured_testdir: AlluredTestdir):
    path = allured_testdir.testdir.mkpydir("path.with.dots")

    path.joinpath("test_path.py").write_text(
        textwrap.dedent(
            """\
            def test_path_with_dots_test_example():
                pass
            """
        )
    )

    allured_testdir.run_with_allure()

    assert_that(
        allured_testdir.allure_report,
        has_test_case(
            "test_path_with_dots_test_example",
            has_package(ends_with("path.with.dots.test_path"))
        )
    )


def test_with_no_package(allured_testdir: AlluredTestdir):
    """
    >>> def test_package_less(request):
    ...     pass
    """
    allured_testdir.parse_docstring_source()

    allured_testdir.testdir.makeini("""[pytest]""")
    allured_testdir.run_with_allure(allured_testdir.testdir.path)

    assert_that(
        allured_testdir.allure_report,
        has_test_case(
            "test_package_less",
            has_package("test_with_no_package")
        )
    )
