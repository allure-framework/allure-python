Feature: Language
    Scenario: Use russian
    Given feature definition ru
        """
        Функционал: Язык

          Сценарий: На русском
            Допустим passed step
        """
     When I run behave with allure formatter with options "--lang ru"
     Then allure report has a scenario with name "На русском"