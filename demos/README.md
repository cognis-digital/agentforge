# agentforge demos

Real-use-case agent orgs you can run today. Each folder has an `org.json` (a real
agentforge org definition) and a `SCENARIO.md` (where it came from, what to expect,
the exact commands, and how to act on the output). Everything runs offline on the
deterministic mock backend — no API key needed — and validates against the published
org schema.

| # | Demo | Teams / Agents | Shows off |
|---|------|----------------|-----------|
| 01 | [Sev-1 Incident Response Cell](01-incident-response/) | 1 / 5 | `run`, `pm github`, `export langgraph` |
| 02 | [SOC 2 Type II Readiness](02-soc2-audit-readiness/) | 1 / 5 | `validate` **failing** chain-of-command gate, `pm jira` |
| 03 | [Applied AI Research Lab](03-ai-research-lab/) | 2 / 6 | multi-team `run`, `export crewai --code`, `mermaid` |
| 04 | [Mobile App Launch Squad](04-mobile-app-launch/) | 1 / 7 | `pm trello`/`github`, go/no-go `run`, `autogen` |
| 05 | [M&A Due-Diligence Deal Team](05-due-diligence-deal-team/) | 1 / 5 | `validate` **passing** (exec lead), `langgraph` |
| 06 | [MLOps Platform Team](06-mlops-platform-team/) | 1 / 5 | tool-approval policy, `export openhands`, `mermaid` |
| 07 | [Federal Grant Proposal Team](07-grant-proposal-writers/) | 1 / 5 | persona→system-prompt, `pm notion` |
| 08 | [Customer Support Escalation Pod](08-customer-support-escalation/) | 1 / 4 | `run` synthesis + usage metering, `pm asana` |
| 09 | [Energy-Sector Trading Research Desk](09-energy-trading-desk/) | 1 / 5 | adversarial risk check, `crewai`, `pm linear` |
| 10 | [Export JTF MERIDIAN](10-jtf-meridian-export/) | 7 / 7 | `schema` (JSON Schema export + validation), all exporters |

## Quick start

```sh
# Validate any demo org against the schema (expect ok:true)
agentforge schema --file demos/01-incident-response/org.json

# Run a team on a task (offline, deterministic)
agentforge run --file demos/01-incident-response/org.json --team ir \
  --task "Contain a suspected credential-stuffing incident"

# Export it to your framework, or sync it to your board
agentforge export --file demos/03-ai-research-lab/org.json --framework crewai --code
agentforge pm --file demos/04-mobile-app-launch/org.json --platform trello --task "..."
```

Demos 02 and 05 are a matched pair: 02 **fails** a `--require-reports-to`
governance check (its lead is `principal` with no manager) and 05 **passes** the
same check (its lead is `exec`), so you can see exactly how the chain-of-command
rule behaves.

## Regenerating the org files

The `org.json` files are committed. To rebuild them from the agentforge API (so they
stay schema-valid by construction):

```sh
PYTHONPATH=. python demos/_build_orgs.py
```
