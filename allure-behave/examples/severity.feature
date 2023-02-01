Feature: Severity

  Scenario: Default severity is normal
    Given feature definition
        """
        Feature: Severity

        Scenario: Scenario and feature without severity
          Given simple passed step
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario and feature without severity"
      And scenario has "normal" severity


  Scenario: Severity tag in feature
    Given feature definition
        """
        @critical
        Feature: Severity

        Scenario: Scenario in feature with critical severity
          Given simple passed step
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario in feature with critical severity"
      And scenario has "critical" severity


  Scenario: Severity tag in scenario
    Given feature definition
        """
        Feature: Severity

        @critical
        Scenario: Scenario with critical severity in feature without severity
          Given simple passed step
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with critical severity in feature without severity"
      And scenario has "critical" severity


  Scenario: Severity tag in scenario and feature
    Given feature definition
        """
        @critical
        Feature: Severity

        @minor
        Scenario: Scenario with minor severity in feature with critical severity
          Given simple passed step
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with minor severity in feature with critical severity"
      And scenario has "minor" severity


  Scenario: Repeated severity tag
    Given feature definition
        """
        Feature: Severity

        @minor @critical @blocker
        Scenario: Scenario with repeated severity tag
          Given simple passed step
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with repeated severity tag"
      And scenario has "blocker" severity