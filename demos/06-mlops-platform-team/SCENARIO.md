# Demo 06 — MLOps Platform Team

**Where the data came from.** The team that runs an internal ML platform: a
Platform Lead, a Serving Engineer (low-latency serving + autoscaling), a Pipelines
Engineer (training/eval + data lineage), an Observability Engineer (metrics, drift,
alerting), and an ML Security Reviewer. Five agents, one `platform` team.

**What to expect.** A heavily ops-flavored org (lots of `ops`, `shell`, `http`,
`hardware_plan`). It's the ideal target for a **tool allow/deny policy**: in a real
deploy you'd deny `shell` to most roles and require approval on anything that
touches prod.

## Run it

```sh
agentforge schema --file demos/06-mlops-platform-team/org.json

# Run the team on an on-call-style task
agentforge run --file demos/06-mlops-platform-team/org.json --team platform \
  --task "Serving p99 latency doubled after the 2pm deploy — each role, your first check"

# Governance: flag the privileged tools so a human signs off before use
agentforge validate --file demos/06-mlops-platform-team/org.json \
  --approval-required shell,http --format json

# Export to OpenHands (autonomous software agents) with per-agent tools
agentforge export --file demos/06-mlops-platform-team/org.json --framework openhands

# Org chart as Mermaid
agentforge export --file demos/06-mlops-platform-team/org.json --framework mermaid --code
```

## How to act on it

- The **validate** call lists which agents hold `shell`/`http` so you know what an
  approval workflow has to gate.
- **OpenHands** export carries each agent's `tools`, so the autonomous agents only
  get the integrations their role is supposed to touch.
