# Changelog

## 0.2.1 — Schema, Mermaid, and demos
- **Org JSON Schema** (`agentforge.schema`) — emit a standards-compliant JSON Schema
  (Draft 2020-12) for an org definition (`agentforge schema --format json`), generated
  from the live persona/skill/tool registries so it never drifts. Use it for
  `$schema` editor autocomplete and CI linting of org files.
- **Dependency-free org validator** — `agentforge schema --file org.json` checks
  structure, the enum vocabularies, unique keys, and the `lead`/`reports_to`
  cross-references, with JSON-path error locations. No third-party validator required;
  cross-checked against `jsonschema` when installed.
- **Mermaid exporter** — `agentforge export --framework mermaid` renders the org chart
  (teams + chain-of-command) as a Mermaid flowchart that GitHub/GitLab/Notion render
  natively.
- **`demos/`** — 10 real-use-case agent orgs (incident response, SOC 2 readiness, AI
  research lab, mobile launch, M&A due diligence, MLOps, grant writing, support
  escalation, energy research desk, JTF MERIDIAN), each with a runnable `org.json` and
  a `SCENARIO.md`. A test validates every demo against the schema.
- 29 tests.

## 0.2.0 — Enterprise hardening
- **Generic OpenAI backend** (`OpenAIBackend`) — point agentforge at *any* OpenAI-
  compatible endpoint (OpenAI, Azure OpenAI, vLLM, a corporate gateway), not just the
  Cognis fleet. Retries + timeout; raises `BackendError` on final failure.
- **`FleetBackend`** now subclasses it (edgemesh/local fleet) with a graceful mock
  fallback for local dev.
- **Governance policy engine** (`policy.Policy` / `PolicyEngine`) — global + per-role
  tool allow/deny lists, approval-required tools, budget caps, and chain-of-command
  (`require_reports_to`). `validate(org)` is a pre-deploy gate; `agentforge validate`.
- **Audit trail** (`audit.AuditTrail`) — structured, append-only JSONL of every agent
  run/synthesis/error with timestamps; `summary()`.
- **Config & persistence** (`config`) — `load_org`/`save_org` (JSON, optional YAML);
  `backend_from_env()` driven by `AGENTFORGE_BACKEND/_BASE_URL/_API_KEY/_MODEL`
  (secrets from the environment, never code).
- **Runtime hardening** — per-agent error isolation (one failing agent no longer kills
  the run), usage metering (`RunResult.usage`), optional policy validation + audit hooks.
- `py.typed` marker; 20 tests; version bump.

## 0.1.0 — Initial release
- Organization → Teams → Agents domain model with Persona / experience / skills / tools.
- Persona archetypes + system-prompt composer; skill/tool registry.
- Templates: software_team, research_firm, jtf_meridian.
- Runtime with LocalMockBackend + FleetBackend.
- Interop: export to CrewAI/AutoGen/LangGraph/OpenHands/TaskWeaver/MetaGPT; PM sync to
  GitHub/Jira/Linear/Notion/Trello/Asana.
