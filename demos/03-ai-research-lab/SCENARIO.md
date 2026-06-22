# Demo 03 — Applied AI Research Lab

**Where the data came from.** A two-team research org: a `research` team (Principal
Investigator, Research Scientist, Research Engineer, and a Reproducibility Skeptic
whose whole job is to break results before they ship) and an `ml_infra` team (ML
Infra Lead + Data Engineer) that keeps training and eval reproducible. Six agents
across two teams — the first multi-team demo, so you can run each team separately.

**What to expect.** Two teams means two leads and two `run` targets. The skeptic
agent carries `red_teaming`; the infra lead carries the `hardware_plan` tool (maps
to Cognis `labforge`).

## Run it

```sh
agentforge schema --file demos/03-ai-research-lab/org.json

# Run the research team on a framing task
agentforge run --file demos/03-ai-research-lab/org.json --team research \
  --task "Design an eval to measure retrieval grounding on long documents"

# Run the infra team on a different task
agentforge run --file demos/03-ai-research-lab/org.json --team ml_infra \
  --task "Make our training runs bit-for-bit reproducible across the cluster"

# Export the whole lab to CrewAI (hierarchical process), with runnable code
agentforge export --file demos/03-ai-research-lab/org.json --framework crewai --code

# Visualize the two-team org chart (paste into a GitHub README / Notion page)
agentforge export --file demos/03-ai-research-lab/org.json --framework mermaid --code
```

## How to act on it

- Run the two teams independently, or export to CrewAI and let a hierarchical crew
  coordinate them.
- The **mermaid** export drops straight into any Markdown that renders Mermaid
  (GitHub, GitLab, Notion, Obsidian) so the lab's structure is reviewable as a
  diagram, not just JSON.
