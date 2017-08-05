Feature: Language
    Scenario: Use russian
    Given feature definition ru
        """
        Функционал: Юникод

          Структура сценария: Солнечный круг, небо вокруг
            Пусть всегда будет <это>
            Пусть всегда буду я
            Примеры:
             | это    |
             | солнце |
             | небо   |
             | мама   |
        """
     Then skip for python 2
     When I run behave with allure formatter with options "--lang ru"
     Then allure report has a scenario with name "Солнечный круг, небо вокруг"
      And scenario contains step "Пусть всегда будет солнце"
      And scenario contains step "Пусть всегда будет небо"
      And scenario contains step "Пусть всегда будет мама"
      And scenario contains step "Пусть всегда буду я"