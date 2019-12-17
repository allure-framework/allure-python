Feature: Scenario
  Scenario: Default labels
    Given feature file aaa with content:
      """
      Feature: Scenario example
        Scenario: Scenario example
          Given passed step
          When failed step
          Then passed step
      """
    And dummy steps in conftest.py
    And test file with "Scenario example" scenario in example
    When run pytest-bdd with allure
    Then it has result for example scenario
