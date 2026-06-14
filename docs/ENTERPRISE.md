# agentforge for enterprise

agentforge is built to drop into a real organization, not just a demo. The pieces an
enterprise needs:

## 1. Bring your own model backend
Set environment variables — no code changes, secrets from your store:
```sh
export AGENTFORGE_BACKEND=openai          # openai | fleet | mock
export AGENTFORGE_BASE_URL=https://your-gateway/v1
export AGENTFORGE_API_KEY=$(vault read -field=token secret/llm)
export AGENTFORGE_MODEL=your-default-model
```
```python
from agentforge import backend_from_env, Runtime, load_org
rt = Runtime(backend_from_env())
rt.run_team(load_org("orgs/research.json"), "research", "Q3 market sizing")
```
`OpenAIBackend` works with OpenAI, Azure OpenAI, vLLM, or any OpenAI-compatible
gateway; `FleetBackend` targets a local edgemesh/Cognis fleet. Both retry with a
timeout and surface `BackendError` instead of crashing a run.

## 2. Governance — policy as code
```python
from agentforge import Policy, PolicyEngine, load_org
policy = Policy(
    denied_tools=["shell"],                 # never allowed
    approval_required=["github", "sql"],    # human sign-off before use
    role_tools={"SRE": ["http", "shell"]},  # per-role allowlists
    max_agent_calls=200,                    # budget cap
    require_reports_to=True,                # enforce chain of command
)
report = PolicyEngine(policy).validate(load_org("orgs/eng.json"))
assert report["ok"], report["violations"]   # gate deploys in CI
```
Run it from the CLI in a pipeline: `agentforge validate --file orgs/eng.json
--require-reports-to --approval-required github,sql`.

## 3. Auditability
```python
from agentforge import AuditTrail, Runtime, backend_from_env
trail = AuditTrail("audit/run.jsonl")        # append-only JSONL
Runtime(backend_from_env(), audit=trail).run_team(org, "eng", task)
trail.summary()   # counts by event kind, agents touched
```
Every agent run, synthesis, and error is recorded with a timestamp — traceable for
debugging and compliance.

## 4. Org definitions in version control
Keep orgs as JSON/YAML in your repo; `load_org`/`save_org` round-trip them. Review org
changes like code; validate them in CI before they ship.

## 5. Reliability
Per-agent error isolation (a single failing agent doesn't fail the run), retries +
timeouts on the backend, and usage metering (`RunResult.usage`) for cost/limit tracking.

## 6. Runs on infrastructure you own
Pair with **edgemesh** (cluster your machines into one OpenAI endpoint) and **labforge**
(plan/scale the hardware) to run the whole agent org on-prem, air-gapped if needed.
