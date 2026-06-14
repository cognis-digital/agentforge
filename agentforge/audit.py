"""
Audit trail — a structured, append-only record of what the agent org did: every
agent invocation, with timestamps, backend, and outcome. Enterprises need this for
traceability, debugging, and compliance. Writes JSONL when given a path, otherwise
keeps an in-memory log.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
import json
import time


@dataclass
class Event:
    ts: float
    kind: str                  # "agent_run" | "synthesis" | "policy_block" | "run_start" | "run_end"
    org: str = ""
    team: str = ""
    agent: str = ""
    backend: str = ""
    detail: str = ""

    def to_dict(self): return asdict(self)


class AuditTrail:
    def __init__(self, path: str | None = None):
        self.path = path
        self.events: list[Event] = []

    def record(self, kind: str, **fields) -> Event:
        e = Event(ts=time.time(), kind=kind, **fields)
        self.events.append(e)
        if self.path:
            with open(self.path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(e.to_dict()) + "\n")
        return e

    def summary(self) -> dict:
        kinds = {}
        for e in self.events:
            kinds[e.kind] = kinds.get(e.kind, 0) + 1
        agents = sorted({e.agent for e in self.events if e.agent})
        return {"events": len(self.events), "by_kind": kinds, "agents": agents}
