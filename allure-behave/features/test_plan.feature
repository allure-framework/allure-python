Feature: Test plan
  Scenario: Select scenarios by fullname
    Given feature definition
      """
      Feature: Test plan example

      Scenario: Scenario with passed step
        Given passed step

      Scenario: Ignored scenario
        Given passed step
      """
    Given feature definition
      """
      Feature: Another Test plan example

      Scenario: Another scenario with passed step
        Given passed step

      Scenario: Another ignored scenario
        Given passed step
      """
    Given test plan
      """
      {
        "version":"1.0",
        "tests": [
          {
            "selector": "<string>:Scenario with passed step"
          },
          {
            "selector": "<string>:Another scenario with passed step"
          }
        ]
      }
      """
    When I run behave with allure formatter
    Then allure report has a scenario with name "Scenario with passed step"
    Then allure report has not a scenario with name "Ignored scenario"
    Then allure report has a scenario with name "Another scenario with passed step"
    Then allure report has not a scenario with name "Another ignored scenario"

  Scenario: Select scenarios by allureid
    Given feature definition
      """
      Feature: Test plan example

      @allure.as_id:1
      Scenario: Scenario with passed step
        Given passed step

      @allure.as_id:2
      Scenario: Ignored scenario
        Given passed step
      """
    Given feature definition
      """
      Feature: Another Test plan example

      @allure.as_id:3
      Scenario: Another scenario with passed step
        Given passed step

      @allure.as_id:4
      Scenario: Another ignored scenario
        Given passed step
      """
    Given test plan
      """
      {
        "version":"1.0",
        "tests": [
          {
            "id": "1"
          },
          {
            "id": "3"
          }
        ]
      }
      """
    When I run behave with allure formatter
    Then allure report has a scenario with name "Scenario with passed step"
    Then allure report has not a scenario with name "Ignored scenario"
    Then allure report has a scenario with name "Another scenario with passed step"
    Then allure report has not a scenario with name "Another ignored scenario"