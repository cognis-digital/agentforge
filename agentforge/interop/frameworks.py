"""
Export an agentforge Organization to popular agent frameworks. Each exporter returns
a plain dict (the framework's config shape) so it works without the framework
installed; `to_code` emits a runnable snippet for the two code-first ones.

Supported: CrewAI, AutoGen / AG2, LangGraph, OpenHands, TaskWeaver, MetaGPT.
"""
from __future__ import annotations
from ..models import Organization, Agent
from ..personas import system_prompt


def _sys(org, team, a): return system_prompt(a, org.name, team.mission)


def to_crewai(org: Organization) -> dict:
    agents, tasks = [], []
    for t in org.teams:
        for a in t.members:
            agents.append({"role": a.role, "goal": a.goals or f"Excel as {a.role}",
                           "backstory": _sys(org, t, a), "tools": a.tools,
                           "allow_delegation": a.experience in ("staff", "principal", "exec")})
            tasks.append({"description": f"{a.role} contributes to the org mission",
                          "agent": a.role, "expected_output": "a concrete deliverable"})
    return {"framework": "crewai", "agents": agents, "tasks": tasks,
            "process": "hierarchical"}


def to_autogen(org: Organization) -> dict:
    agents = [{"name": a.key, "system_message": _sys(org, t, a),
               "llm_config": {"model": a.model}}
              for t in org.teams for a in t.members]
    return {"framework": "autogen", "agents": agents,
            "group_chat": {"agents": [a["name"] for a in agents], "max_round": 12}}


def to_langgraph(org: Organization) -> dict:
    nodes = [{"id": a.key, "role": a.role, "system": _sys(org, t, a)}
             for t in org.teams for a in t.members]
    edges = [{"from": a.reports_to, "to": a.key}
             for t in org.teams for a in t.members if a.reports_to]
    return {"framework": "langgraph", "nodes": nodes, "edges": edges,
            "entrypoint": next((n["id"] for n in nodes), None)}


def to_openhands(org: Organization) -> dict:
    return {"framework": "openhands", "agents": [
        {"name": a.name, "system_prompt": _sys(org, t, a), "tools": a.tools,
         "llm": {"model": a.model}} for t in org.teams for a in t.members]}


def to_taskweaver(org: Organization) -> dict:
    return {"framework": "taskweaver", "roles": [
        {"name": a.key, "alias": a.name, "intro": _sys(org, t, a),
         "plugins": a.tools} for t in org.teams for a in t.members]}


def to_metagpt(org: Organization) -> dict:
    return {"framework": "metagpt", "roles": [
        {"name": a.name, "profile": a.role, "goal": a.goals or a.role,
         "constraints": a.persona.tone, "actions": a.skills}
        for t in org.teams for a in t.members]}


EXPORTERS = {
    "crewai": to_crewai, "autogen": to_autogen, "langgraph": to_langgraph,
    "openhands": to_openhands, "taskweaver": to_taskweaver, "metagpt": to_metagpt,
}


def export(org: Organization, framework: str) -> dict:
    fn = EXPORTERS.get((framework or "").lower())
    if not fn:
        raise ValueError(f"unknown framework '{framework}'; known: {', '.join(EXPORTERS)}")
    return fn(org)


def to_code(org: Organization, framework: str) -> str:
    """Runnable snippet for the code-first frameworks (crewai/autogen)."""
    fw = (framework or "").lower()
    if fw == "crewai":
        cfg = to_crewai(org)
        lines = ["from crewai import Agent, Task, Crew, Process", ""]
        for i, a in enumerate(cfg["agents"]):
            lines.append(f"a{i} = Agent(role={a['role']!r}, goal={a['goal']!r}, "
                         f"backstory={a['backstory'][:80]!r}...)")
        lines.append(f"# {len(cfg['agents'])} agents; build Tasks + Crew(process=Process.hierarchical)")
        return "\n".join(lines)
    if fw == "autogen":
        cfg = to_autogen(org)
        lines = ["from autogen import ConversableAgent, GroupChat, GroupChatManager", ""]
        for a in cfg["agents"]:
            lines.append(f"{a['name']} = ConversableAgent({a['name']!r}, "
                         f"system_message={a['system_message'][:60]!r}...)")
        lines.append(f"chat = GroupChat(agents=[{', '.join(a['name'] for a in cfg['agents'])}], "
                     f"max_round=12)")
        return "\n".join(lines)
    raise ValueError(f"to_code supports crewai/autogen; got '{framework}'")
