import pytest
from hamcrest import assert_that, has_entry, ends_with, all_of
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_parameter
from allure_commons_test.result import with_excluded
from allure_commons_test.result import with_mode


def params_name(request):
    node_id = request.node.nodeid
    _, name = node_id.rstrip("]").split("[")
    return name


def test_parametrization(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.mark.parametrize("n", [1, 2])
    ... def test_parametrization_example(n):
    ...     assert param
    """

    assert_that(
        executed_docstring_source.allure_report,
        all_of(
            has_test_case(
                "test_parametrization_example[1]",
                has_parameter("n", "1")
            ),
            has_test_case(
                "test_parametrization_example[2]",
                has_parameter("n", "2")
            )
        )
    )


def test_parametrization_with_ids(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.mark.parametrize("v", [1, 2], ids=["a", "b"])
    ... def test_parametrization_with_ids_example(v):
    ...     pass
    """

    assert_that(
        executed_docstring_source.allure_report,
        all_of(
            has_test_case(
                f"test_parametrization_with_ids_example[a]",
                has_parameter("v", "1")
            ),
            has_test_case(
                f"test_parametrization_with_ids_example[b]",
                has_parameter("v", "2")
            )
        )
    )


def test_parametrization_many_decorators(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.mark.parametrize("s", ["a", "b"])
    ... @pytest.mark.parametrize("n", [1, 2])
    ... def test_parametrization_many_decorators_example(n, s):
    ...     pass
    """

    assert_that(
        executed_docstring_source.allure_report,
        all_of(
            has_test_case(
                "test_parametrization_many_decorators_example[1-a]",
                has_parameter("n", "1"),
                has_parameter("s", "'a'")
            ),
            has_test_case(
                "test_parametrization_many_decorators_example[1-b]",
                has_parameter("n", "1"),
                has_parameter("s", "'b'")
            ),
            has_test_case(
                "test_parametrization_many_decorators_example[2-a]",
                has_parameter("n", "2"),
                has_parameter("s", "'a'")
            ),
            has_test_case(
                "test_parametrization_many_decorators_example[2-b]",
                has_parameter("n", "2"),
                has_parameter("s", "'b'")
            )
        )
    )


def test_parametrization_decorators_with_partial_ids(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.mark.parametrize("s", ["a", "b"], ids=["A", "B"])
    ... @pytest.mark.parametrize("n", [1, 2])
    ... def test_two_marks_one_with_ids(n, s):
    ...     pass
    """

    assert_that(
        executed_docstring_source.allure_report,
        all_of(
            has_test_case(
                "test_two_marks_one_with_ids[1-A]",
                has_parameter("n", "1"),
                has_parameter("s", "'a'")
            ),
            has_test_case(
                "test_two_marks_one_with_ids[1-B]",
                has_parameter("n", "1"),
                has_parameter("s", "'b'")
            ),
            has_test_case(
                "test_two_marks_one_with_ids[2-A]",
                has_parameter("n", "2"),
                has_parameter("s", "'a'")
            ),
            has_test_case(
                "test_two_marks_one_with_ids[2-B]",
                has_parameter("n", "2"),
                has_parameter("s", "'b'")
            )
        )
    )


def test_dynamic_parameter_add(executed_docstring_source):
    """
    >>> import allure

    >>> def test_parameter_add():
    ...     allure.dynamic.parameter("param1", "param-value")
    """
    assert_that(
        executed_docstring_source.allure_report,
        has_test_case(
            "test_parameter_add",
            has_parameter("param1", "'param-value'")
        )
    )


def test_dynamic_parameter_excluded(executed_docstring_source):
    """
    >>> import allure

    >>> def test_parameter_excluded():
    ...     allure.dynamic.parameter("param1", "param-value", excluded=True)
    """

    assert_that(
        executed_docstring_source.allure_report,
        has_test_case(
            "test_parameter_excluded",
            has_parameter(
                "param1",
                "'param-value'",
                with_excluded()
            )
        )
    )


def test_dynamic_parameter_mode(executed_docstring_source):
    """
    >>> import allure

    >>> def test_parameter_mode():
    ...     allure.dynamic.parameter("param1", "param-value", mode=allure.parameter_mode.MASKED)
    """

    assert_that(
        executed_docstring_source.allure_report,
        has_test_case(
            "test_parameter_mode",
            has_parameter(
                "param1",
                "'param-value'",
                with_mode('masked')
            )
        )
    )


def test_dynamic_parameter_override(executed_docstring_source):
    """
    >>> import pytest
    ... import allure

    >>> @pytest.mark.parametrize("param1", [object()], ids=["param-id"])
    ... def test_parameter_override(param1):
    ...     allure.dynamic.parameter("param1", "readable-value")
    """
    assert_that(
        executed_docstring_source.allure_report,
        has_test_case(
            "test_parameter_override[param-id]",
            has_parameter("param1", "'readable-value'")
        )
    )


def test_dynamic_parameter_override_from_fixture(executed_docstring_source):
    """
    >>> import pytest
    ... import allure


    >>> @pytest.fixture()
    ... def fixt():
    ...     allure.dynamic.parameter("param1", "readable-value")

    >>> @pytest.mark.parametrize("param1", [object()], ids=["param-id"])
    ... def test_parameter_override_from_fixture(fixt, param1):
    ...     pass
    """
    assert_that(
        executed_docstring_source.allure_report,
        has_test_case(
            "test_parameter_override_from_fixture[param-id]",
            has_parameter("param1", "'readable-value'")
        )
    )


def test_fullname_with_braces(executed_docstring_source):
    """
    >>> import pytest
    ... import allure

    >>> class TestClass:
    ...     @pytest.mark.parametrize("param1", ["qwe]["])
    ...     def test_with_braces(self, param1):
    ...         pass
    """

    assert_that(
        executed_docstring_source.allure_report,
        has_test_case(
            "test_with_braces[qwe][]",
            has_entry(
                'fullName',
                ends_with(".TestClass#test_with_braces")
            ),
            has_parameter("param1", "'qwe]['")
        )
    )
