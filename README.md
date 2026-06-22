# agentforge

> Build entire **organizations of AI agents** — roles, personalities, experience,
> skills, and tools — then run them, or export them to the agent framework of your
> choice and sync them to your project-management suite. Fully interoperable with
> the **Cognis 300+ suite** (edgemesh / fleet / jtf-meridian) and the popular
> agent + PM platforms.

[![Code License: COCL 1.0](https://img.shields.io/badge/License-COCL%201.0-6b46c1.svg)](LICENSE)
[![tests](https://img.shields.io/badge/tests-29%20passing-2ea44f.svg)](tests/)
[![enterprise-ready](https://img.shields.io/badge/enterprise-ready-1f6feb.svg)](docs/ENTERPRISE.md)

<!-- cognis:layman:start -->
## What is this?

Most agent tools make you wire up one or two bots in code. agentforge lets you
design a whole *org* — like staffing a company — and treat it as data: a Research
Firm, a Software Team, or Cognis's own JTF MERIDIAN command structure, each with
named agents that have a job title, a personality (a careful analyst, a relentless
skeptic, a pragmatic builder…), an experience level, the skills they're good at, and
the tools they can use. Once you've described the org, agentforge can run it on a
task (locally, or on your own AI fleet), or hand it to whatever agent framework you
already use — CrewAI, AutoGen, LangGraph, OpenHands, TaskWeaver, MetaGPT — and put
its tasks on your board in GitHub, Jira, Linear, Notion, Trello, or Asana. One
definition of your agent workforce; many places to run it.
<!-- cognis:layman:end -->

## The model

`Organization → Teams → Agents`. Each **Agent** has a **Persona** (archetype +
traits like rigor/creativity/risk/skepticism + tone), an **experience** level
(intern…principal…exec), **skills** (from a registry), **tools** (mapped to real
integrations and Cognis capabilities), goals, a model hint, and a `reports_to`.
Everything round-trips to JSON/YAML.

## What it does

```sh
agentforge templates                       # ready-made orgs
agentforge org --template jtf_meridian     # the Cognis command structure as agents
agentforge agents --template research_firm # roles / personas / skills / tools
agentforge run --template software_team --team eng --task "design an API"   # +--fleet for live
agentforge export --template research_firm --framework crewai               # or autogen/langgraph/openhands/taskweaver/metagpt
agentforge export --template software_team --framework autogen --code       # runnable snippet
agentforge export --template jtf_meridian --framework mermaid --code        # org chart as a Mermaid diagram
agentforge pm --template software_team --platform github --task "ship A"    # or jira/linear/notion/trello/asana
agentforge schema --format json                                             # JSON Schema (Draft 2020-12) for org files
agentforge schema --file my_org.json                                        # validate an org against the schema
agentforge frameworks                       # everything it interoperates with
```

## Demos

[`demos/`](demos/) has 10 ready-to-run, real-use-case agent orgs — each a real
`org.json` plus a `SCENARIO.md` (where it came from, what to expect, exact commands,
how to act). They run offline on the deterministic mock backend, no API key needed:
incident response, SOC 2 readiness, an AI research lab, a mobile-app launch squad, an
M&A due-diligence deal team, an MLOps platform team, a grant-proposal team, a support
escalation pod, an energy-sector research desk, and exporting the JTF MERIDIAN
command structure. See [`demos/README.md`](demos/README.md).

```sh
agentforge schema --file demos/01-incident-response/org.json   # ok:true
agentforge run --file demos/09-energy-trading-desk/org.json --team desk --task "bull vs bear: grid-scale power"
```

## Interoperability

**Agent frameworks (export):** CrewAI · AutoGen/AG2 · LangGraph · OpenHands ·
TaskWeaver · MetaGPT (+ DeepTeam red-team persona mapping). One org definition →
each framework's native config (and runnable code for the code-first ones).

**Project-management suites (sync):** GitHub Projects/Issues · Jira · Linear ·
Notion · Trello · Asana — agents become assignees, tasks become issues/cards.

**Cognis suite:** `edgemesh` is the model/compute backend (the `FleetBackend`
targets its OpenAI-compatible `/v1`); the local **fleet/cog4** runs each agent
(per-agent slot via `Agent.model`); **jtf-meridian** ships as a built-in org
template; the tool registry maps to **kycaml / cryptotrace / ragkit / labforge**;
**labforge** plans the hardware the org runs on. Run `agentforge frameworks`.

## Runtime

`Runtime(backend).run_team(org, team, task)` assigns a task across a team, collects
each agent's contribution, and has the lead synthesize a result, with per-agent error
isolation and usage metering. `LocalMockBackend` is deterministic/offline;
`OpenAIBackend` targets any OpenAI-compatible endpoint (retries + timeout);
`FleetBackend` targets edgemesh/the fleet with a graceful fallback.

## Enterprise

Built to drop into a real org (see [`docs/ENTERPRISE.md`](docs/ENTERPRISE.md)):

- **Bring your own backend** via env vars (`AGENTFORGE_BACKEND/_BASE_URL/_API_KEY/_MODEL`) — OpenAI, Azure OpenAI, vLLM, a gateway, or the local fleet; secrets from your store, never code.
- **Governance — policy as code:** global + per-role tool allow/deny lists, approval-required tools, budget caps, chain-of-command. `PolicyEngine.validate(org)` gates deploys; `agentforge validate` runs it in CI.
- **Audit trail:** append-only JSONL of every agent run/synthesis/error with timestamps.
- **Org-as-config** in version control (`load_org`/`save_org`), reviewed and validated like code — with a published **JSON Schema** (`agentforge schema`, Draft 2020-12) for editor autocomplete and CI linting of org files.
- **Reliability:** retries/timeouts, per-agent error isolation, usage metering for cost/limit tracking.
- Runs on infrastructure you own — pair with **edgemesh** + **labforge** for on-prem/air-gapped.

```sh
agentforge validate --file orgs/eng.json --require-reports-to --approval-required github,sql
```

<!-- cognis:install:start -->
## Install

```sh
curl -fsSL https://raw.githubusercontent.com/cognis-digital/agentforge/HEAD/install.sh | sh   # Linux/macOS
```
```powershell
irm https://raw.githubusercontent.com/cognis-digital/agentforge/HEAD/install.ps1 | iex        # Windows
```
```sh
pipx install "git+https://github.com/cognis-digital/agentforge.git"   # or uv tool install / pip install
git clone https://github.com/cognis-digital/agentforge.git && cd agentforge && pip install .  # source
```
Then: `agentforge --help`
<!-- cognis:install:end -->

## Topics / Domains

`ai-agents` · `multi-agent` · `agent-orchestration` · `llm` · `crewai` · `autogen` ·
`langgraph` · `agentops` · part of the **Cognis Neural Suite** (AI & ML domain).

## Verification

```text
tests   : 29 passing (deterministic; offline mock backend)
runtime : pure Python standard library; no third-party deps
demos   : 10 real-use-case orgs, each validated against the schema
```

## Disclaimer

agentforge is a definition + orchestration + export layer; it does not vendor or
reimplement the target frameworks — install those you actually run. Exporters
produce each framework's config/structure; PM adapters produce payloads (wire a
client + token to push). Not affiliated with any framework or platform named.

## License

Cognis Open Collaboration License (COCL) 1.0 — see [LICENSE](LICENSE).
