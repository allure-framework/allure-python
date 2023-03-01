Feature: Scenario Outline
  @single-table
  @1
  Scenario Outline: Scenario outline with one table
    Given a user <name> <surname>

    Examples: Customers
      | name  | surname |
      | Alice | Johnson |
      | Bob   | Smith   |

  @single-table
  @2
  Scenario Outline: Another scenario outline with one table
    Given a user <name> <surname>

    Examples: Employees
      | name  | surname |
      | Jane  | Watson  |
      | Mark  | Nickson |

  @multiple-tables
  Scenario Outline: Scenario outline with multiple tables
    Given a user <name> <surname>

    Examples: Customers
      | name  | surname |
      | Alice | Johnson |
      | Bob   | Smith   |

    Examples: Employees
      | name  | surname |
      | Jane  | Watson  |
      | Mark  | Nickson |
