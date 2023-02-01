Feature: Language
    Scenario: Use russian
      Given feature definition ru
        """
        Свойство: Юникод

          Структура сценария: Солнечный круг, небо вокруг
            Пусть всегда будет <это>
            Пусть всегда буду я
            Примеры:
             | это    |
             | солнце |
             | небо   |
             | мама   |
        """
     When I run behave with allure formatter with options "--lang ru"
     Then allure report has a scenario with name "Солнечный круг, небо вокруг"
      And scenario contains step "Пусть всегда будет солнце"
      And scenario contains step "Пусть всегда будет небо"
      And scenario contains step "Пусть всегда будет мама"
      And scenario contains step "Пусть всегда буду я"


    Scenario: Assert message in step
      Given feature definition ru
        """
        Свойство: Юникод

          Сценарий: Ошибка с utf-8 сообщением
            Допустим провальный шаг
        """
      When I run behave with allure formatter with options "--lang ru"
      Then allure report has a scenario with name "Ошибка с utf-8 сообщением"
       And scenario contains step "Допустим провальный шаг"
       And step has status details with message "AssertionError: Фиаско!"


    Scenario: ASCII assert message in step
      Given feature definition ru
        """
        Свойство: Юникод

          Сценарий: Ошибка с utf-8 сообщением
            Допустим провальный шаг с ascii
        """
      When I run behave with allure formatter with options "--lang ru"
      Then allure report has a scenario with name "Ошибка с utf-8 сообщением"
       And scenario contains step "Допустим провальный шаг с ascii"
       And step has status details with message "AssertionError: Фиаско!"
