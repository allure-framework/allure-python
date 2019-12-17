Feature: Scenario
  Scenario: Default labels
    Given feature file aaa with content:
      """
      Feature: Scenario example
        Scenario Outline: Scenario example
          Given passed step
          When <status> step
          Then passed step

        Examples:
        | status |
        | passed |
        | failed  |
      """
    And dummy steps in conftest.py
    And test file with "Scenario example" scenario in example
    When run pytest-bdd with allure
    Then it has result for example scenario
