"""
Runtime — actually run an organization on a task.

A Backend produces an agent's contribution. `LocalMockBackend` is deterministic and
offline (so the tool + tests run anywhere). `FleetBackend` calls a local Cognis
fleet / edgemesh OpenAI-compatible endpoint (cognis interop) — each agent's persona
becomes the system prompt and its `model` selects a slot. The `Runtime` assigns a
task across a team, collects contributions, and (optionally) has the team lead
synthesize a result.
"""
from __future__ import annotations
from dataclasses import dataclass, field
import json
import urllib.request

from .models import Organization, Team, Agent
from . import personas


class Backend:
    def run(self, agent: Agent, system: str, task: str) -> str:
        raise NotImplementedError


class LocalMockBackend(Backend):
    """Deterministic, no network — describes what each agent would contribute."""
    def run(self, agent: Agent, system: str, task: str) -> str:
        skills = ", ".join(agent.skills) or "general"
        return (f"[{agent.name} · {agent.role} · {agent.persona.archetype}] On '{task[:80]}': "
                f"would contribute using {skills}. Tone: {agent.persona.tone}. "
                f"(offline mock — connect a FleetBackend for live output.)")


class FleetBackend(Backend):
    """OpenAI-compatible endpoint (edgemesh :8080/v1 or a fleet slot). Falls back to
    the mock string if the endpoint is unreachable, so callers never hard-fail."""
    def __init__(self, base_url="http://127.0.0.1:8080/v1", api_key="local",
                 timeout=120):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self._mock = LocalMockBackend()

    def run(self, agent: Agent, system: str, task: str) -> str:
        model = agent.model if agent.model and agent.model != "auto" else "default"
        payload = json.dumps({"model": model, "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": task}]}).encode()
        try:
            req = urllib.request.Request(
                f"{self.base_url}/chat/completions", data=payload,
                headers={"Content-Type": "application/json",
                         "Authorization": f"Bearer {self.api_key}"})
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                data = json.loads(r.read().decode("utf-8", "replace"))
            return data["choices"][0]["message"]["content"].strip()
        except Exception:
            return self._mock.run(agent, system, task)


@dataclass
class RunResult:
    task: str
    org: str
    contributions: dict = field(default_factory=dict)   # agent_key -> text
    synthesis: str = ""
    backend: str = ""

    def to_dict(self): return vars(self)


class Runtime:
    def __init__(self, backend: Backend = None):
        self.backend = backend or LocalMockBackend()

    def run_team(self, org: Organization, team_key: str, task: str,
                 synthesize: bool = True) -> RunResult:
        team = org.team(team_key)
        if not team:
            raise ValueError(f"unknown team '{team_key}'")
        res = RunResult(task=task, org=org.key, backend=type(self.backend).__name__)
        for a in team.members:
            sysp = personas.system_prompt(a, org.name, team.mission)
            res.contributions[a.key] = self.backend.run(a, sysp, task)
        if synthesize and team.lead:
            lead = team.agent(team.lead) or team.members[0]
            joined = "\n".join(f"- {k}: {v}" for k, v in res.contributions.items())
            sysp = personas.system_prompt(lead, org.name, team.mission)
            res.synthesis = self.backend.run(
                lead, sysp + "\nYou are the lead: synthesize the team's contributions "
                "into a single decision/recommendation.",
                f"Task: {task}\n\nTeam contributions:\n{joined}")
        return res
