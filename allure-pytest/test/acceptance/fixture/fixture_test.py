import pytest
import allure
from hamcrest import assert_that, not_
from allure_commons_test.report import has_test_case
from allure_commons_test.container import has_container, has_before, has_after
from allure_commons_test.result import has_step
from itertools import combinations_with_replacement

fixture_scopes = ["session", "module", "class", "function"]


@allure.feature("Fixture")
@pytest.mark.parametrize("first_scope", fixture_scopes)
@pytest.mark.parametrize("second_scope", fixture_scopes)
def test_fixture(allured_testdir, first_scope, second_scope):
    allured_testdir.testdir.makepyfile("""
        import pytest

        @pytest.fixture(scope="{first_scope}")
        def first_fixture():
            pass

        @pytest.fixture(scope="{second_scope}")
        def second_fixture():
            pass

        def test_fixture_example(first_fixture, second_fixture):
            pass
    """.format(first_scope=first_scope, second_scope=second_scope))

    allured_testdir.run_with_allure()

    assert_that(allured_testdir.allure_report,
                has_test_case("test_fixture_example",
                              has_container(allured_testdir.allure_report,
                                            has_before("first_fixture")
                                            ),
                              has_container(allured_testdir.allure_report,
                                            has_before("second_fixture"),
                                            )
                              )
                )


@pytest.mark.parametrize(
    ["parent_scope", "child_scope"],
    list(combinations_with_replacement(fixture_scopes, 2))
)
def test_nested_fixture(allured_testdir, parent_scope, child_scope):
    allured_testdir.testdir.makepyfile("""
        import pytest

        @pytest.fixture(scope="{parent_scope}")
        def parent_fixture():
            pass

        @pytest.fixture(scope="{child_scope}")
        def child_fixture(parent_fixture):
            pass

        def test_nested_fixture_example(child_fixture):
            pass

        def test_fixture_used_in_other_fixtures_example(parent_fixture):
            pass

    """.format(parent_scope=parent_scope, child_scope=child_scope))

    allured_testdir.run_with_allure()

    assert_that(allured_testdir.allure_report,
                has_test_case("test_nested_fixture_example",
                              has_container(allured_testdir.allure_report,
                                            has_before("parent_fixture")
                                            ),
                              has_container(allured_testdir.allure_report,
                                            has_before("child_fixture"),
                                            )
                              )
                )

    assert_that(allured_testdir.allure_report,
                has_test_case("test_fixture_used_in_other_fixtures_example",
                              has_container(allured_testdir.allure_report,
                                            has_before("parent_fixture")
                                            ),
                              not_(has_container(allured_testdir.allure_report,
                                                 has_before("child_fixture"),
                                                 )
                                   )
                              )
                )


@allure.feature("Fixture")
def test_nested_fixtures(executed_docstring_source):
    """
    >>> import pytest

    If we have two fixtures:
    >>> @pytest.fixture
    ... def first_fixture():
    ...     pass


    >>> @pytest.fixture
    ... def second_fixture():
    ...     pass

    And one that uses both previous:
    >>> @pytest.fixture
    ... def child_fixture(first_fixture, second_fixture):
    ...     pass

    For next test, allure report will contain all tree fixtures:
    >>> def test_nested_fixtures_example(child_fixture):
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_nested_fixtures_example",
                              has_container(executed_docstring_source.allure_report,
                                            has_before("first_fixture")
                                            ),
                              has_container(executed_docstring_source.allure_report,
                                            has_before("second_fixture"),
                                            ),
                              has_container(executed_docstring_source.allure_report,
                                            has_before("child_fixture"),
                                            )
                              )
                )


@allure.feature("Fixture")
def test_fixture_allure_title(allured_testdir):
    allured_testdir.testdir.makepyfile("""
        import pytest
        import allure

        @pytest.fixture
        @allure.title("Allure fixture title")
        def first_fixture():
            pass

        def test_titled_fixture_example(first_fixture):
            pass
    """)

    allured_testdir.run_with_allure()

    assert_that(allured_testdir.allure_report,
                has_test_case("test_titled_fixture_example",
                              has_container(allured_testdir.allure_report,
                                            has_before("Allure fixture title")
                                            )
                              )
                )


@allure.feature("Fixture")
def test_fixture_allure_title_before(allured_testdir):
    allured_testdir.testdir.makepyfile("""
        import pytest
        import allure

        @allure.title("Allure fixture title")
        @pytest.fixture
        def first_fixture():
            pass

        def test_titled_before_fixture_example(first_fixture):
            pass
    """)

    allured_testdir.run_with_allure()

    assert_that(allured_testdir.allure_report,
                has_test_case("test_titled_before_fixture_example",
                              has_container(allured_testdir.allure_report,
                                            has_before("Allure fixture title")
                                            )
                              )
                )


def test_titled_fixture_from_conftest(allured_testdir):
    allured_testdir.testdir.makeconftest("""
        import allure
        import pytest

        @allure.title('Titled fixture before pytest.fixture')
        @pytest.fixture
        def first_fixture():
            pass

        @pytest.fixture
        @allure.title('Titled fixture after pytest.fixture')
        def second_fixture():
            pass
    """)

    allured_testdir.testdir.makepyfile("""
        def test_with_titled_conftest_fixtures(first_fixture, second_fixture):
            pass
    """)

    allured_testdir.run_with_allure()

    assert_that(allured_testdir.allure_report,
                has_test_case("test_with_titled_conftest_fixtures",
                              has_container(allured_testdir.allure_report,
                                            has_before("Titled fixture before pytest.fixture")
                                            ),
                              has_container(allured_testdir.allure_report,
                                            has_before("Titled fixture after pytest.fixture")
                                            )
                              )
                )


def test_fixture_override(allured_testdir):
    allured_testdir.testdir.makeconftest("""
        import pytest
        import allure

        @pytest.fixture
        def my_fixture():
            with allure.step('Step in before in original fixture'):
                pass
            yield
            with allure.step('Step in after in original fixture'):
                pass

    """)

    allured_testdir.testdir.makepyfile("""
        import pytest
        import allure

        @pytest.fixture
        def my_fixture(my_fixture):
            with allure.step('Step in before in redefined fixture'):
                pass
            yield
            with allure.step('Step in after in redefined fixture'):
                pass

        def test_with_redefined_fixture(my_fixture):
            pass
    """)

    allured_testdir.run_with_allure()

    assert_that(allured_testdir.allure_report,
                has_test_case("test_with_redefined_fixture",
                              has_container(allured_testdir.allure_report,
                                            has_before("my_fixture",
                                                       has_step("Step in before in original fixture")
                                                       ),
                                            has_after("my_fixture::0",
                                                      has_step("Step in after in original fixture")
                                                      )
                                            ),
                              has_container(allured_testdir.allure_report,
                                            has_before("my_fixture",
                                                       has_step("Step in before in redefined fixture")
                                                       ),
                                            has_after("my_fixture::0",
                                                      has_step("Step in after in redefined fixture")
                                                      )
                                            ),
                              )
                )
