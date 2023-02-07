Feature: Behave hooks support

  @hook_target
  Scenario: Tag hooks as fixture - this scenario is affected
    Given noop

  Scenario: Tag hooks as fixture - this scenario is not affected
    Given noop
