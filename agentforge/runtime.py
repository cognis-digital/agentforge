"""
Runtime — run an organization on a task, with enterprise hardening: a generic
OpenAI-compatible backend (any provider, not just the Cognis fleet), retries +
timeouts, per-agent error isolation, usage metering, optional policy enforcement,
and an audit trail.

Backends:
  LocalMockBackend  deterministic, offline (default; tool + tests run anywhere)
  OpenAIBackend     any OpenAI-compatible /v1 endpoint (OpenAI, Azure OpenAI, vLLM,
                    a gateway…); retries; raises BackendError on final failure
  FleetBackend      OpenAIBackend pointed at edgemesh/the local fleet, with a
                    graceful mock fallback for local dev
"""
from __future__ import annotations
from dataclasses import dataclass, field
import json
import time
import urllib.request

from .models import Organization, Agent
from . import personas


class BackendError(Exception):
    pass


class Backend:
    def run(self, agent: Agent, system: str, task: str) -> str:
        raise NotImplementedError


class LocalMockBackend(Backend):
    def run(self, agent: Agent, system: str, task: str) -> str:
        skills = ", ".join(agent.skills) or "general"
        return (f"[{agent.name} · {agent.role} · {agent.persona.archetype}] On "
                f"'{task[:80]}': would contribute using {skills}. Tone: "
                f"{agent.persona.tone}. (offline mock — set AGENTFORGE_BACKEND to go live.)")


class OpenAIBackend(Backend):
    """Generic OpenAI-compatible chat backend with retries + timeout."""
    def __init__(self, base_url="https://api.openai.com/v1", api_key="",
                 default_model="default", timeout=120, retries=2):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.default_model = default_model
        self.timeout = timeout
        self.retries = max(0, retries)

    def run(self, agent: Agent, system: str, task: str) -> str:
        model = agent.model if agent.model and agent.model != "auto" else self.default_model
        payload = json.dumps({"model": model, "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": task}]}).encode()
        last = None
        for attempt in range(self.retries + 1):
            try:
                req = urllib.request.Request(
                    f"{self.base_url}/chat/completions", data=payload,
                    headers={"Content-Type": "application/json",
                             "Authorization": f"Bearer {self.api_key}"})
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    data = json.loads(r.read().decode("utf-8", "replace"))
                return data["choices"][0]["message"]["content"].strip()
            except Exception as e:
                last = e
                if attempt < self.retries:
                    time.sleep(0.5 * (attempt + 1))
        raise BackendError(f"{self.base_url}: {type(last).__name__}: {last}")


class FleetBackend(OpenAIBackend):
    """edgemesh / local-fleet endpoint; falls back to the mock for local dev."""
    def __init__(self, base_url="http://127.0.0.1:8080/v1", api_key="local",
                 default_model="default", timeout=120, retries=1):
        super().__init__(base_url, api_key, default_model, timeout, retries)
        self._mock = LocalMockBackend()

    def run(self, agent, system, task):
        try:
            return super().run(agent, system, task)
        except BackendError:
            return self._mock.run(agent, system, task)


@dataclass
class RunResult:
    task: str
    org: str
    backend: str
    contributions: dict = field(default_factory=dict)
    synthesis: str = ""
    usage: dict = field(default_factory=dict)        # {"agent_calls": n, "errors": n}
    policy: dict = field(default_factory=dict)        # validation result if a policy was set

    def to_dict(self): return vars(self)


class Runtime:
    def __init__(self, backend: Backend = None, policy=None, audit=None):
        self.backend = backend or LocalMockBackend()
        self.policy = policy            # optional PolicyEngine
        self.audit = audit              # optional AuditTrail

    def _log(self, kind, **f):
        if self.audit:
            self.audit.record(kind, **f)

    def run_team(self, org: Organization, team_key: str, task: str,
                 synthesize: bool = True) -> RunResult:
        team = org.team(team_key)
        if not team:
            raise ValueError(f"unknown team '{team_key}'")
        bname = type(self.backend).__name__
        res = RunResult(task=task, org=org.key, backend=bname)
        self._log("run_start", org=org.key, team=team_key, backend=bname, detail=task[:120])

        if self.policy:
            res.policy = self.policy.validate(org)

        calls = errors = 0
        for a in team.members:
            sysp = personas.system_prompt(a, org.name, team.mission)
            try:
                res.contributions[a.key] = self.backend.run(a, sysp, task)
                calls += 1
                self._log("agent_run", org=org.key, team=team_key, agent=a.key, backend=bname)
            except BackendError as e:
                errors += 1
                res.contributions[a.key] = f"[error: {e}]"
                self._log("error", org=org.key, team=team_key, agent=a.key, detail=str(e))

        if synthesize and team.lead:
            lead = team.agent(team.lead) or team.members[0]
            joined = "\n".join(f"- {k}: {v}" for k, v in res.contributions.items())
            sysp = personas.system_prompt(lead, org.name, team.mission)
            try:
                res.synthesis = self.backend.run(
                    lead, sysp + "\nYou are the lead: synthesize the team's "
                    "contributions into one decision/recommendation.",
                    f"Task: {task}\n\nContributions:\n{joined}")
                calls += 1
                self._log("synthesis", org=org.key, team=team_key, agent=lead.key)
            except BackendError as e:
                errors += 1
                res.synthesis = f"[synthesis error: {e}]"

        res.usage = {"agent_calls": calls, "errors": errors}
        self._log("run_end", org=org.key, team=team_key, detail=json.dumps(res.usage))
        return res
