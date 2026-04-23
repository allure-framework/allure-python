import allure
from tests.allure_behave.behave_runner import AllureBehaveRunner as Runner
from hamcrest import assert_that, all_of, not_, equal_to
from allure_commons_test.container import has_container, has_before, has_after
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_attachment_with_content
from allure_commons_test.result import has_step


def test_global_hooks(behave_runner: Runner):
    behave_runner.run_behave(
        feature_paths=["./test-data/global-hooks.feature"],
        step_paths=["./test-data/steps.py"],
        environment_path="./test-data/global-hooks.py"
    )
    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Global hooks as fixtures",
            with_status("passed"),
            has_container(
                behave_runner.allure_results,
                has_before("before all", with_status("passed"))
            ),
            has_container(
                behave_runner.allure_results,
                has_before("before feature", with_status("passed"))
            ),
            has_container(
                behave_runner.allure_results,
                has_before("before scenario", with_status("passed"))
            ),
            has_container(
                behave_runner.allure_results,
                has_before("before step", with_status("passed"))
            ),
            has_container(
                behave_runner.allure_results,
                has_after("after all", with_status("passed"))
            ),
            has_container(
                behave_runner.allure_results,
                has_after("after feature", with_status("passed"))
            ),
            has_container(
                behave_runner.allure_results,
                has_after("after scenario", with_status("passed"))
            ),
            has_container(
                behave_runner.allure_results,
                has_after("after step", with_status("passed"))
            )
        )
    )


def test_tag_hooks(behave_runner: Runner):
    behave_runner.run_behave(
        feature_paths=[
            "./test-data/tag-hook.feature",
            "./test-data/feature-tag-hook.feature"
        ],
        step_paths=["./test-data/steps.py"],
        environment_path="./test-data/tag-hooks.py"
    )
    assert_that(
        behave_runner.allure_results,
        all_of(
            has_test_case(
                "Tag hooks as fixture - this scenario is affected",
                with_status("passed"),
                has_container(
                    behave_runner.allure_results,
                    has_before("before tag @hook_target", with_status("passed"))
                ),
                has_container(
                    behave_runner.allure_results,
                    has_after("after tag @hook_target", with_status("passed"))
                )
            ),
            has_test_case(
                "Tag hooks as fixture - this scenario is not affected",
                with_status("passed"),
                not_(
                    has_container(
                        behave_runner.allure_results,
                        has_before("before tag @hook_target")
                    )
                ),
                not_(
                    has_container(
                        behave_runner.allure_results,
                        has_after("after tag @hook_target")
                    )
                )
            ),
            has_test_case(
                "Feature-level tag hooks as fixtures",
                with_status("passed"),
                has_container(
                    behave_runner.allure_results,
                    has_before("before tag @hook_target", with_status("passed"))
                ),
                has_container(
                    behave_runner.allure_results,
                    has_after("after tag @hook_target", with_status("passed"))
                )
            )
        )
    )


def test_attachment_before_feature(behave_runner: Runner):
    behave_runner.run_behave(
        feature_paths=["./test-data/attachment-hook.feature"],
        step_paths=["./test-data/steps.py"],
        environment_path="./test-data/attachment-hooks.py"
    )
    assert_that(
        behave_runner.allure_results,
        all_of(
            has_test_case(
                "Attachment from before_feature fixture-hook",
                with_status("passed"),
                has_container(
                    behave_runner.allure_results,
                    has_before(
                        "before feature",
                        with_status("passed"),
                        has_attachment_with_content(
                            behave_runner.allure_results.attachments,
                            equal_to("Attachment from before_feature"),
                            allure.attachment_type.TEXT.mime_type,
                            "Dynamic attachment"
                        )
                    ),
                )
            ),
            has_test_case(
                "One more scenario with same attachment in fixture-hook",
                with_status("passed"),
                has_container(
                    behave_runner.allure_results,
                    has_before(
                        "before feature",
                        with_status("passed"),
                        has_attachment_with_content(
                            behave_runner.allure_results.attachments,
                            equal_to("Attachment from before_feature"),
                            allure.attachment_type.TEXT.mime_type,
                            "Dynamic attachment"
                        )
                    )
                )
            )
        )
    )


def test_context_step_in_scenario_hooks(behave_runner: Runner):
    behave_runner.run_behave(
        feature_paths=["./test-data/step-hook.feature"],
        step_paths=["./test-data/steps.py"],
        environment_path="./test-data/context-step-hooks.py"
    )
    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Hook with steps",
            with_status("passed"),
            has_container(
                behave_runner.allure_results,
                has_before(
                    "before scenario",
                    with_status("passed"),
                    has_step(
                        "Step in before_scenario",
                        with_status("passed")
                    )
                ),
            ),
            has_container(
                behave_runner.allure_results,
                has_after(
                    "after scenario",
                    with_status("passed"),
                    has_step(
                        "Step in after_scenario",
                        with_status("passed")
                    )
                )
            )
        )
    )


def test_func_step_in_scenario_hooks(behave_runner: Runner):
    behave_runner.run_behave(
        feature_paths=["./test-data/step-hook.feature"],
        step_paths=["./test-data/steps.py"],
        environment_path="./test-data/func-step-hooks.py"
    )
    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Hook with steps",
            with_status("passed"),
            has_container(
                behave_runner.allure_results,
                has_before(
                    "before all",
                    with_status("passed"),
                    has_step(
                        "Step in 'before_all'",
                        with_status("passed")
                    )
                ),
            ),
            has_container(
                behave_runner.allure_results,
                has_after(
                    "after all",
                    with_status("passed"),
                    has_step(
                        "Step in 'after_all'",
                        with_status("passed")
                    )
                )
            )
        )
    )
