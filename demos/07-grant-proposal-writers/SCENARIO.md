# Demo 07 — Federal Grant Proposal Team

**Where the data came from.** A team assembling a competitive federal R&D grant: a
Principal Investigator, a Lead Proposal Writer, a Budget Analyst, a Compliance
Reviewer (checks every solicitation requirement), and a Red Team Reviewer who grades
the draft like the review panel will. Five agents, one `proposal` team.

**What to expect.** A writing/compliance-heavy org. The Red Team Reviewer
(`skeptic`, `red_teaming`) and Compliance Reviewer (`staff`, `compliance`) make this
a good demo of how persona + skills shape the exported system prompts.

## Run it

```sh
agentforge schema --file demos/07-grant-proposal-writers/org.json

# See how each role's persona becomes a system prompt (look at the 'system' fields)
agentforge export --file demos/07-grant-proposal-writers/org.json --framework langgraph

# Run the team on a draft-review pass
agentforge run --file demos/07-grant-proposal-writers/org.json --team proposal \
  --task "Review our 3-page technical narrative against the solicitation; what loses us points?"

# Track the proposal workstreams in Notion
agentforge pm --file demos/07-grant-proposal-writers/org.json --platform notion \
  --task "Technical narrative draft 1" --task "Budget + justification" \
  --task "Compliance matrix" --task "Red-team review" --format json
```

## How to act on it

- Read the `system` fields in the **langgraph** export to see the Red Team Reviewer
  is instructed to grade adversarially while the Writer is instructed to align and
  translate — same task, different behavior, driven by persona.
- **run** gives you a fast panel-style critique before you submit.
