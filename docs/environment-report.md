# Environment Inspection Report — AgentEvalOps

**Generated Date:** August 28, 2026  
**Phase:** Phase 0 — Production Foundation & Developer Environment

---

## 1. Detected System & Hardware Specifications

| Component | Specification |
| :--- | :--- |
| **Operating System** | Microsoft Windows 10 Pro 64-bit (10.0.19045) |
| **CPU Architecture** | x86_64 (64-bit) |
| **System Memory (RAM)** | 8.00 GB Total Physical RAM (~7.68 GiB usable) |
| **Storage (Drive E:)** | 48.65 GB Free / 140.82 GB Total (NTFS) — Workspace Root (`E:\AgentEvalvo`) |
| **Storage (Drive C:)** | 25.55 GB Free / 97.09 GB Total (NTFS) — System Drive |

---

## 2. Detected Tooling & Versions

| Tool | Status | Detected Version | Location / Provider |
| :--- | :--- | :--- | :--- |
| **Python** | Installed | `3.14.6` | Global Python Runtime |
| **uv** | Installed | `0.12.0` | High-performance Python package & environment manager |
| **Node.js** | Installed | `v24.18.0` | Modern LTS JavaScript Runtime |
| **npm** | Installed | `11.16.0` | Node Package Manager |
| **Git** | Installed | `2.55.0.windows.3` | Version Control System |
| **Docker Engine** | Installed | `29.6.2` | Container Runtime |
| **Docker Compose** | Installed | `v5.3.1` | Container Orchestration |
| **Poetry** | Not Installed | N/A | Superseded by `uv` per Section 4 requirement |
| **pnpm** | Available via npx / npm | N/A | Managed via npm/npx workspace scripts |
| **Yarn** | Not Installed | N/A | Not required |
| **psql (Native)** | Not Installed | N/A | Managed cleanly via Docker Compose (`postgres:16-alpine`) |
| **redis-server (Native)** | Not Installed | N/A | Managed cleanly via Docker Compose (`redis:7-alpine`) |

---

## 3. Tooling Decisions & Actions

### Installed / Managed in Environment:
- **`uv`**: Utilized as the primary Python environment and package management engine across all backend, SDK, evaluator, and tooling subpackages via `pyproject.toml` workspace definitions.
- **Node.js / npm**: Utilized for Next.js App Router frontend tooling and TypeScript project configuration.
- **Docker & Docker Compose**: Configured to run PostgreSQL 16, Redis 7, and Qdrant (optional vector search container) in slim containerized environments.

### Intentionally NOT Installed & Rationale (Hardware Constraints):
1. **Large Local LLM Checkpoints (Llama, Mistral, Qwen, DeepSeek)**: Excluded due to 8 GB RAM and 48 GB disk constraints. External API models (OpenAI, Anthropic, Gemini) or Google Colab/Cloud GPUs will be used.
2. **PyTorch CUDA / Heavy GPU Toolkits**: Excluded from default runtime dependencies. Heavy ML dependencies will be defined under optional ML packages for cloud execution.
3. **Multi-GB Embedding Checkpoints**: Light sentence-transformers or remote API embeddings will be used for vector evaluation.
4. **Native Windows PostgreSQL / Redis Services**: Avoided polluting Windows OS background services; Docker containers provide isolated, reproducible, health-checked database environments.

---

## 4. Environment Verification Summary

- [x] OS & Hardware Specs Verified
- [x] Python 3.12+ / 3.14 + `uv` environment confirmed
- [x] Node.js v24 + npm runtime confirmed
- [x] Docker & Docker Compose functionality verified
- [x] Workspace initialized at `E:\AgentEvalvo`
