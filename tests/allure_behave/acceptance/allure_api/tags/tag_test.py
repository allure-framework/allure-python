""" ./allure-behave/examples/tag.rst """

import pytest
from tests.allure_behave.behave_runner import AllureBehaveRunner
from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_tag


@pytest.mark.parametrize(["feature_id", "scenario", "tags"], [
    pytest.param(
        "tag-scenario-feature",
        "Applying a tag directly to a scenario",
        ["distributed"],
        id="scenario-tag"
    ),
    pytest.param(
        "tag-feature-feature",
        "Applying a tag to a feature",
        ["isolated"],
        id="feature-tag"
    ),
    pytest.param(
        "tag-multiple-feature",
        "Applying multiple tags",
        ["node-1", "node-2", "node-3", "node-4"],
        id="multiple-tags"
    )
])
def test_behave_tags_as_allure_tags(
    feature_id,
    scenario,
    tags,
    behave_runner: AllureBehaveRunner
):
    behave_runner.run_behave(
        feature_rst_ids=[feature_id],
        step_literals=["given('noop')(lambda c:None)"]
    )
    assert_that(
        behave_runner.allure_results,
        has_test_case(
            scenario,
            *(has_tag(tag) for tag in tags)
        )
    )
