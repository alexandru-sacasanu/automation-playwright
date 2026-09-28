Feature: Checkout
  As a logged-in shopper
  I want to check out the items in my cart
  So that I can complete my purchase

  Background:
    Given I am logged in as the standard user
    And I have added "Sauce Labs Backpack" and "Sauce Labs Bike Light" to the cart
    And I go to the cart page

  @smoke
  Scenario: Completing checkout with valid info
    When I proceed to checkout
    And I fill in checkout info with first name "Alex", last name "Demo", postal code "94107"
    And I finish the checkout
    Then I should see an order confirmation containing "Thank you"

  @regression
  Scenario: Checkout requires a first name
    When I proceed to checkout
    And I fill in checkout info with first name "", last name "Demo", postal code "94107"
    Then I should see a checkout error

  @regression
  Scenario: Checkout requires a postal code
    When I proceed to checkout
    And I fill in checkout info with first name "Alex", last name "Demo", postal code ""
    Then I should see a checkout error
