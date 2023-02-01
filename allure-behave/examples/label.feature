Feature: Label

    Scenario: Scenario label
    Given feature definition
        """
        Feature: Step status

          @allure.label.owner:me
          Scenario: Scenario with passed step
              Given simple passed step
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with passed step"
      And scenario has "owner" label with value "me"