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

  Scenario: Dynamic description
    Given feature definition
        """
        Feature: Step status

          Scenario: Scenario with passed step
              Given simple passed step
        """
      And hooks implementation
        """
        import allure
        import allure_commons

        @allure_commons.fixture
        def before_scenario(context, scenario):
            allure.dynamic.description("Test description")
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with passed step"
      And scenario has description "Test description"