"""
JSON Schema for an agentforge Organization definition.

An org is org-as-config kept in version control (see `docs/ENTERPRISE.md`). To
review and gate those JSON/YAML files like code you need a machine-readable contract:
this module emits a standards-compliant JSON Schema (Draft 2020-12) describing the
`Organization -> Teams -> Agents` shape, the persona/experience/skill/tool vocabulary,
and the cross-references (`lead`, `reports_to`).

Use it to:
  - validate org files in CI (`agentforge schema` | any JSON-Schema validator),
  - get editor autocomplete/linting via `$schema` in your org JSON,
  - publish a stable contract other Cognis tools can target.

Pure standard library; the schema is generated from the live registries/personas so
it never drifts from the code.
"""
from __future__ import annotations

from . import personas, registry
from .models import EXPERIENCE, TOOL_NAME, TOOL_VERSION

SCHEMA_ID = "https://github.com/cognis-digital/agentforge/schema/org.schema.json"


def org_schema() -> dict:
    """Return the JSON Schema (Draft 2020-12) for an Organization document."""
    archetypes = sorted(personas.ARCHETYPES)
    skills = sorted(registry.SKILLS)
    tools = sorted(registry.TOOLS)

    persona = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "archetype": {"type": "string", "enum": archetypes,
                          "description": "Personality archetype (shapes tone/reasoning)."},
            "tone": {"type": "string"},
            "traits": {
                "type": "object",
                "description": "0..1 trait weights.",
                "additionalProperties": {"type": "number", "minimum": 0, "maximum": 1},
            },
            "motto": {"type": "string"},
        },
    }

    agent = {
        "type": "object",
        "required": ["key", "role"],
        "additionalProperties": False,
        "properties": {
            "key": {"type": "string", "minLength": 1,
                    "description": "Unique agent id within the org."},
            "name": {"type": "string"},
            "role": {"type": "string", "description": "Job title / function."},
            "persona": persona,
            "experience": {"type": "string", "enum": list(EXPERIENCE)},
            "skills": {"type": "array", "items": {"type": "string", "enum": skills},
                       "description": "Skill keys from the registry."},
            "tools": {"type": "array", "items": {"type": "string", "enum": tools},
                      "description": "Tool keys from the registry."},
            "goals": {"type": "string"},
            "model": {"type": "string",
                      "description": "Fleet slot / model hint; 'auto' = backend default."},
            "reports_to": {"type": ["string", "null"],
                           "description": "agent key of this agent's manager."},
        },
    }

    team = {
        "type": "object",
        "required": ["key", "members"],
        "additionalProperties": False,
        "properties": {
            "key": {"type": "string", "minLength": 1},
            "name": {"type": "string"},
            "mission": {"type": "string"},
            "lead": {"type": ["string", "null"],
                     "description": "agent key of the team lead (must be a member)."},
            "members": {"type": "array", "items": agent},
        },
    }

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": SCHEMA_ID,
        "title": "agentforge Organization",
        "description": (
            "An organization of AI agents (roles, personalities, experience, skills, "
            "tools) as defined by agentforge."),
        "type": "object",
        "required": ["key", "teams"],
        "additionalProperties": False,
        "properties": {
            "tool": {"const": TOOL_NAME},
            "version": {"type": "string"},
            "key": {"type": "string", "minLength": 1},
            "name": {"type": "string"},
            "mission": {"type": "string"},
            "teams": {"type": "array", "items": team},
        },
        "x-agentforge": {
            "archetypes": archetypes,
            "experience_levels": list(EXPERIENCE),
            "skills": skills,
            "tools": tools,
            "generated_for_version": TOOL_VERSION,
        },
    }


def _err(path: str, msg: str) -> dict:
    return {"path": path, "error": msg}


def validate_doc(doc: dict) -> dict:
    """Validate an org *document* (dict) against the contract, without needing a
    third-party validator. Checks structure, the enum vocabularies, unique keys,
    and the `lead`/`reports_to` cross-references. Returns {ok, errors[]}."""
    errors: list = []
    archetypes = set(personas.ARCHETYPES)
    skills = set(registry.SKILLS)
    tools = set(registry.TOOLS)
    exp = set(EXPERIENCE)

    if not isinstance(doc, dict):
        return {"ok": False, "errors": [_err("$", "document must be an object")]}
    if not doc.get("key"):
        errors.append(_err("$.key", "required, non-empty"))
    teams = doc.get("teams")
    if not isinstance(teams, list):
        errors.append(_err("$.teams", "required array of teams"))
        return {"ok": not errors, "errors": errors}

    seen_team_keys: set = set()
    all_agent_keys: set = set()
    for ti, t in enumerate(teams):
        tp = f"$.teams[{ti}]"
        if not isinstance(t, dict) or not t.get("key"):
            errors.append(_err(tp + ".key", "required, non-empty"))
            continue
        if t["key"] in seen_team_keys:
            errors.append(_err(tp + ".key", f"duplicate team key '{t['key']}'"))
        seen_team_keys.add(t["key"])
        members = t.get("members") or []
        member_keys = set()
        for mi, m in enumerate(members):
            mp = f"{tp}.members[{mi}]"
            if not isinstance(m, dict) or not m.get("key"):
                errors.append(_err(mp + ".key", "required, non-empty"))
                continue
            if not m.get("role"):
                errors.append(_err(mp + ".role", "required"))
            if m["key"] in all_agent_keys:
                errors.append(_err(mp + ".key", f"duplicate agent key '{m['key']}'"))
            member_keys.add(m["key"])
            all_agent_keys.add(m["key"])
            e = m.get("experience", "mid")
            if e not in exp:
                errors.append(_err(mp + ".experience", f"'{e}' not in {sorted(exp)}"))
            p = m.get("persona") or {}
            arch = p.get("archetype")
            if arch is not None and arch not in archetypes:
                errors.append(_err(mp + ".persona.archetype",
                                   f"'{arch}' not in {sorted(archetypes)}"))
            for s in m.get("skills", []):
                if s not in skills:
                    errors.append(_err(mp + ".skills", f"unknown skill '{s}'"))
            for tl in m.get("tools", []):
                if tl not in tools:
                    errors.append(_err(mp + ".tools", f"unknown tool '{tl}'"))
        lead = t.get("lead")
        if lead is not None and lead not in member_keys:
            errors.append(_err(tp + ".lead", f"lead '{lead}' is not a member of the team"))

    # reports_to must reference some agent in the org
    for ti, t in enumerate(teams):
        for mi, m in enumerate(t.get("members") or []):
            if not isinstance(m, dict):
                continue
            rt = m.get("reports_to")
            if rt is not None and rt not in all_agent_keys:
                errors.append(_err(f"$.teams[{ti}].members[{mi}].reports_to",
                                   f"reports_to '{rt}' is not an agent in this org"))
    return {"ok": not errors, "errors": errors}
