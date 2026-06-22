"""Tests for agentforge. No network — the mock backend is deterministic."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentforge import (  # noqa: E402
    TOOL_NAME, TOOL_VERSION, Agent, Team, Organization, from_template, TEMPLATES,
    personas, registry, Runtime, LocalMockBackend,
)
from agentforge.models import Persona  # noqa: E402
from agentforge.interop import frameworks as fw, pm, catalog  # noqa: E402
from agentforge.cli import main  # noqa: E402


def test_metadata():
    assert TOOL_NAME == "agentforge"
    assert TOOL_VERSION.count(".") == 2


def test_templates_build():
    assert set(TEMPLATES) >= {"software_team", "research_firm", "jtf_meridian"}
    for k in TEMPLATES:
        org = from_template(k)
        assert org.headcount() >= 1 and org.teams
        json.dumps(org.to_dict())  # round-trips
        # from_dict round-trip
        org2 = Organization.from_dict(org.to_dict())
        assert org2.headcount() == org.headcount()


def test_jtf_meridian_mirrors_divisions():
    org = from_template("jtf_meridian")
    team_keys = {t.key for t in org.teams}
    assert {"command", "blackbook", "nullbyte", "athena", "ironclad",
            "prometheus", "foundry"} <= team_keys
    assert org.agent("archon").experience == "exec"


def test_persona_and_prompt():
    p = personas.make_persona("skeptic")
    assert p.traits["skepticism"] >= 0.9
    a = Agent("x", "X", "Tester", persona=p, experience="senior",
              skills=["red_teaming"], tools=["code_exec"])
    sp = personas.system_prompt(a, "Org", "mission")
    assert "skeptic" in sp and "red_teaming" in sp and "senior" in sp


def test_registry():
    assert "coding" in registry.list_skills()
    assert registry.tool("llm")["cognis"]  # mapped to a cognis capability
    v = registry.validate(["coding", "nope_skill"], ["llm", "nope_tool"])
    assert v["unknown_skills"] == ["nope_skill"] and v["unknown_tools"] == ["nope_tool"]


def test_runtime_mock():
    org = from_template("research_firm")
    res = Runtime(LocalMockBackend()).run_team(org, "research", "assess the market")
    assert res.contributions and res.synthesis
    assert "offline mock" in next(iter(res.contributions.values()))
    json.dumps(res.to_dict())


def test_export_all_frameworks():
    org = from_template("software_team")
    for f in fw.EXPORTERS:
        out = fw.export(org, f)
        assert out["framework"] == f
        if f == "mermaid":
            assert out["diagram"].startswith("flowchart")
            continue
        # every agent represented
        n = len(org.all_agents())
        key = "agents" if "agents" in out else ("roles" if "roles" in out else "nodes")
        assert len(out[key]) == n
    # code generation for the two code-first ones
    assert "crewai" in fw.to_code(org, "crewai").lower()
    assert "conversableagent" in fw.to_code(org, "autogen").lower()
    try:
        fw.export(org, "nope"); assert False
    except ValueError:
        pass


def test_pm_sync_all():
    org = from_template("software_team")
    for plat in pm.ADAPTERS:
        out = pm.sync(org, plat, ["ship feature A", "fix bug B"])
        assert out["platform"] in (plat, "github_projects")
    try:
        pm.sync(org, "nope", []); assert False
    except ValueError:
        pass


def test_catalog():
    assert any(f["key"] == "crewai" for f in catalog.all_frameworks())
    assert any(f["key"] == "openhands" for f in catalog.all_frameworks())
    assert any(f["key"] == "taskweaver" for f in catalog.all_frameworks())
    assert any(p["key"] == "jira" for p in catalog.pm_suites())
    assert any(c["repo"] == "edgemesh" for c in catalog.cognis())


def test_cli():
    assert main(["templates"]) == 0
    assert main(["org", "--template", "jtf_meridian"]) == 0
    assert main(["agents", "--template", "research_firm", "--format", "json"]) == 0
    assert main(["personas"]) == 0
    assert main(["skills"]) == 0
    assert main(["run", "--template", "software_team", "--team", "eng",
                 "--task", "design an API"]) == 0
    assert main(["export", "--template", "software_team", "--framework", "crewai",
                 "--format", "json"]) == 0
    assert main(["export", "--template", "software_team", "--framework", "autogen", "--code"]) == 0
    assert main(["pm", "--template", "software_team", "--platform", "github",
                 "--task", "ship A", "--format", "json"]) == 0
    assert main(["frameworks"]) == 0
