"""
Ready-made organization templates. Build a full agent org in one call, then
customize. `jtf_meridian` mirrors the Cognis JTF MERIDIAN command structure so an
agentforge org maps 1:1 onto the company's real divisions (cognis interop).
"""
from __future__ import annotations
from .models import Organization, Team, Agent
from .personas import make_persona


def _a(key, name, role, arch, exp, skills, tools, goals="", reports_to=None):
    return Agent(key=key, name=name, role=role, persona=make_persona(arch),
                 experience=exp, skills=skills, tools=tools, goals=goals,
                 reports_to=reports_to)


def software_team() -> Organization:
    t = Team("eng", "Engineering", "Ship reliable software.", lead="em", members=[
        _a("em", "Morgan", "Engineering Manager", "strategist", "principal",
           ["planning", "project_mgmt"], ["github"], "Deliver the roadmap."),
        _a("arch", "Avi", "Staff Architect", "strategist", "staff",
           ["architecture", "code_review"], ["github", "code_exec"], reports_to="em"),
        _a("be", "Bao", "Backend Engineer", "builder", "senior",
           ["coding", "architecture"], ["code_exec", "github", "sql"], reports_to="em"),
        _a("fe", "Frankie", "Frontend Engineer", "builder", "mid",
           ["coding", "design"], ["code_exec", "github"], reports_to="em"),
        _a("qa", "Quinn", "QA / Test", "skeptic", "senior",
           ["code_review", "red_teaming"], ["code_exec"], "Break it before users do.", reports_to="em"),
        _a("sre", "Sam", "SRE", "operator", "senior",
           ["ops"], ["shell", "http"], reports_to="em"),
    ])
    return Organization("software_team", "Software Team",
                        "A full software delivery team.", teams=[t])


def research_firm() -> Organization:
    t = Team("research", "Research", "Produce decision-ready, sourced analysis.", lead="lead",
             members=[
        _a("lead", "Lena", "Research Lead", "strategist", "principal",
           ["planning", "writing"], ["rag"], "Frame questions; synthesize."),
        _a("r1", "Rafa", "Researcher", "researcher", "senior",
           ["research"], ["web_search", "rag"], reports_to="lead"),
        _a("r2", "Remy", "Researcher", "researcher", "mid",
           ["research"], ["web_search"], reports_to="lead"),
        _a("an", "Ana", "Quant Analyst", "analyst", "senior",
           ["data_analysis"], ["sql", "code_exec"], reports_to="lead"),
        _a("sk", "Soren", "Devil's Advocate", "skeptic", "staff",
           ["red_teaming"], [], "Refute every conclusion.", reports_to="lead"),
        _a("wr", "Wren", "Writer", "diplomat", "senior",
           ["writing"], [], reports_to="lead"),
    ])
    return Organization("research_firm", "Research Firm",
                        "A multi-analyst research org.", teams=[t])


def jtf_meridian() -> Organization:
    """Mirrors the Cognis JTF MERIDIAN 6-division command structure."""
    divs = [
        ("blackbook", "TF BLACKBOOK", "ORACLE", "Quant / Finance", "analyst",
         ["data_analysis"], ["sql", "code_exec"]),
        ("nullbyte", "GHOST CELL NULLBYTE", "SPECTER", "Cyber / Security", "skeptic",
         ["security_review", "red_teaming"], ["sanctions_screen", "chain_analytics"]),
        ("athena", "DIV-6 ATHENA-PRIME", "SAGE", "AI / R&D", "researcher",
         ["research", "architecture"], ["llm", "rag", "hardware_plan"]),
        ("ironclad", "TF IRONCLAD", "ANVIL", "GovCon / Compliance", "operator",
         ["compliance", "project_mgmt"], ["http"]),
        ("prometheus", "TF PROMETHEUS", "FORGE", "Energy", "strategist",
         ["research", "data_analysis"], ["web_search"]),
        ("foundry", "TF FOUNDRY", "MASON", "Revenue / Delivery", "builder",
         ["coding", "project_mgmt"], ["github", "code_exec"]),
    ]
    teams = []
    for key, name, callsign, domain, arch, skills, tools in divs:
        lead = _a(f"{key}_lead", callsign, f"{name} Lead", arch, "principal",
                  skills, tools, f"Own the {domain} domain.")
        teams.append(Team(key, name, f"{domain} division.", lead=lead.key, members=[lead]))
    org = Organization("jtf_meridian", "JTF MERIDIAN",
                       "Cognis Digital's 6-division command structure as an agent org.",
                       teams=teams)
    # ARCHON command element as its own team
    archon = _a("archon", "ARCHON", "Commander", "strategist", "exec",
                ["planning"], [], "Set intent; synthesize the common operating picture.")
    org.teams.insert(0, Team("command", "JTF MERIDIAN Command",
                             "Cross-division authority.", lead="archon", members=[archon]))
    return org


TEMPLATES = {
    "software_team": software_team,
    "research_firm": research_firm,
    "jtf_meridian": jtf_meridian,
}


def from_template(name: str) -> Organization:
    fn = TEMPLATES.get(name)
    if not fn:
        raise ValueError(f"unknown template '{name}'; known: {', '.join(TEMPLATES)}")
    return fn()
