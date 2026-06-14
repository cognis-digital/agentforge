"""
Governance policy engine — the controls an enterprise needs before it lets an agent
org act: which tools are allowed (globally or per role), which require human
approval, and a budget cap on agent calls. Validate an org against policy before
deploying it, and gate tool use at runtime.
"""
from __future__ import annotations
from dataclasses import dataclass, field

from .models import Organization, Agent


@dataclass
class Policy:
    allowed_tools: list = field(default_factory=list)     # empty = allow any not denied
    denied_tools: list = field(default_factory=list)
    approval_required: list = field(default_factory=list)  # tools needing human sign-off
    role_tools: dict = field(default_factory=dict)         # role -> allowed tool list
    max_agent_calls: int = 0                               # 0 = unlimited
    require_reports_to: bool = False                       # every non-exec must have a manager

    def to_dict(self): return vars(self)


@dataclass
class Decision:
    allow: bool
    needs_approval: bool = False
    reason: str = ""


class PolicyEngine:
    def __init__(self, policy: Policy = None):
        self.policy = policy or Policy()

    def check(self, agent: Agent, tool: str) -> Decision:
        p = self.policy
        if tool in p.denied_tools:
            return Decision(False, reason=f"tool '{tool}' is denied by policy")
        role_allow = p.role_tools.get(agent.role)
        if role_allow is not None and tool not in role_allow:
            return Decision(False, reason=f"role '{agent.role}' may not use '{tool}'")
        if p.allowed_tools and tool not in p.allowed_tools:
            return Decision(False, reason=f"tool '{tool}' not in the global allowlist")
        if tool in p.approval_required:
            return Decision(True, needs_approval=True,
                            reason=f"tool '{tool}' requires human approval")
        return Decision(True)

    def validate(self, org: Organization) -> dict:
        """Pre-deploy check: list every policy violation across the org."""
        violations = []
        for a in org.all_agents():
            for tool in a.tools:
                d = self.check(a, tool)
                if not d.allow:
                    violations.append({"agent": a.key, "tool": tool, "reason": d.reason})
            if self.policy.require_reports_to and a.experience != "exec" and not a.reports_to:
                violations.append({"agent": a.key, "tool": None,
                                   "reason": "non-exec agent has no reports_to (chain of command)"})
        approvals = sorted({t for a in org.all_agents() for t in a.tools
                            if t in self.policy.approval_required})
        return {"ok": not violations, "violations": violations,
                "tools_needing_approval": approvals,
                "headcount": org.headcount(),
                "budget_calls": self.policy.max_agent_calls or "unlimited"}
