Feature: Behave cmd options

  Scenario: Tags in scenario with options "--tags=tag"
    Given feature definition
        """
        Feature: Tags filtering

        @tag
        Scenario: Scenario with tag
          Given simple passed step

        Scenario: Scenario without tag
          Given simple passed step
        """
     When I run behave with allure formatter with options "--tags=tag"
     Then allure report has a scenario with name "Scenario with tag"
      And this scenario has "passed" status

     Then allure report has a scenario with name "Scenario without tag"
      And this scenario has "skipped" status

  Scenario: Tags in scenario with options "--tags=tag --no-skipped"
    Given feature definition
        """
        Feature: Tags filtering

        @tag
        Scenario: Scenario with tag
          Given simple passed step

        Scenario: Scenario without tag
          Given simple passed step
        """
     When I run behave with allure formatter with options "--tags=tag --no-skipped"
     Then allure report has a scenario with name "Scenario with tag"
      And this scenario has "passed" status

     Then allure report has not a scenario with name "Scenario without tag"
