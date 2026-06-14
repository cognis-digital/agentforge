"""Catalog of everything agentforge interoperates with — agent frameworks, PM
suites, and the Cognis suite — for discovery (`agentforge frameworks`)."""

AGENT_FRAMEWORKS = [
    {"key": "crewai", "name": "CrewAI", "kind": "role-based crews", "export": True},
    {"key": "autogen", "name": "AutoGen / AG2", "kind": "conversable multi-agent", "export": True},
    {"key": "langgraph", "name": "LangGraph", "kind": "graph workflows", "export": True},
    {"key": "openhands", "name": "OpenHands", "kind": "autonomous software agents", "export": True},
    {"key": "taskweaver", "name": "TaskWeaver", "kind": "code-first agents", "export": True},
    {"key": "metagpt", "name": "MetaGPT", "kind": "SOP role agents", "export": True},
    {"key": "deepteam", "name": "DeepTeam", "kind": "LLM red-team personas",
     "export": False, "note": "map 'skeptic'/red_teaming agents to adversarial personas."},
    {"key": "langchain", "name": "LangChain", "kind": "agent/tool runtime", "export": False},
]

PM_SUITES = [
    {"key": "github", "name": "GitHub Projects/Issues"},
    {"key": "jira", "name": "Jira"},
    {"key": "linear", "name": "Linear"},
    {"key": "notion", "name": "Notion"},
    {"key": "trello", "name": "Trello"},
    {"key": "asana", "name": "Asana"},
]

COGNIS = [
    {"repo": "edgemesh", "role": "Model/compute backend — FleetBackend targets its /v1 endpoint."},
    {"repo": "cognis fleet (cog4)", "role": "Local models that run each agent (per-agent slot via Agent.model)."},
    {"repo": "jtf-meridian", "role": "Built-in org template mirroring the command structure."},
    {"repo": "cognis-connect", "role": "Emit agent outputs as the shared Finding contract."},
    {"repo": "labforge", "role": "Plan the hardware the agent org runs on."},
    {"repo": "kycaml / cryptotrace / ragkit", "role": "Tools agents call (tool registry maps to them)."},
]


def all_frameworks(): return list(AGENT_FRAMEWORKS)
def pm_suites(): return list(PM_SUITES)
def cognis(): return list(COGNIS)
