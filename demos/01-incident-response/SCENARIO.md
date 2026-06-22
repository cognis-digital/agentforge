# Demo 01 — Sev-1 Incident Response Cell

**Where the data came from.** A platform team's incident-response runbook, encoded
as an agentforge org: an Incident Commander, a Forensics Lead, a Threat Hunter, an
SRE on-call, and a Comms/Legal liaison — the roles you actually staff a security
bridge with. The org is defensive: contain, investigate, recover, notify.

**What to expect.** `org.json` is a 5-agent, single-team org (`ir`) with a clean
chain of command (everyone `reports_to` the Incident Commander). It validates
against the agentforge schema, runs on a task with the offline mock backend, and
exports to any framework.

## Run it

```sh
# 1. Sanity-check the org definition against the published schema
agentforge schema --file demos/01-incident-response/org.json

# 2. Run the cell on a live-looking task (offline mock backend — deterministic)
agentforge run --file demos/01-incident-response/org.json --team ir \
  --task "Contain a suspected credential-stuffing incident on the auth service"

# 3. Stand up the incident bridge as GitHub issues, one per workstream
agentforge pm --file demos/01-incident-response/org.json --platform github \
  --task "Rotate exposed credentials" --task "Build the forensic timeline" \
  --task "Draft customer + regulator notification" --format json

# 4. Hand the cell to LangGraph (the reports_to chain becomes graph edges)
agentforge export --file demos/01-incident-response/org.json --framework langgraph
```

## How to act on it

- Use **(2)** to get each role's first-move framing on the bridge.
- Use **(3)** to spin a board where each containment/forensics/comms workstream is
  an issue owned by the right agent.
- Wire `AGENTFORGE_BACKEND=fleet` (or `openai`) to run the cell against a real model
  instead of the mock; the system prompts carry each role's persona and tools.
