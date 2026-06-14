"""
Project-management interop — map an agent org + its tasks onto popular PM suites so
human and agent work share one board. Each adapter returns the payload/mapping for
its target (no live API calls; wire a client + token to push).

Supported: GitHub Projects/Issues, Jira, Linear, Notion, Trello, Asana.
"""
from __future__ import annotations
from ..models import Organization


def _assignees(org: Organization) -> list:
    return [{"id": a.key, "name": a.name, "role": a.role, "team": t.key}
            for t in org.teams for a in t.members]


def to_github(org: Organization, tasks: list[str]) -> dict:
    return {"platform": "github_projects",
            "project": {"title": f"{org.name} — agent org", "body": org.mission},
            "labels": [t.key for t in org.teams] + ["agent"],
            "members": _assignees(org),
            "issues": [{"title": t, "labels": ["agent"], "body": "Owned by an agentforge agent."}
                       for t in tasks]}


def to_jira(org: Organization, tasks: list[str]) -> dict:
    return {"platform": "jira",
            "project": {"name": org.name, "key": org.key.upper()[:10]},
            "components": [{"name": t.name} for t in org.teams],
            "issues": [{"fields": {"summary": t, "issuetype": {"name": "Task"},
                                   "labels": ["agentforge"]}} for t in tasks]}


def to_linear(org: Organization, tasks: list[str]) -> dict:
    return {"platform": "linear",
            "team": {"name": org.name, "key": org.key.upper()[:5]},
            "labels": [t.key for t in org.teams],
            "issues": [{"title": t, "labelIds": ["agentforge"]} for t in tasks]}


def to_notion(org: Organization, tasks: list[str]) -> dict:
    return {"platform": "notion",
            "database": {"title": f"{org.name} Tasks",
                         "properties": {"Name": "title", "Owner": "select",
                                        "Team": "select", "Status": "status"}},
            "pages": [{"Name": t, "Status": "Backlog"} for t in tasks],
            "owners": [a["name"] for a in _assignees(org)]}


def to_trello(org: Organization, tasks: list[str]) -> dict:
    return {"platform": "trello",
            "board": {"name": org.name},
            "lists": ["Backlog", "In Progress", "Review", "Done"],
            "cards": [{"name": t, "idList": "Backlog"} for t in tasks]}


def to_asana(org: Organization, tasks: list[str]) -> dict:
    return {"platform": "asana",
            "project": {"name": org.name, "notes": org.mission},
            "tasks": [{"name": t, "tags": ["agentforge"]} for t in tasks]}


ADAPTERS = {"github": to_github, "jira": to_jira, "linear": to_linear,
            "notion": to_notion, "trello": to_trello, "asana": to_asana}


def sync(org: Organization, platform: str, tasks: list[str]) -> dict:
    fn = ADAPTERS.get((platform or "").lower())
    if not fn:
        raise ValueError(f"unknown PM platform '{platform}'; known: {', '.join(ADAPTERS)}")
    return fn(org, tasks or [])
