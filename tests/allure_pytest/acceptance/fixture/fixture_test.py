import pytest
from hamcrest import assert_that, not_, all_of
from itertools import combinations_with_replacement
from tests.allure_pytest.pytest_runner import AllurePytestRunner

import allure
from allure_commons_test.report import has_test_case
from allure_commons_test.container import has_container, has_before, has_after
from allure_commons_test.result import has_step

fixture_scopes = ["session", "module", "class", "function"]


@allure.feature("Fixture")
@pytest.mark.parametrize("first_scope", fixture_scopes)
@pytest.mark.parametrize("second_scope", fixture_scopes)
def test_fixture(allure_pytest_runner: AllurePytestRunner, first_scope, second_scope):
    testfile_content = (
        f"""
        import pytest

        @pytest.fixture(scope="{first_scope}")
        def first_fixture():
            pass

        @pytest.fixture(scope="{second_scope}")
        def second_fixture():
            pass

        def test_fixture_example(first_fixture, second_fixture):
            pass
        """
    )

    allure_results = allure_pytest_runner.run_pytest(testfile_content)

    assert_that(
        allure_results,
        has_test_case(
            "test_fixture_example",
            has_container(allure_results, has_before("first_fixture")),
            has_container(allure_results, has_before("second_fixture"))
        )
    )


@pytest.mark.parametrize(
    ["parent_scope", "child_scope"],
    list(combinations_with_replacement(fixture_scopes, 2))
)
def test_nested_fixture(allure_pytest_runner: AllurePytestRunner, parent_scope, child_scope):
    testfile_content = (
        f"""
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
        """
    )

    allure_results = allure_pytest_runner.run_pytest(testfile_content)

    assert_that(
        allure_results,
        has_test_case(
            "test_nested_fixture_example",
            has_container(allure_results, has_before("parent_fixture")),
            has_container(allure_results, has_before("child_fixture"))
        )
    )

    assert_that(
        allure_results,
        has_test_case(
            "test_fixture_used_in_other_fixtures_example",
            has_container(allure_results, has_before("parent_fixture")),
            not_(has_container(allure_results, has_before("child_fixture")))
        )
    )


@allure.feature("Fixture")
def test_nested_fixtures(allure_pytest_runner: AllurePytestRunner):
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

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_nested_fixtures_example",
            has_container(allure_results, has_before("first_fixture")),
            has_container(allure_results, has_before("second_fixture")),
            has_container(allure_results, has_before("child_fixture"))
        )
    )


@allure.feature("Fixture")
def test_fixture_allure_title(allure_pytest_runner: AllurePytestRunner):
    testfile_content = (
        """
        import pytest
        import allure

        @pytest.fixture
        @allure.title("Allure fixture title")
        def first_fixture():
            pass

        def test_titled_fixture_example(first_fixture):
            pass
        """
    )

    allure_results = allure_pytest_runner.run_pytest(testfile_content)

    assert_that(
        allure_results,
        has_test_case(
            "test_titled_fixture_example",
            has_container(
                allure_results,
                has_before("Allure fixture title")
            )
        )
    )


@allure.feature("Fixture")
def test_fixture_allure_title_before(allure_pytest_runner: AllurePytestRunner):
    testfile_content = (
        """
        import pytest
        import allure

        @allure.title("Allure fixture title")
        @pytest.fixture
        def first_fixture():
            pass

        def test_titled_before_fixture_example(first_fixture):
            pass
        """
    )

    allure_results = allure_pytest_runner.run_pytest(testfile_content)

    assert_that(
        allure_results,
        has_test_case(
            "test_titled_before_fixture_example",
            has_container(
                allure_results,
                has_before("Allure fixture title")
            )
        )
    )


def test_titled_fixture_from_conftest(allure_pytest_runner: AllurePytestRunner):
    conftest_content = (
        """
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
        """
    )

    testfile_content = (
        """
        def test_with_titled_conftest_fixtures(first_fixture, second_fixture):
            pass
        """
    )

    allure_results = allure_pytest_runner.run_pytest(
        testfile_content,
        conftest_literal=conftest_content
    )

    assert_that(
        allure_results,
        has_test_case(
            "test_with_titled_conftest_fixtures",
            has_container(
                allure_results,
                has_before("Titled fixture before pytest.fixture")
            ),
            has_container(
                allure_results,
                has_before("Titled fixture after pytest.fixture")
            )
        )
    )


