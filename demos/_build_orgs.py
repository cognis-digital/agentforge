"""Builds the org.json for each demo via the agentforge API so every file is
guaranteed valid against the published schema. Run from the repo root:

    PYTHONPATH=. python demos/_build_orgs.py

This is a maintenance helper; the generated org.json files are committed so the
demos work without running it.
"""
from __future__ import annotations
import json
import os

from agentforge.models import Organization, Team, Agent
from agentforge.personas import make_persona

HERE = os.path.dirname(os.path.abspath(__file__))


def A(key, name, role, arch, exp, skills, tools, goals="", reports_to=None, model="auto"):
    return Agent(key=key, name=name, role=role, persona=make_persona(arch),
                 experience=exp, skills=skills, tools=tools, goals=goals,
                 reports_to=reports_to, model=model)


def write(path, org: Organization):
    out = os.path.join(HERE, path, "org.json")
    json.dump(org.to_dict(), open(out, "w", encoding="utf-8"), indent=2)
    print("wrote", out, "-", org.headcount(), "agents")


# 01 — Security incident-response cell
write("01-incident-response", Organization(
    "incident_response", "Sev-1 Incident Response Cell",
    "Contain, eradicate, and recover from a security incident; produce a defensible timeline.",
    teams=[Team("ir", "Incident Response", "Run the incident bridge to resolution.", lead="ic", members=[
        A("ic", "Imani", "Incident Commander", "operator", "principal",
          ["planning", "project_mgmt"], ["github", "http"],
          "Own the bridge; drive containment and comms cadence."),
        A("forensics", "Felix", "Forensics Lead", "analyst", "senior",
          ["security_review", "data_analysis"], ["shell", "code_exec", "rag"],
          "Establish a defensible timeline from logs and artifacts.", reports_to="ic"),
        A("threat", "Tariq", "Threat Hunter", "skeptic", "senior",
          ["security_review", "red_teaming"], ["chain_analytics", "http"],
          "Find lateral movement and persistence; assume breach.", reports_to="ic"),
        A("sre", "Sana", "SRE on-call", "operator", "senior",
          ["ops"], ["shell", "http"], "Isolate hosts, rotate creds, restore service.", reports_to="ic"),
        A("comms", "Cleo", "Comms / Legal liaison", "diplomat", "staff",
          ["writing", "compliance"], [], "Draft customer + regulator notifications.", reports_to="ic"),
    ])]))

# 02 — SOC 2 audit-readiness program
write("02-soc2-audit-readiness", Organization(
    "soc2_readiness", "SOC 2 Type II Readiness Program",
    "Get the org audit-ready: map controls, gather evidence, remediate gaps before the auditor arrives.",
    teams=[Team("grc", "GRC", "Stand up SOC 2 controls and evidence.", lead="grc_lead", members=[
        A("grc_lead", "Greta", "GRC Program Lead", "strategist", "principal",
          ["compliance", "planning", "project_mgmt"], ["github"],
          "Own the control matrix and the auditor relationship."),
        A("controls", "Cory", "Controls Analyst", "analyst", "senior",
          ["compliance", "data_analysis"], ["rag", "http"],
          "Map each Trust Services Criterion to an implemented control.", reports_to="grc_lead"),
        A("evidence", "Esme", "Evidence Collector", "operator", "mid",
          ["compliance", "ops"], ["github", "shell", "http"],
          "Automate evidence pulls (access reviews, change logs, backups).", reports_to="grc_lead"),
        A("sec", "Sven", "Security Engineer", "skeptic", "senior",
          ["security_review", "red_teaming"], ["code_exec", "shell"],
          "Validate that controls actually hold under test.", reports_to="grc_lead"),
        A("writer", "Wendy", "Policy Writer", "diplomat", "mid",
          ["writing", "compliance"], ["rag"],
          "Write the policies and the system description.", reports_to="grc_lead"),
    ])]))

