Feature: Cart
  As a logged-in shopper
  I want to add and remove items from my cart
  So that I can control what I'm about to buy

  Background:
    Given I am logged in as the standard user

  @smoke
  Scenario: Adding an item updates the cart badge
    When I add "Sauce Labs Backpack" to the cart
    Then the cart badge should show "1"

  @regression
  Scenario: Adding multiple items updates the cart badge
    When I add "Sauce Labs Backpack" to the cart
    And I add "Sauce Labs Bike Light" to the cart
    Then the cart badge should show "2"

  @regression
  Scenario: Removing an item updates the cart badge
    When I add "Sauce Labs Backpack" to the cart
    And I add "Sauce Labs Bike Light" to the cart
    And I remove "Sauce Labs Backpack" from the cart
    Then the cart badge should show "1"
