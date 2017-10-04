Feature: Step

  Scenario: Failed step
    Given feature definition
        """
        Feature: Step status

          Scenario: Scenario with failed step
              Given simple failed step
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with failed step"
      And scenario contains step "Given simple failed step"
      And this step has "failed" status
      And this step has status details with message "AssertionError: Assert message"


  Scenario: Broken step
    Given feature definition
        """
        Feature: Step status

          Scenario: Scenario with broken step
              Given simple broken step
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with broken step"
      And scenario contains step "Given simple broken step"
      And this step has "broken" status
      And this step has status details with message "ZeroDivisionError"


  Scenario: Step text parameter
    Given feature definition
        """
        Feature: Step Data

          Scenario: Scenario with step contains text data
            Given simple passed step with text data
                '''
                Some text in step
                '''
              And simple passed step
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with step contains text data"
      And scenario contains step "Given simple passed step with text data"
      And this step has attachment
      And this step has "passed" status


  Scenario: Step table parameter
    Given feature definition
        """
        Feature: Step Data

          Scenario: Scenario with step contains table data
            Given simple passed step with table data
                | name | value |
                | e    | 2     |
                | e    | 4     |

              And simple passed step
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with step contains table data"
      And scenario contains step "Given simple passed step with table data"
      And this step has attachment
      And this step has "passed" status


  Scenario: Step attachment
    Given feature definition
        """
        Feature: Step Data

          Scenario: Scenario with step that attached data
            Given passed step with attachment
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with step that attached data"
      And scenario contains step "Given passed step with attachment"
      And this step has attachment
      And this step has "passed" status
