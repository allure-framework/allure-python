Feature: Description

  Scenario: Use description
    Given feature definition
        """
        Feature: Description

          Scenario: Scenario with description
            Scenario description.
            Yep, multi-line description!

            Given simple passed step
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with description"
