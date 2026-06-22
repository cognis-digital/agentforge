# Demo 09 — Energy-Sector Trading Research Desk

**Where the data came from.** A research desk that produces sourced theses on energy
and power-infrastructure equities: a Head of Research, a Macro/Energy Analyst, a
Quant Analyst, a Risk Manager (whose job is to refute every thesis and cap
downside), and a Desk Writer who publishes the morning note. Five agents, one `desk`
team. This mirrors a real sell-side/buy-side research structure.

**What to expect.** A research org built around an adversarial check: the Risk
Manager is a `skeptic` with `red_teaming`, so when you run the desk you get theses
*and* their rebuttals before the lead synthesizes a call.

## Run it

```sh
agentforge schema --file demos/09-energy-trading-desk/org.json

# Run the desk on a thesis — analysts propose, risk refutes, head synthesizes
agentforge run --file demos/09-energy-trading-desk/org.json --team desk \
  --task "Build the bull and bear case for grid-scale power infrastructure into year-end"

# Export to CrewAI hierarchical crew (the head delegates)
agentforge export --file demos/09-energy-trading-desk/org.json --framework crewai --code

# Org chart for the desk
agentforge export --file demos/09-energy-trading-desk/org.json --framework mermaid --code

# Put the research agenda on a Linear board
agentforge pm --file demos/09-energy-trading-desk/org.json --platform linear \
  --task "Power-demand supply/demand update" --task "Backtest the momentum signal" \
  --task "Risk: concentration + drawdown review" --format json
```

## How to act on it

- The **run** synthesis is the desk's actual call, with the Risk Manager's
  objections already folded in — exactly the workflow a research head wants.
- Point `AGENTFORGE_BACKEND` at the local fleet to run the desk on your own models;
  per-agent `model` hints let you route the quant and the writer to different slots.

> Illustrative org structure and tasks only — not investment advice.
