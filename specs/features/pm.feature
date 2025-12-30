Feature: Project Manager Validation
  Scenario: Incomplete requirements trigger gaps identification
    Given a client provides "Build a RAG system"
    When the PM Agent analyzes the request
    Then the Charter should be marked as incomplete
    And "Budget constraints missing" should be in the gaps