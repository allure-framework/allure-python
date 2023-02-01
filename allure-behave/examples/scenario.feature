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


  Scenario: Skip steps after fail step
    Given feature definition
        """
        Feature: Scenario

        Scenario: Scenario with failed step in chain
          Given passed step
          Given failed step
          Given broken step
        """
      When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with failed step in chain"
      And this scenario has "failed" status

      And this scenario contains step "Given passed step"
      And this step has "passed" status

      And this scenario contains step "Given failed step"
      And this step has "failed" status

      And this scenario contains step "Given broken step"
      And this step has "skipped" status


  Scenario: Scenario without name
    Given feature definition
        """
        Feature: Scenario

        Scenario:
          Given passed step
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario"