def test_fixture_override(allure_pytest_runner: AllurePytestRunner):
    conftest_content = (
        """
        import pytest
        import allure

        @pytest.fixture
        def my_fixture():
            with allure.step('Step in before in original fixture'):
                pass
            yield
            with allure.step('Step in after in original fixture'):
                pass

        """
    )

    testfile_content = (
        """
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
        """
    )

    allure_results = allure_pytest_runner.run_pytest(
        testfile_content,
        conftest_literal=conftest_content
    )

    assert_that(
        allure_results,
        has_test_case(
            "test_with_redefined_fixture",
            has_container(
                allure_results,
                has_before(
                    "my_fixture",
                    has_step("Step in before in original fixture")
                ),
                has_after(
                    "my_fixture::0",
                    has_step("Step in after in original fixture")
                )
            ),
            has_container(
                allure_results,
                has_before(
                    "my_fixture",
                    has_step("Step in before in redefined fixture")
                ),
                has_after(
                    "my_fixture::0",
                    has_step("Step in after in redefined fixture")
                )
            )
        )
    )


@pytest.mark.parametrize(
    ["parent_scope", "child_scope"],
    list(combinations_with_replacement(fixture_scopes, 2))
)
def test_dynamically_called_fixture(
    allure_pytest_runner: AllurePytestRunner,
    parent_scope,
    child_scope
):
    testfile_content = (
        f"""
        import pytest

        @pytest.fixture(scope="{parent_scope}", autouse=True)
        def parent_auto_call_fixture():
            yield

        @pytest.fixture(scope="{child_scope}")
        def child_manual_call_fixture():
            yield

        @pytest.fixture(scope="{parent_scope}")
        def parent_dyn_call_fixture():
            yield

        @pytest.fixture(scope="{child_scope}")
        def child_dyn_call_fixture(request):
            request.getfixturevalue('parent_dyn_call_fixture')

        def test_one(child_manual_call_fixture):
            pass

        def test_two(request):
            request.getfixturevalue('child_dyn_call_fixture')

        def test_three(request):
            request.getfixturevalue('parent_dyn_call_fixture')
        """
    )

    allure_results = allure_pytest_runner.run_pytest(testfile_content)

    assert_that(
        allure_results,
        all_of(
            has_test_case(
                "test_one",
                has_container(
                    allure_results,
                    has_before("parent_auto_call_fixture"),
                    has_after("parent_auto_call_fixture::0")
                ),
                has_container(
                    allure_results,
                    has_before("child_manual_call_fixture"),
                    has_after("child_manual_call_fixture::0")
                ),
                not_(
                    has_container(
                        allure_results,
                        has_before("parent_dyn_call_fixture"),
                        has_after("parent_dyn_call_fixture::0")
                    ),
                ),
                not_(
                    has_container(
                        allure_results,
                        has_before("child_dyn_call_fixture")
                    ),
                )
            ),
            has_test_case(
                "test_two",
                has_container(
                    allure_results,
                    has_before("parent_auto_call_fixture"),
                    has_after("parent_auto_call_fixture::0")
                ),
                not_(
                    has_container(
                        allure_results,
                        has_before("child_manual_call_fixture"),
                        has_after("child_manual_call_fixture::0")
                    ),
                ),
                has_container(
                    allure_results,
                    has_before("parent_dyn_call_fixture"),
                    has_after("parent_dyn_call_fixture::0")
                ),
                has_container(
                    allure_results,
                    has_before("child_dyn_call_fixture")
                )
            ),
            has_test_case(
                "test_three",
                has_container(
                    allure_results,
                    has_before("parent_auto_call_fixture"),
                    has_after("parent_auto_call_fixture::0")
                ),
                not_(
                    has_container(
                        allure_results,
                        has_before("child_manual_call_fixture"),
                        has_after("child_manual_call_fixture::0")
                    ),
                ),
                has_container(
                    allure_results,
                    has_before("parent_dyn_call_fixture"),
                    has_after("parent_dyn_call_fixture::0")
                ),
                not_(
                    has_container(
                        allure_results,
                        has_before("child_dyn_call_fixture")
                    )
                )
            )
        )
    )


def test_one_fixture_on_two_tests(allure_pytest_runner: AllurePytestRunner):
    testfile_content = (
        """
        import pytest
        import allure

        @pytest.fixture
        def fixture(request):
            with allure.step(request.node.name):
                pass

        class TestClass:
            def test_first(self, fixture):
                pass

            def test_second(self, fixture):
                pass
        """
    )
    allure_results = allure_pytest_runner.run_pytest(testfile_content)

    assert_that(
        allure_results,
        all_of(
            has_test_case(
                "test_first",
                has_container(
                    allure_results,
                    has_before(
                        "fixture",
                        has_step("test_first")
                    )
                ),
                not_(
                    has_container(
                        allure_results,
                        has_before(
                            "fixture",
                            has_step("test_second")
                        )
                    )
                )
            ),
            has_test_case(
                "test_second",
                has_container(
                    allure_results,
                    has_before(
                        "fixture",
                        has_step("test_second")
                    )
                ),
                not_(
                    has_container(
                        allure_results,
                        has_before(
                            "fixture",
                            has_step("test_first")
                        )
                    )
                )
            )
        )
    )
