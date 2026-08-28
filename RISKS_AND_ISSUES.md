# Risks & Issues — AgentEvalOps

| Risk / Issue ID | Description | Severity | Mitigation Strategy | Owner | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **RISK-01** | High memory usage during heavy trace processing | Medium | Process traces asynchronously using Redis worker queues; avoid loading multi-GB data into memory. | Principal Eng | Active / Mitigated |
| **RISK-02** | GitHub OAuth token scope missing `workflow` scope | Low | Handled during setup; optional manual grant via `gh auth refresh -s workflow`. | SRE | Mitigated |
