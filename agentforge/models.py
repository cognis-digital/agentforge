"""
agentforge domain model — define an organization of AI agents the way you'd define
a company: Organization -> Teams -> Agents, where each Agent carries a Role, a
Persona (personality), an experience level, Skills, and Tools.

Everything is plain dataclasses with to_dict/from_dict so an org round-trips to JSON
or YAML, and the interop adapters can translate it to CrewAI / AutoGen / LangGraph /
OpenHands / TaskWeaver / etc. and to project-management suites.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Optional

TOOL_NAME = "agentforge"
TOOL_VERSION = "0.2.1"

EXPERIENCE = ["intern", "junior", "mid", "senior", "staff", "principal", "exec"]


@dataclass
class Persona:
    """An agent's personality — shapes tone and how it reasons/communicates."""
    archetype: str = "operator"          # see personas.ARCHETYPES
    tone: str = "concise, direct"
    traits: dict = field(default_factory=dict)   # 0..1: rigor, creativity, risk, collaboration, skepticism
    motto: str = ""

    def to_dict(self): return asdict(self)


@dataclass
class Agent:
    key: str
    name: str
    role: str                             # job title / function
    persona: Persona = field(default_factory=Persona)
    experience: str = "mid"
    skills: list = field(default_factory=list)     # skill keys (registry)
    tools: list = field(default_factory=list)      # tool keys (registry)
    goals: str = ""
    model: str = "auto"                   # fleet slot / model hint; "auto" = backend default
    reports_to: Optional[str] = None      # agent key of manager

    def to_dict(self):
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Agent":
        p = d.get("persona") or {}
        return cls(key=d["key"], name=d.get("name", d["key"]), role=d.get("role", ""),
                   persona=Persona(**p) if isinstance(p, dict) else Persona(),
                   experience=d.get("experience", "mid"), skills=d.get("skills", []),
                   tools=d.get("tools", []), goals=d.get("goals", ""),
                   model=d.get("model", "auto"), reports_to=d.get("reports_to"))


@dataclass
class Team:
    key: str
    name: str
    mission: str = ""
    lead: Optional[str] = None            # agent key
    members: list = field(default_factory=list)   # list[Agent]

    def to_dict(self):
        return {"key": self.key, "name": self.name, "mission": self.mission,
                "lead": self.lead, "members": [m.to_dict() for m in self.members]}

    @classmethod
    def from_dict(cls, d: dict) -> "Team":
        return cls(key=d["key"], name=d.get("name", d["key"]), mission=d.get("mission", ""),
                   lead=d.get("lead"),
                   members=[Agent.from_dict(m) for m in d.get("members", [])])

    def agent(self, key: str) -> Optional[Agent]:
        return next((m for m in self.members if m.key == key), None)


@dataclass
class Organization:
    key: str
    name: str
    mission: str = ""
    teams: list = field(default_factory=list)     # list[Team]

    def to_dict(self):
        return {"tool": TOOL_NAME, "version": TOOL_VERSION, "key": self.key,
                "name": self.name, "mission": self.mission,
                "teams": [t.to_dict() for t in self.teams]}

    @classmethod
    def from_dict(cls, d: dict) -> "Organization":
        return cls(key=d["key"], name=d.get("name", d["key"]), mission=d.get("mission", ""),
                   teams=[Team.from_dict(t) for t in d.get("teams", [])])

    def all_agents(self) -> list:
        return [m for t in self.teams for m in t.members]

    def team(self, key: str) -> Optional[Team]:
        return next((t for t in self.teams if t.key == key), None)

    def agent(self, key: str) -> Optional[Agent]:
        return next((a for a in self.all_agents() if a.key == key), None)

    def headcount(self) -> int:
        return len(self.all_agents())
