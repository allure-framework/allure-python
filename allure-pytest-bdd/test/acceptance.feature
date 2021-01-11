# Created by denis at 11.01.2021
Feature: test
  # Enter feature description here

  Scenario: scenario
    Given py file with imports: pytest, pytest_bdd, allure

    And func:
      """
      @given("given_step")
      def my_func():
          allure.attach("blah", ...)
          raise Exception("message")
      """
