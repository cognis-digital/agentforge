"""Tests for the agentforge enterprise layer: config, policy, audit, hardened runtime."""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentforge import (  # noqa: E402
    from_template, TOOL_VERSION, load_org, save_org, backend_from_env,
    Policy, PolicyEngine, AuditTrail, Runtime, OpenAIBackend, FleetBackend,
    LocalMockBackend, BackendError,
)
from agentforge.cli import main  # noqa: E402


def test_version_bumped():
    assert TOOL_VERSION == "0.2.1"


def test_org_save_load_roundtrip(tmp_path=None):
    org = from_template("jtf_meridian")
    p = os.path.join(tempfile.mkdtemp(), "org.json")
    save_org(org, p)
    back = load_org(p)
    assert back.headcount() == org.headcount()
    assert back.key == org.key


def test_backend_from_env_defaults_mock(monkeypatch=None):
    os.environ.pop("AGENTFORGE_BACKEND", None)
    assert isinstance(backend_from_env(), LocalMockBackend)
    os.environ["AGENTFORGE_BACKEND"] = "openai"
    os.environ["AGENTFORGE_API_KEY"] = "x"
    assert isinstance(backend_from_env(), OpenAIBackend)
    os.environ["AGENTFORGE_BACKEND"] = "fleet"
    assert isinstance(backend_from_env(), FleetBackend)
    os.environ.pop("AGENTFORGE_BACKEND", None)


def test_policy_check_and_validate():
    org = from_template("software_team")
    pol = Policy(denied_tools=["shell"], approval_required=["github"])
    eng = PolicyEngine(pol)
    # an agent using a denied tool is a violation
    rep = eng.validate(org)
    assert any(v["tool"] == "shell" for v in rep["violations"]) == any(
        "shell" in a.tools for a in org.all_agents())
    assert "github" in rep["tools_needing_approval"]
    # role allowlist
    pol2 = Policy(role_tools={"SRE": ["http"]})
    d = PolicyEngine(pol2).check(org.agent("sre"), "shell")
    assert not d.allow


def test_policy_require_reports_to():
    org = from_template("software_team")
    rep = PolicyEngine(Policy(require_reports_to=True)).validate(org)
    # the EM (principal) has no reports_to but isn't exec -> flagged; agents with a
    # manager are fine
    flagged = [v for v in rep["violations"] if v["reason"].startswith("non-exec")]
    assert any(v["agent"] == "em" for v in flagged)


def test_audit_trail():
    org = from_template("research_firm")
    trail = AuditTrail()
    Runtime(LocalMockBackend(), audit=trail).run_team(org, "research", "task")
    s = trail.summary()
    assert s["events"] >= 3
    assert "run_start" in s["by_kind"] and "run_end" in s["by_kind"]
    assert "agent_run" in s["by_kind"]


def test_runtime_usage_and_policy_in_result():
    org = from_template("research_firm")
    rt = Runtime(LocalMockBackend(), policy=PolicyEngine(Policy(max_agent_calls=99)))
    res = rt.run_team(org, "research", "size the market")
    assert res.usage["agent_calls"] >= 1 and res.usage["errors"] == 0
    assert "headcount" in res.policy


def test_openai_backend_raises_on_bad_endpoint():
    b = OpenAIBackend(base_url="http://127.0.0.1:1/v1", api_key="x", retries=0, timeout=2)
    org = from_template("software_team")
    a = org.agent("em")
    try:
        b.run(a, "sys", "task")
        assert False, "should have raised BackendError"
    except BackendError:
        pass


def test_fleet_backend_falls_back():
    # unreachable fleet endpoint -> graceful mock fallback (no raise)
    b = FleetBackend(base_url="http://127.0.0.1:1/v1", retries=0, timeout=2)
    org = from_template("software_team")
    out = b.run(org.agent("em"), "sys", "task")
    assert "offline mock" in out


def test_cli_validate():
    assert main(["validate", "--template", "software_team", "--format", "json"]) == 0
    assert main(["validate", "--template", "software_team", "--require-reports-to",
                 "--approval-required", "github,shell"]) == 0
