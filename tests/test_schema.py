"""Tests for the org JSON Schema export + the dependency-free doc validator,
the Mermaid exporter, and the committed demos."""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentforge import from_template, TEMPLATES, org_schema, validate_doc  # noqa: E402
from agentforge.schema import SCHEMA_ID  # noqa: E402
from agentforge.interop import frameworks as fw  # noqa: E402
from agentforge.cli import main  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_org_schema_shape():
    s = org_schema()
    assert s["$schema"].endswith("2020-12/schema")
    assert s["$id"] == SCHEMA_ID
    assert s["properties"]["tool"]["const"] == "agentforge"
    assert "teams" in s["required"] and "key" in s["required"]
    # vocabularies are generated from the live registries
    x = s["x-agentforge"]
    assert "strategist" in x["archetypes"]
    assert "coding" in x["skills"] and "github" in x["tools"]
    assert "exec" in x["experience_levels"]


def test_schema_validates_with_jsonschema_if_present():
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return  # optional dependency; the dependency-free validator covers it
    s = org_schema()
    Draft202012Validator.check_schema(s)  # the schema itself is valid
    v = Draft202012Validator(s)
    for k in TEMPLATES:
        assert not list(v.iter_errors(from_template(k).to_dict()))


def test_validate_doc_passes_templates():
    for k in TEMPLATES:
        rep = validate_doc(from_template(k).to_dict())
        assert rep["ok"], (k, rep["errors"])


def test_validate_doc_catches_errors():
    bad = {"key": "x", "teams": [{"key": "t", "lead": "ghost", "members": [
        {"key": "a", "role": "Dev", "experience": "wizard",
         "skills": ["flying"], "tools": ["teleport"], "reports_to": "nobody"},
        {"key": "a", "role": "Dup"}]}]}
    rep = validate_doc(bad)
    assert not rep["ok"]
    paths = {e["path"] for e in rep["errors"]}
    msgs = " ".join(e["error"] for e in rep["errors"])
    assert "$.teams[0].members[0].experience" in paths
    assert "unknown skill 'flying'" in msgs
    assert "unknown tool 'teleport'" in msgs
    assert "duplicate agent key 'a'" in msgs
    assert any("lead 'ghost'" in e["error"] for e in rep["errors"])
    assert any("reports_to 'nobody'" in e["error"] for e in rep["errors"])


def test_validate_doc_rejects_non_object():
    assert not validate_doc([])["ok"]
    assert not validate_doc({"key": "x"})["ok"]  # missing teams


def test_mermaid_export():
    org = from_template("software_team")
    out = fw.export(org, "mermaid")
    assert out["framework"] == "mermaid"
    d = out["diagram"]
    assert d.startswith("flowchart TD")
    # every agent is a node, every reports_to is an edge
    for a in org.all_agents():
        assert a.key in d
        if a.reports_to:
            assert f"{a.reports_to} --> {a.key}" in d
    # to_code returns the diagram string
    assert fw.to_code(org, "mermaid") == d
    assert "mermaid" in fw.EXPORTERS


def test_cli_schema():
    # emit the schema
    assert main(["schema", "--format", "json"]) == 0
    # validate a clean template -> 0
    assert main(["schema", "--template", "jtf_meridian"]) == 0


def test_cli_export_mermaid():
    assert main(["export", "--template", "research_firm", "--framework", "mermaid",
                 "--code"]) == 0


def test_all_demos_are_schema_valid():
    files = sorted(glob.glob(os.path.join(ROOT, "demos", "*", "org.json")))
    assert len(files) >= 8, "expected the committed demo org files"
    for f in files:
        doc = json.load(open(f, encoding="utf-8"))
        rep = validate_doc(doc)
        assert rep["ok"], (f, rep["errors"])
