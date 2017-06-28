Feature: Scenario

  Scenario Outline: Scenario status
    Given feature definition
        """
        Feature: Scenario

        Scenario: Scenario with <step type> step
          Given <step type> step
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with <step type> step"
      And this scenario has "<status>" status
      And this scenario contains step "Given <step type> step"
      And this step has "<status>" status

    Examples: statuses
            | step type | status |
            | passed    | passed |
            | failed    | failed |
            | broken    | broken |
            | undefined | broken |

