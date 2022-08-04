Feature: Scenario outline
  Scenario: Scenario outline
    Given example.feature with content:
      """
      Feature: Scenario outline
        Scenario Outline: Outline example
          Given <first> step
          When do nothing
          Then step with <second> param

        Examples:
        | first | second |
        | Alpha |      1 |
        | Bravo |      2 |
      """
    And example_test.py with content:
      """
      from pytest_bdd import scenario
      from pytest_bdd import given, then, when
      from pytest_bdd.parsers import cfparse

      @given(cfparse("{first} step"))
      def given_step(first):
          pass

      @when("do nothing")
      def nope_step():
          pass

      @then(cfparse("step with {second} param"))
      def then_step(second):
          pass

      @scenario("example.feature", "Outline example")
      def test_scenario_outline_example():
          pass
      """
    When run pytest-bdd with allure

    Then allure report has result for "Outline example" scenario
    Then this scenario contains "Given Alpha step" step
    Then this scenario contains "Then step with 1 param" step

    Then allure report has result for "Outline example" scenario
    Then this scenario contains "Given Bravo step" step
    Then this scenario contains "Then step with 2 param" step


