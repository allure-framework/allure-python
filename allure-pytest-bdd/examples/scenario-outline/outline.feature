Feature: Allure report for scenario outline
  Scenario Outline: Two examples with two parameters each
    Given first step for <first> value
    When something is done with the value <second>
    Then check postconditions using <first> and <second>

    Examples:
      | first | second |
      | Alpha |      1 |
      | Bravo |      2 |
