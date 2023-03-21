Feature: Background

  Scenario Outline: Background status
    Given feature definition
        """
        Feature: Background

          Background: Scenario background with <step type> step
            Given <step type> step in background
              And another passed step in background

          Scenario: Scenario with background contains <step type> step
            Given passed step
              And one more passed step

          Scenario: Another scenario with background contains <step type> step
            Given passed step
        """

     When I run behave with allure formatter

     Then allure report has a scenario with name "Scenario with background contains <step type> step"
      And this scenario has "<status>" status
      And this scenario contains step "Given <step type> step in background"
      And this step has "<status>" status
      And this scenario contains step "And another passed step in background"
      And this step has "<other status>" status
      And this scenario contains step "Given passed step"
      And this step has "<other status>" status
      And this scenario contains step "And one more passed step"
      And this step has "<other status>" status

     Then allure report has a scenario with name "Another scenario with background contains <step type> step"
      And this scenario has "<status>" status
      And this scenario contains step "Given passed step"
      And this step has "<other status>" status

    Examples: statuses
            | step type | status | other status |
            | passed    | passed | passed       |
            | failed    | failed | skipped      |
            | broken    | broken | skipped      |
            | undefined | broken | skipped      |
