# Relational Data Model & Multi-Tenancy Strategy

## 1. Multi-Tenant Entity Hierarchy

```text
Organization
 ├── User (role-based permissions)
 └── Project
      ├── APIKey (project-scoped access token)
      ├── Agent
      │    └── AgentVersion (system prompt, model, config)
      │         └── Run (execution session, tokens, cost)
      │              ├── Trace (execution graph)
      │              │    └── Span (LLM / Tool / Retrieval / Embedding)
      │              └── Evaluation (scores, reasons, severity)
      ├── Dataset
      │    └── DatasetCase (input, expected_output)
      ├── Evaluator (evaluator configuration & criteria)
      ├── Experiment (eval run comparison)
      └── Deployment (environment active version)
```

## 2. Multi-Tenancy Strategy

- **Tenant Boundary**: Every database model extends `Base` (UUID primary key + timestamps) and includes foreign keys to `organization_id` and `project_id`.
- **Query Scoping**: Application repositories strictly scope all query filters to the authenticated request's `organization_id` and `project_id`.
- **Future Database Isolation**: Designed to support schema-per-tenant or database-per-tenant isolation if required for enterprise compliance.
