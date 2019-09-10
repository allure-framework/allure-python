Feature: Link

    Scenario: Scenario issue link
    Given feature definition
        """
        Feature: Step status

          @allure.issue:http://qameta.io
          Scenario: Scenario with passed step
              Given simple passed step
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with passed step"
      And scenario has "http://qameta.io" link with type "issue"

  Scenario: Feature user link
    Given feature definition
        """
        @allure.link.homepage:http://qameta.io
        Feature: Step status

          Scenario: Scenario with passed step
              Given simple passed step
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with passed step"
      And scenario has "http://qameta.io" link


  Scenario: Feature and scenario user link
    Given feature definition
        """
        @allure.link.homepage:http://qameta.io
        Feature: Step status

          @allure.issue:http://example.com
          Scenario: Scenario with passed step
              Given simple passed step
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with passed step"
      And scenario has "http://qameta.io" link
      And scenario has "http://example.com" link with type "issue"
