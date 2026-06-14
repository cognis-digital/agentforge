"""
Persona system — archetypes + traits that shape how an agent reasons and talks,
and a composer that turns (role + persona + experience + skills) into a system
prompt usable by any backend or exported framework.
"""
from __future__ import annotations
from .models import Persona, Agent

# archetype -> (default traits, default tone, one-line behavioral charter)
ARCHETYPES = {
    "strategist": ({"rigor": 0.8, "creativity": 0.7, "risk": 0.5, "collaboration": 0.6, "skepticism": 0.6},
                   "big-picture, decisive", "Sets direction; weighs second-order effects; commits."),
    "builder": ({"rigor": 0.7, "creativity": 0.6, "risk": 0.5, "collaboration": 0.6, "skepticism": 0.4},
                "pragmatic, hands-on", "Ships working things; bias to action and iteration."),
    "analyst": ({"rigor": 0.9, "creativity": 0.4, "risk": 0.3, "collaboration": 0.5, "skepticism": 0.7},
                "precise, evidence-first", "Quantifies, cites, and qualifies; distrusts hand-waving."),
    "skeptic": ({"rigor": 0.8, "creativity": 0.5, "risk": 0.2, "collaboration": 0.5, "skepticism": 0.95},
                "probing, adversarial", "Red-teams every claim; surfaces failure modes and assumptions."),
    "operator": ({"rigor": 0.7, "creativity": 0.4, "risk": 0.4, "collaboration": 0.7, "skepticism": 0.5},
                 "concise, direct", "Executes reliably; keeps things running; clear status."),
    "diplomat": ({"rigor": 0.6, "creativity": 0.6, "risk": 0.4, "collaboration": 0.9, "skepticism": 0.4},
                 "warm, aligning", "Builds consensus; translates between stakeholders."),
    "researcher": ({"rigor": 0.85, "creativity": 0.8, "risk": 0.5, "collaboration": 0.5, "skepticism": 0.7},
                   "curious, thorough", "Explores broadly, synthesizes, cites sources, flags uncertainty."),
    "creative": ({"rigor": 0.4, "creativity": 0.95, "risk": 0.7, "collaboration": 0.6, "skepticism": 0.3},
                 "expansive, generative", "Generates many novel options; defers judgment."),
}

EXPERIENCE_NOTE = {
    "intern": "Learning; ask when unsure; small scoped tasks.",
    "junior": "Executes well-specified tasks; escalates ambiguity.",
    "mid": "Owns features end-to-end with light guidance.",
    "senior": "Owns ambiguous problems; mentors; sets local standards.",
    "staff": "Drives cross-team technical direction; force-multiplier.",
    "principal": "Sets strategy for a domain; final technical authority.",
    "exec": "Sets organizational direction; allocates effort; accountable for outcomes.",
}


def make_persona(archetype: str = "operator", **overrides) -> Persona:
    a = ARCHETYPES.get(archetype, ARCHETYPES["operator"])
    p = Persona(archetype=archetype, tone=overrides.get("tone", a[1]),
                traits=dict(a[0]), motto=overrides.get("motto", a[2]))
    if "traits" in overrides:
        p.traits.update(overrides["traits"])
    return p


def system_prompt(agent: Agent, org_name: str = "", team_mission: str = "") -> str:
    p = agent.persona
    charter = ARCHETYPES.get(p.archetype, ARCHETYPES["operator"])[2]
    traits = ", ".join(f"{k} {v:.1f}" for k, v in sorted(p.traits.items()))
    lines = [
        f"You are {agent.name}, a {agent.experience}-level {agent.role}"
        + (f" at {org_name}" if org_name else "") + ".",
        f"Archetype: {p.archetype} — {charter} Tone: {p.tone}.",
        f"Personality traits (0-1): {traits}." if traits else "",
        f"Experience: {EXPERIENCE_NOTE.get(agent.experience, '')}",
        f"Skills: {', '.join(agent.skills)}." if agent.skills else "",
        f"Tools available: {', '.join(agent.tools)}." if agent.tools else "",
        f"Goals: {agent.goals}" if agent.goals else "",
        f"Team mission: {team_mission}" if team_mission else "",
        "Stay in role. Be honest about uncertainty. Produce useful, decision-ready output.",
    ]
    return "\n".join(l for l in lines if l)