# 03 — AI research lab
write("03-ai-research-lab", Organization(
    "ai_research_lab", "Applied AI Research Lab",
    "Turn open questions into reproducible findings and shippable prototypes.",
    teams=[
        Team("research", "Research", "Frame, run, and write up experiments.", lead="pi", members=[
            A("pi", "Priya", "Principal Investigator", "strategist", "principal",
              ["planning", "research", "writing"], ["rag", "web_search"],
              "Set the research agenda; defend conclusions."),
            A("re1", "Ravi", "Research Scientist", "researcher", "senior",
              ["research", "data_analysis"], ["code_exec", "rag", "web_search"],
              "Design and run experiments; report honestly.", reports_to="pi"),
            A("re2", "Robin", "Research Engineer", "builder", "mid",
              ["coding", "architecture"], ["code_exec", "github"],
              "Build the eval harness and reproduce baselines.", reports_to="pi"),
            A("critic", "Cass", "Reproducibility Skeptic", "skeptic", "staff",
              ["red_teaming", "data_analysis"], ["code_exec"],
              "Try to break every claimed result before it ships.", reports_to="pi"),
        ]),
        Team("ml_infra", "ML Infra", "Keep training and eval reproducible at scale.",
             lead="infra_lead", members=[
            A("infra_lead", "Iris", "ML Infra Lead", "operator", "staff",
              ["ops", "architecture"], ["shell", "hardware_plan", "code_exec"],
              "Own clusters, data versioning, and run reproducibility."),
            A("data", "Dane", "Data Engineer", "builder", "senior",
              ["data_analysis", "coding"], ["sql", "code_exec"],
              "Curate and version datasets.", reports_to="infra_lead"),
        ]),
    ]))

# 04 — Mobile app launch
write("04-mobile-app-launch", Organization(
    "mobile_launch", "Mobile App Launch Squad",
    "Ship v1.0 of a consumer mobile app to both stores and instrument the funnel.",
    teams=[Team("squad", "Launch Squad", "Design, build, test, and release v1.0.", lead="pm", members=[
        A("pm", "Pia", "Product Manager", "strategist", "principal",
          ["planning", "project_mgmt", "writing"], ["github"],
          "Own scope, store listings, and the launch checklist."),
        A("ios", "Ian", "iOS Engineer", "builder", "senior",
          ["coding", "design"], ["code_exec", "github"], reports_to="pm"),
        A("android", "Ada", "Android Engineer", "builder", "senior",
          ["coding", "design"], ["code_exec", "github"], reports_to="pm"),
        A("backend", "Bex", "Backend Engineer", "builder", "mid",
          ["coding", "architecture"], ["code_exec", "github", "sql", "http"], reports_to="pm"),
        A("qa", "Quill", "Mobile QA", "skeptic", "senior",
          ["code_review", "red_teaming"], ["code_exec"],
          "Test on real devices; gate the release.", reports_to="pm"),
        A("designer", "Dot", "Product Designer", "creative", "senior",
          ["design", "writing"], [], reports_to="pm"),
        A("growth", "Gus", "Growth Analyst", "analyst", "mid",
          ["data_analysis"], ["sql", "http"],
          "Instrument activation + retention; read the funnel.", reports_to="pm"),
    ])]))

# 05 — M&A due-diligence deal team
write("05-due-diligence-deal-team", Organization(
    "dd_deal_team", "Acquisition Due-Diligence Deal Team",
    "Diligence a target company across financial, technical, legal, and security dimensions; recommend go/no-go.",
    teams=[Team("deal", "Deal Team", "Produce the diligence memo and the recommendation.",
                lead="partner", members=[
        A("partner", "Petra", "Deal Partner", "strategist", "exec",
          ["planning", "writing"], ["rag"],
          "Own the thesis and the final recommendation."),
        A("fin", "Farouk", "Financial Analyst", "analyst", "senior",
          ["data_analysis"], ["sql", "code_exec", "rag"],
          "Validate the financial model and quality of earnings.", reports_to="partner"),
        A("tech", "Tessa", "Technical DD Lead", "researcher", "staff",
          ["architecture", "code_review", "research"], ["github", "code_exec"],
          "Assess the codebase, architecture, and tech debt.", reports_to="partner"),
        A("sec", "Soren", "Security DD", "skeptic", "senior",
          ["security_review", "red_teaming"], ["chain_analytics", "http", "sanctions_screen"],
          "Find security and counterparty risk; KYC/sanctions screen.", reports_to="partner"),
        A("legal", "Lola", "Legal / Compliance", "operator", "senior",
          ["compliance", "writing"], ["rag"],
          "Surface contract, IP, and regulatory exposure.", reports_to="partner"),
    ])]))

# 06 — MLOps platform team
write("06-mlops-platform-team", Organization(
    "mlops_platform", "MLOps Platform Team",
    "Run the internal ML platform: serving, pipelines, observability, and on-call.",
    teams=[Team("platform", "Platform", "Keep models shipping and serving reliably.",
                lead="lead", members=[
        A("lead", "Lin", "Platform Lead", "strategist", "principal",
          ["planning", "architecture", "ops"], ["github", "hardware_plan"],
          "Own platform roadmap and reliability SLOs."),
        A("serving", "Sol", "Serving Engineer", "builder", "senior",
          ["coding", "ops", "architecture"], ["code_exec", "http", "shell"],
          "Own low-latency model serving and autoscaling.", reports_to="lead"),
        A("pipelines", "Pace", "Pipelines Engineer", "builder", "mid",
          ["coding", "data_analysis"], ["code_exec", "sql", "github"],
          "Own training/eval pipelines and data lineage.", reports_to="lead"),
        A("obs", "Oda", "Observability Engineer", "operator", "senior",
          ["ops", "data_analysis"], ["http", "shell", "sql"],
          "Own metrics, drift detection, and alerting.", reports_to="lead"),
        A("sec", "Sage", "ML Security Reviewer", "skeptic", "staff",
          ["security_review", "red_teaming"], ["code_exec"],
          "Review models and prompts for abuse and exfil risk.", reports_to="lead"),
    ])]))

