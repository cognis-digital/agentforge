# Demo 05 — Acquisition Due-Diligence Deal Team

**Where the data came from.** A deal team diligencing an acquisition target across
financial, technical, legal, and security dimensions, led by a Deal Partner
(`exec`). The Security DD agent carries `sanctions_screen` and `chain_analytics`
(Cognis `kycaml` / `cryptotrace`) for counterparty and on-chain risk.

**What to expect.** Because the lead is `exec`, this org passes a strict
`--require-reports-to` governance check with **zero** violations — the contrast with
Demo 02 (where the lead is only `principal` and gets flagged) shows exactly how the
chain-of-command rule treats the exec tier.

## Run it

```sh
agentforge schema --file demos/05-due-diligence-deal-team/org.json

# Strict governance — expect ok:true, no violations (the partner is exec, so the
# chain-of-command rule does not require them to have a manager)
agentforge validate --file demos/05-due-diligence-deal-team/org.json \
  --require-reports-to --format json

# Run the deal team on the core diligence question
agentforge run --file demos/05-due-diligence-deal-team/org.json --team deal \
  --task "First-pass diligence on Target Co: each lead, your top risk and what evidence you need"

# Export to LangGraph — reports_to becomes the supervision graph
agentforge export --file demos/05-due-diligence-deal-team/org.json --framework langgraph
```

## How to act on it

- **validate** here is the positive control: pair it with Demo 02 to see a failing
  vs. passing chain-of-command gate.
- The **run** task gives you a structured first-pass risk register straight from the
  five diligence workstreams.
