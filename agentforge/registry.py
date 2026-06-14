"""
Skill + tool registry — the shared vocabulary agents reference. Skills are
capabilities (what an agent is good at); tools are callable integrations (what an
agent can use). The interop adapters map tool keys to each target framework's tool
objects, and to Cognis tools where there's a match.
"""
from __future__ import annotations

# skill key -> description
SKILLS = {
    "planning": "Decompose goals into actionable plans.",
    "research": "Gather, evaluate, and synthesize information.",
    "coding": "Write, refactor, and debug software.",
    "code_review": "Critically review code for bugs and quality.",
    "architecture": "Design systems and make build-vs-buy/scaling calls.",
    "data_analysis": "Analyze data and quantify findings.",
    "writing": "Produce clear docs, specs, and comms.",
    "security_review": "Find and reason about security risks.",
    "red_teaming": "Adversarially test assumptions, plans, and systems.",
    "project_mgmt": "Track work, dependencies, and delivery.",
    "ops": "Run, monitor, and keep systems healthy.",
    "design": "Design UX/visuals/interfaces.",
    "sales": "Qualify, pitch, and close.",
    "compliance": "Map work to regulatory/standard requirements.",
}

# tool key -> {desc, cognis (matching cognis repo/capability if any)}
TOOLS = {
    "web_search": {"desc": "Search the web.", "cognis": "cog4 research"},
    "code_exec": {"desc": "Execute code in a sandbox.", "cognis": "edgemesh node"},
    "file_io": {"desc": "Read/write files.", "cognis": ""},
    "shell": {"desc": "Run shell commands.", "cognis": ""},
    "github": {"desc": "Read/write GitHub issues, PRs, repos.", "cognis": "reposecure/ghaudit"},
    "sql": {"desc": "Query databases.", "cognis": "opengcp/openaws emulators"},
    "http": {"desc": "Call HTTP APIs.", "cognis": ""},
    "rag": {"desc": "Retrieve over a knowledge base.", "cognis": "ragkit/engram"},
    "llm": {"desc": "Call a language model.", "cognis": "edgemesh /v1 + the fleet"},
    "browser": {"desc": "Drive a headless browser.", "cognis": ""},
    "sanctions_screen": {"desc": "KYC/AML screening.", "cognis": "kycaml"},
    "chain_analytics": {"desc": "Blockchain forensics.", "cognis": "cryptotrace"},
    "hardware_plan": {"desc": "Plan/scale lab hardware.", "cognis": "labforge"},
}


def skill(key: str): return SKILLS.get(key)
def tool(key: str): return TOOLS.get(key)
def list_skills(): return dict(SKILLS)
def list_tools(): return dict(TOOLS)


def validate(skills: list, tools: list) -> dict:
    """Report which referenced skills/tools are unknown (extensible — unknowns are
    allowed but flagged)."""
    return {"unknown_skills": [s for s in skills if s not in SKILLS],
            "unknown_tools": [t for t in tools if t not in TOOLS]}
