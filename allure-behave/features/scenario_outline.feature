Feature: Scenario Outline

  Scenario: Scenario outline with one examples table
    Given feature definition
        """
        Feature: Scenario Outline

          Scenario Outline: Scenario outline with one examples table
            Given simple passed step with param "<user>"

            Examples: examples table
            | user  |
            | Alice |
            | Bob   |
        """
     When I run behave with allure formatter

     Then allure report has a scenario with name "Scenario outline with one examples table -- @1.1 examples table"
      And scenario contains step "Given simple passed step with param "Alice""
      And this scenario has parameter "user" with value "Alice"

     Then allure report has a scenario with name "Scenario outline with one examples table -- @1.2 examples table"
      And scenario contains step "Given simple passed step with param "Bob""
      And this scenario has parameter "user" with value "Bob"

  Scenario: Scenario outline with many examples table
    Given feature definition
        """
        Feature: Scenario Outline

          Scenario Outline: Scenario outline with many examples table
            Given simple passed step with params "<parameter one> <parameter two>"

            Examples: first table
            | parameter one | parameter two |
            | Peter         | I             |
            | Catherine     | II            |

            Examples: second table
            | parameter one | parameter two |
            | Richard       | the Lionheart |
            | Alexander     | the Great     |
        """
     When I run behave with allure formatter

     Then allure report has a scenario with name "Scenario outline with many examples table -- @1.1 first table"
      And scenario contains step "Given simple passed step with params "Peter I""
      And this scenario has parameter "parameter one" with value "Peter"
      And this scenario has parameter "parameter two" with value "I"

     Then allure report has a scenario with name "Scenario outline with many examples table -- @1.2 first table"
      And scenario contains step "Given simple passed step with params "Catherine II""
      And this scenario has parameter "parameter one" with value "Catherine"
      And this scenario has parameter "parameter two" with value "II"

     Then allure report has a scenario with name "Scenario outline with many examples table -- @2.1 second table"
      And scenario contains step "Given simple passed step with params "Richard the Lionheart""
      And this scenario has parameter "parameter one" with value "Richard"
      And this scenario has parameter "parameter two" with value "the Lionheart"

     Then allure report has a scenario with name "Scenario outline with many examples table -- @2.2 second table"
      And scenario contains step "Given simple passed step with params "Alexander the Great""
      And this scenario has parameter "parameter one" with value "Alexander"
      And this scenario has parameter "parameter two" with value "the Great"


  Scenario: Many scenario outlines with one examples table
    Given feature definition
        """
        Feature: Scenario Outline

          Scenario Outline: First scenario outline in feature
            Given simple passed step with param "<friend>"

            Examples: examples table
            | friend |
            | Rick   |
            | Morty  |


          Scenario Outline: Second scenario outline in feature
            Given simple passed step with param "<hero>"

            Examples: examples table
            | hero |
            | Finn |
            | Jack |
        """
     When I run behave with allure formatter

     Then allure report has a scenario with name "First scenario outline in feature -- @1.1 examples table"
      And scenario contains step "Given simple passed step with param "Rick""
      And this scenario has parameter "friend" with value "Rick"

     Then allure report has a scenario with name "First scenario outline in feature -- @1.2 examples table"
      And scenario contains step "Given simple passed step with param "Morty""
      And this scenario has parameter "friend" with value "Morty"

     Then allure report has a scenario with name "Second scenario outline in feature -- @1.1 examples table"
      And scenario contains step "Given simple passed step with param "Finn""
      And this scenario has parameter "hero" with value "Finn"

     Then allure report has a scenario with name "Second scenario outline in feature -- @1.2 examples table"
      And scenario contains step "Given simple passed step with param "Jack""
      And this scenario has parameter "hero" with value "Jack"

  Scenario Outline: Scenario outline with one examples table
    Given feature definition
        """
        Feature: Scenario Outline

          Scenario Outline: Scenario outline with example variable <user> in name
            Given simple passed step with param "<user>"

            Examples: examples table
            | user  |
            | Alice |
            | Bob   |
        """
    When I run behave with allure formatter
    Then allure report has a scenario with name "Scenario outline with example variable <user> in name <postfix>"

    Examples: examples table
            | user  | postfix                 |
            | Alice |  -- @1.1 examples table |
            | Bob   |  -- @1.2 examples table |