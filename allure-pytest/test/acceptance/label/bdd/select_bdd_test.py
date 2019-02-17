""" ./examples/label/bdd/select_tests_by_bdd.rst """

import pytest
from hamcrest import assert_that, only_contains, any_of, ends_with


@pytest.mark.parametrize(
    ["options", "expected_tests"],
    [
        ({"epics": ["Another Epic"]},
         [
             "test_with_another_epic_feature_story"
         ]),

        ({"features": ["My Feature"]},
         [
             "test_with_epic_feature_story",
             "test_with_epic_feature"
         ]),

        ({"stories": ["My Story", "Another Story"]},
         [
             "test_with_epic_feature_story",
             "test_with_another_epic_feature_story"
         ]),

        ({"stories": ["My Story"], "epics": ["Another Epic"]},
         [
             "test_with_epic_feature_story",
             "test_with_another_epic_feature_story"
         ])

    ]
)
def test_select_by_bdd_label(allured_testdir, options, expected_tests):
    allured_testdir.parse_docstring_path()

    params = []

    for key in options.keys():
        params.append("--allure-{key}".format(key=key))
        params.append(",".join(options[key]))

    allured_testdir.run_with_allure(*params)
    test_cases = [test_case["fullName"] for test_case in allured_testdir.allure_report.test_cases]

    assert_that(test_cases, only_contains(
        any_of(
            *[ends_with(name) for name in expected_tests]
        )
    ))
