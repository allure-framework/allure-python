Feature: Scenario outline example converters
  Scenario: Scenario outline example converters
    Given example.feature with content:
      """
      Feature: Scenario outline example converters
        Scenario Outline: Outline example converters
          Given step with <array> param

        Examples:
        | array |
        | 0;1   |
        | 2;3   |
      """
    And example_test.py with content:
      """
      from pytest_bdd import scenario
      from pytest_bdd import given, then, when

      def param_to_array(data):
          if data:
              if ";" in data:
                  return [item for item in data.split(";")]
              # case for single item that should also be returned as an array item
              elif isinstance(data, str):
                  return [data]
          else:
              return []

      @given("step with <array> param")
      def then_step_with_array(array):
          pass

      @scenario("example.feature", "Outline example converters", example_converters={'array':param_to_array})
      def test_scenario_outline_example():
          pass
      """
    When run pytest-bdd with allure

    Then allure report has result for "Outline example converters" scenario
    Then this scenario has parameter "array" with value "['0','1']"
    Then this scenario contains "Given step with <['0', '1']> param" step

    Then allure report has result for "Outline example converters" scenario
    Then this scenario has parameter "array" with value "['2','3']"
    Then this scenario contains "Given step with <['2', '3']> param" step


