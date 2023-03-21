Feature: Hook

  Scenario Outline: Hook 'scenario'
    Given feature definition
        """
        Feature: Hook
          Scenario: Scenario with "<when> <where>" hook
            Given simple passed step

          Scenario: Another scenario with "<when> <where>" hook
            Given simple passed step
        """
      And hooks implementation
        """
        import allure_commons


        @allure_commons.fixture
        def <when>_<where>(context, <where>):
            pass
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with "<when> <where>" hook"
      And this scenario has <when> fixture "<when>_<where>"

     Then allure report has a scenario with name "Another scenario with "<when> <where>" hook"
      And this scenario has <when> fixture "<when>_<where>"

    Examples: fixtures
            | when   | where    |
            | before | scenario |
            | after  | scenario |


  Scenario Outline: Hook 'tag'
    Given feature definition
        """
        Feature: Hook

          @tag_for_hook
          Scenario: Scenario with "<when> <where>" hook
            Given simple passed step

          Scenario: Another scenario without "<when> <where>" hook
            Given simple passed step
        """
      And hooks implementation
        """
        import allure_commons


        @allure_commons.fixture
        def <when>_<where>(context, <where>):
            pass
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with "<when> <where>" hook"
      And this scenario has <when> fixture "<when>_<where>"

     Then allure report has a scenario with name "Another scenario without "<when> <where>" hook"
      And this scenario has not <when> fixture "<when>_<where>"

    Examples: fixtures
            | when   | where |
            | before | tag   |
            | after  | tag   |


  Scenario Outline: Hook 'tag'
    Given feature definition
        """
        @tag_for_hook
        Feature: Hook

          Scenario: Scenario with "<when> <where>" hook
            Given simple passed step

          Scenario: Another scenario with "<when> <where>" hook
            Given simple passed step
        """
      And hooks implementation
        """
        import allure_commons


        @allure_commons.fixture
        def <when>_<where>(context, <where>):
            pass
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with "<when> <where>" hook"
      And this scenario has <when> fixture "<when>_<where>"

     Then allure report has a scenario with name "Another scenario with "<when> <where>" hook"
      And this scenario has <when> fixture "<when>_<where>"

    Examples: fixtures
            | when   | where |
            | before | tag   |
            | after  | tag   |


  Scenario Outline: Hook 'feature'
    Given feature definition
        """
        Feature: Hook
          Scenario: Scenario with "<when> <where>" hook
            Given simple passed step

          Scenario: Another scenario with "<when> <where>" hook
            Given simple passed step
        """
      And hooks implementation
        """
        import allure_commons


        @allure_commons.fixture
        def <when>_<where>(context, <where>):
            pass
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with "<when> <where>" hook"
      And this scenario has <when> fixture "<when>_<where>"

     Then allure report has a scenario with name "Another scenario with "<when> <where>" hook"
      And this scenario has <when> fixture "<when>_<where>"

    Examples: fixtures
            | when   | where   |
            | before | feature |
            | after  | feature |


  Scenario Outline: Hook 'all'
    Given feature definition
        """
        Feature: Hook
          Scenario: Scenario with "<when> <where>" hook
            Given simple passed step

          Scenario: Another scenario with "<when> <where>" hook
            Given simple passed step
        """
      And hooks implementation
        """
        import allure_commons


        @allure_commons.fixture
        def <when>_<where>(context):
            pass
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with "<when> <where>" hook"
      And this scenario has <when> fixture "<when>_<where>"

     Then allure report has a scenario with name "Another scenario with "<when> <where>" hook"
      And this scenario has <when> fixture "<when>_<where>"

    Examples: fixtures
            | when   | where |
            | before | all   |
            | after  | all   |


  Scenario: Hook attachment
    Given feature definition
        """
        Feature: Hook
          Scenario: Scenario with "before_feature" hook and attachment
            Given simple passed step
        """
      And hooks implementation
        """
        import allure
        import allure_commons


        @allure_commons.fixture
        def before_feature(context, feature):
            allure.attach('Hi there!', name='user attachment', attachment_type=allure.attachment_type.TEXT)
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with "before_feature" hook and attachment"
      And this scenario has before fixture "before_feature"
      And this before has attachment


  Scenario Outline: Hook step as context
    Given feature definition
        """
        Feature: Hook
          Scenario: Scenario with "<when> <where>" hook and step inside
            Given simple passed step
        """
      And hooks implementation
        """
        import allure
        import allure_commons


        @allure_commons.fixture
        def <when>_<where>(context, <where>):
            with allure.step('Step inside fixture'):
              pass
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with "<when> <where>" hook and step inside"
      And this scenario has <when> fixture "<when>_<where>"
      And this <when> contains step "Step inside fixture"

    Examples: fixtures
            | when   | where    |
            | before | scenario |
            | after  | scenario |


  Scenario Outline: Hook step as function
    Given feature definition
        """
        Feature: Hook
          Scenario:  Scenario with "<when> <where>" hook and step as function inside
            Given simple passed step
        """
      And hooks implementation
        """
        import allure
        import allure_commons

        @allure.step('Step function')
        def step():
            pass

        @allure_commons.fixture
        def <when>_<where>(context):
            step()
        """
     When I run behave with allure formatter
     Then allure report has a scenario with name "Scenario with "<when> <where>" hook and step as function inside"
      And this scenario has <when> fixture "<when>_<where>"
      And this <when> contains step "Step function"

    Examples: fixtures
            | when   | where |
            | before | all   |
            | after  | all   |

