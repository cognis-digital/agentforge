# Demo 02 — SOC 2 Type II Readiness Program

**Where the data came from.** A GRC program getting an org audit-ready for a SOC 2
Type II examination: a GRC Program Lead, a Controls Analyst (maps Trust Services
Criteria to implemented controls), an Evidence Collector (automates access reviews,
change logs, backups), a Security Engineer (tests that controls actually hold), and
a Policy Writer. Five agents, one `grc` team.

**What to expect.** This org is deliberately useful for the **governance / policy**
feature: the program lead is a `principal` with no manager, so a
`--require-reports-to` policy check will flag exactly one chain-of-command gap — the
kind of finding `agentforge validate` surfaces in CI before you deploy an org.

## Run it

```sh
# 1. Validate the definition
agentforge schema --file demos/02-soc2-audit-readiness/org.json

# 2. Governance gate: require a chain of command, and flag tools that need sign-off.
#    Expect ok:false with ONE violation (grc_lead has no reports_to) and
#    github/shell listed under tools_needing_approval.
agentforge validate --file demos/02-soc2-audit-readiness/org.json \
  --require-reports-to --approval-required github,shell --format json

# 3. Run the controls workstream
agentforge run --file demos/02-soc2-audit-readiness/org.json --team grc \
  --task "Map our access-control practices to the relevant Trust Services Criteria"

# 4. Put the readiness backlog on a Jira board
agentforge pm --file demos/02-soc2-audit-readiness/org.json --platform jira \
  --task "Quarterly access review evidence" --task "Change-management policy v2" \
  --task "Backup restore test" --format json
```

## How to act on it

- **(2)** is the headline: in a real pipeline you'd run it in CI and fail the build
  on `ok:false`. Here it intentionally fails to demonstrate the check — give the
  lead a `reports_to` (or mark them `exec`) and it goes green.
- Tools flagged under `tools_needing_approval` are the ones a human must approve
  before an agent uses them — useful when an agent could push to GitHub or run a
  shell.
