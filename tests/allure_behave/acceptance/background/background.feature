Feature: Allure-behave compatibility with feature backgrounds
  Background: A background with {bg_step_status} step
    Given the first background step that is {bg_step_status}
      And the second background step with no failures

  Scenario: Scenario with background containing {bg_step_status} step
    Given the first step with no failures
      And the second step with no failures

  Scenario: Another scenario with background containing {bg_step_status} step
    Given the step with no failures
