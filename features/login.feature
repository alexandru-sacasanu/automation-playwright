Feature: Login
  As a user of the store
  I want to log in
  So that I can access the product inventory

  @smoke
  Scenario: Valid credentials log the user in
    Given I am on the login page
    When I log in with username "standard_user" and password "secret_sauce"
    Then I should see the product inventory

  @regression
  Scenario: Locked out user sees an error
    Given I am on the login page
    When I log in with username "locked_out_user" and password "secret_sauce"
    Then I should see a login error containing "locked out"

  @regression
  Scenario: Invalid password shows an error
    Given I am on the login page
    When I log in with username "standard_user" and password "wrong_password"
    Then I should see a login error
