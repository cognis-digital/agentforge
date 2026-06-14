"""agentforge — organizations of AI agents, runnable and exportable.

  templates                         list ready-made org templates
  org --template NAME | --file F    show an organization
  agents --template NAME            list agents (role/persona/experience/skills/tools)
  personas                          list personality archetypes
  skills | tools                    the skill / tool registry
  run --template NAME --team KEY --task "..." [--fleet]   run a team on a task
  export --template NAME --framework crewai|autogen|langgraph|openhands|taskweaver|metagpt [--code]
  pm --template NAME --platform github|jira|linear|notion|trello|asana --task "..."
  frameworks                        everything agentforge interoperates with

--format table|json
"""
from __future__ import annotations
import argparse
import json

from . import templates as T, personas, registry, runtime
from .models import Organization, TOOL_NAME, TOOL_VERSION
from .interop import frameworks as fw, pm as pmmod, catalog


def _j(o): print(json.dumps(o, indent=2, default=lambda x: getattr(x, "to_dict", lambda: str(x))()))


def _load_org(a) -> Organization:
    if getattr(a, "file", None):
        return Organization.from_dict(json.load(open(a.file, encoding="utf-8")))
    return T.from_template(a.template)


def cmd_templates(a):
    if a.format == "json": _j(list(T.TEMPLATES)); return 0
    for k in T.TEMPLATES:
        org = T.from_template(k)
        print(f"{k:16} {org.headcount():>2} agents / {len(org.teams)} teams — {org.mission}")
    return 0


def cmd_org(a):
    org = _load_org(a)
    if a.format == "json": _j(org.to_dict()); return 0
    print(f"# {org.name} ({org.headcount()} agents, {len(org.teams)} teams)\n{org.mission}\n")
    for t in org.teams:
        print(f"[{t.key}] {t.name} — {t.mission}  (lead: {t.lead})")
        for m in t.members:
            print(f"    {m.key:14} {m.experience:9} {m.role:26} {m.persona.archetype}")
    return 0


def cmd_agents(a):
    org = _load_org(a)
    rows = [{"key": m.key, "name": m.name, "role": m.role, "experience": m.experience,
             "archetype": m.persona.archetype, "skills": m.skills, "tools": m.tools,
             "reports_to": m.reports_to} for m in org.all_agents()]
    _j(rows); return 0


def cmd_personas(a):
    if a.format == "json": _j(personas.ARCHETYPES); return 0
    for k, v in personas.ARCHETYPES.items():
        print(f"{k:12} {v[1]:24} {v[2]}")
    return 0


def cmd_skills(a): _j(registry.list_skills()); return 0
def cmd_tools(a): _j(registry.list_tools()); return 0


def cmd_run(a):
    org = _load_org(a)
    backend = runtime.FleetBackend() if a.fleet else runtime.LocalMockBackend()
    res = runtime.Runtime(backend).run_team(org, a.team, a.task)
    if a.format == "json": _j(res.to_dict()); return 0
    print(f"# {org.name} / team {a.team} on: {a.task}  (backend: {res.backend})\n")
    for k, v in res.contributions.items():
        print(f"[{k}] {v}\n")
    if res.synthesis:
        print(f"## Synthesis\n{res.synthesis}")
    return 0


def cmd_export(a):
    org = _load_org(a)
    if a.code:
        print(fw.to_code(org, a.framework)); return 0
    _j(fw.export(org, a.framework)); return 0


def cmd_pm(a):
    org = _load_org(a)
    _j(pmmod.sync(org, a.platform, a.task or [])); return 0


def cmd_frameworks(a):
    out = {"agent_frameworks": catalog.all_frameworks(), "pm_suites": catalog.pm_suites(),
           "cognis": catalog.cognis()}
    if a.format == "json": _j(out); return 0
    print("Agent frameworks (export):")
    for f in catalog.all_frameworks():
        print(f"  {f['key']:12} {f['name']:18} {'[export]' if f['export'] else '[map]':9} {f['kind']}")
    print("\nProject-management suites (sync):")
    for p in catalog.pm_suites():
        print(f"  {p['key']:12} {p['name']}")
    print("\nCognis interop:")
    for c in catalog.cognis():
        print(f"  {c['repo']:28} {c['role']}")
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog=TOOL_NAME, description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--version", action="version", version=f"{TOOL_NAME} {TOOL_VERSION}")
    sub = p.add_subparsers(dest="command")

    def add(n, fn, org=False):
        sp = sub.add_parser(n)
        sp.add_argument("--format", choices=["table", "json"], default="table")
        if org:
            sp.add_argument("--template"); sp.add_argument("--file")
        sp.set_defaults(func=fn)
        return sp

    add("templates", cmd_templates)
    add("org", cmd_org, org=True)
    add("agents", cmd_agents, org=True)
    add("personas", cmd_personas)
    add("skills", cmd_skills)
    add("tools", cmd_tools)
    sp = add("run", cmd_run, org=True); sp.add_argument("--team", required=True)
    sp.add_argument("--task", required=True); sp.add_argument("--fleet", action="store_true")
    sp = add("export", cmd_export, org=True); sp.add_argument("--framework", required=True)
    sp.add_argument("--code", action="store_true")
    sp = add("pm", cmd_pm, org=True); sp.add_argument("--platform", required=True)
    sp.add_argument("--task", action="append")
    add("frameworks", cmd_frameworks)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    if not getattr(args, "command", None):
        build_parser().print_help(); return 2
    # default template if an org-taking command got neither
    if hasattr(args, "template") and not args.template and not getattr(args, "file", None):
        args.template = "software_team"
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
