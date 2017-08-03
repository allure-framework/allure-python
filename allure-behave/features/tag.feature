Feature: Tags

  Scenario: Tags in feature
    Given feature definition
        """
        @uno @due @tre
        Feature: Tags

        Scenario: Scenario in feature with tags
          Given simple passed step
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario in feature with tags"
      And scenario has "uno" tag
      And scenario has "due" tag
      And scenario has "tre" tag


  Scenario: Tags in scenario
    Given feature definition
        """
        Feature: Tags

        @uno @due @tre
        Scenario: Scenario with tags
          Given simple passed step
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with tags"
      And scenario has "uno" tag
      And scenario has "due" tag
      And scenario has "tre" tag


  Scenario: Tags in feature and scenario
    Given feature definition
        """
        @uno @due @tre
        Feature: Tags

        @tre @quattro
        Scenario: Scenario and feature with tags
          Given simple passed step
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario and feature with tags"
      And scenario has "uno" tag
      And scenario has "due" tag
      And scenario has "tre" tag
      And scenario has "quattro" tag
