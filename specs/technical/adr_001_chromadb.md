# ADR 001: ChromaDB for Local RAG

## Context
We need a vector database for CDC indexing and semantic search.

## Decision
Use ChromaDB in Docker for local deployment.

## Consequences
- **Pros**: No cloud dependency, full data sovereignty
- **Cons**: No built-in high availability