# 07 — Grant proposal writing team
write("07-grant-proposal-writers", Organization(
    "grant_writers", "Federal Grant Proposal Team",
    "Win a competitive federal R&D grant: shape the narrative, the budget, and the compliance package.",
    teams=[Team("proposal", "Proposal", "Assemble a compliant, compelling proposal by the deadline.",
                lead="pi", members=[
        A("pi", "Pearl", "Principal Investigator", "strategist", "principal",
          ["planning", "research", "writing"], ["rag", "web_search"],
          "Own the scientific narrative and the win theme."),
        A("writer", "Wes", "Lead Proposal Writer", "diplomat", "senior",
          ["writing"], ["rag"],
          "Turn technical content into a graded, on-spec narrative.", reports_to="pi"),
        A("budget", "Bibi", "Budget Analyst", "analyst", "senior",
          ["data_analysis", "compliance"], ["sql", "code_exec"],
          "Build a defensible, allowable budget.", reports_to="pi"),
        A("compliance", "Cam", "Compliance Reviewer", "operator", "staff",
          ["compliance"], ["rag"],
          "Check every solicitation requirement is met.", reports_to="pi"),
        A("red", "Reese", "Red Team Reviewer", "skeptic", "staff",
          ["red_teaming", "writing"], [],
          "Grade the draft like the review panel will.", reports_to="pi"),
    ])]))

# 08 — Customer support escalation pod
write("08-customer-support-escalation", Organization(
    "support_escalation", "Customer Support Escalation Pod",
    "Resolve escalated enterprise tickets fast and feed fixes back to engineering.",
    teams=[Team("pod", "Escalation Pod", "Drive escalated tickets to resolution.",
                lead="mgr", members=[
        A("mgr", "Mira", "Support Manager", "diplomat", "principal",
          ["planning", "project_mgmt", "writing"], ["github", "http"],
          "Own SLA, customer comms, and escalation triage."),
        A("tier2", "Teo", "Tier-2 Engineer", "operator", "senior",
          ["code_review", "ops"], ["shell", "http", "sql"],
          "Reproduce and resolve technical escalations.", reports_to="mgr"),
        A("tier3", "Toni", "Tier-3 / Eng Liaison", "builder", "staff",
          ["coding", "architecture"], ["code_exec", "github", "sql"],
          "Patch root causes and file durable fixes.", reports_to="mgr"),
        A("kb", "Kai", "Knowledge Base Curator", "researcher", "mid",
          ["writing", "research"], ["rag"],
          "Turn each resolution into a reusable KB article.", reports_to="mgr"),
    ])]))

# 09 — Energy trading research desk (grounded in user's domain)
write("09-energy-trading-desk", Organization(
    "energy_desk", "Energy-Sector Trading Research Desk",
    "Produce decision-ready, sourced theses on energy and power-infrastructure equities; manage risk.",
    teams=[Team("desk", "Research Desk", "Generate and pressure-test trade theses.",
                lead="head", members=[
        A("head", "Hana", "Head of Research", "strategist", "principal",
          ["planning", "research", "writing"], ["rag", "web_search"],
          "Set the thematic agenda; own the desk's calls."),
        A("macro", "Mateo", "Macro / Energy Analyst", "researcher", "senior",
          ["research", "data_analysis"], ["web_search", "rag"],
          "Cover supply/demand, policy, and the energy cycle.", reports_to="head"),
        A("quant", "Qi", "Quant Analyst", "analyst", "senior",
          ["data_analysis"], ["sql", "code_exec"],
          "Backtest signals; quantify edge and drawdown.", reports_to="head"),
        A("risk", "Rhea", "Risk Manager", "skeptic", "staff",
          ["red_teaming", "data_analysis"], ["code_exec"],
          "Refute every thesis; cap downside and concentration.", reports_to="head"),
        A("writer", "Wren", "Desk Writer", "diplomat", "mid",
          ["writing"], ["rag"],
          "Publish the morning note and trade memos.", reports_to="head"),
    ])]))

print("done")
