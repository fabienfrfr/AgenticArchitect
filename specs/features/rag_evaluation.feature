@REQ_RAG_SECURITY
Feature: Security Access RAG Evaluation
  As a Security Agent
  I want to verify that retrieved ArangoDB data is accurate
  So that I ensure no unauthorized information is leaked

  Scenario: Verify ArangoDB context accuracy
    Given an input query "What are the security constraints for ArangoDB?"
    When the agent retrieves data from ArangoDB
    Then the final response should be factually accurate