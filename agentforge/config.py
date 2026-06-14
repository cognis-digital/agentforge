"""
Configuration & persistence — load/save organizations and configure the model
backend from the environment. Enterprise deployments keep org definitions in
version control (JSON/YAML) and point the runtime at their own LLM gateway via
env vars, so nothing is hard-coded.

Env vars (all optional):
  AGENTFORGE_BACKEND      "openai" | "fleet" | "mock"   (default: mock)
  AGENTFORGE_BASE_URL     OpenAI-compatible base url (e.g. https://api.openai.com/v1
                          or http://127.0.0.1:8080/v1 for edgemesh)
  AGENTFORGE_API_KEY      bearer token (read from env / secret store, never code)
  AGENTFORGE_MODEL        default model id when an agent's model is "auto"
"""
from __future__ import annotations
import json
import os

from .models import Organization


def load_org(path: str) -> Organization:
    """Load an org from .json or .yaml/.yml (YAML needs PyYAML; JSON is dependency-free)."""
    text = open(path, encoding="utf-8").read()
    if path.lower().endswith((".yaml", ".yml")):
        try:
            import yaml  # optional
            data = yaml.safe_load(text)
        except ImportError as e:
            raise RuntimeError("PyYAML not installed; use JSON or `pip install pyyaml`") from e
    else:
        data = json.loads(text)
    return Organization.from_dict(data)


def save_org(org: Organization, path: str) -> None:
    data = org.to_dict()
    if path.lower().endswith((".yaml", ".yml")):
        import yaml
        open(path, "w", encoding="utf-8").write(yaml.safe_dump(data, sort_keys=False))
    else:
        json.dump(data, open(path, "w", encoding="utf-8"), indent=2)


def backend_from_env():
    """Construct a backend from env vars. Defaults to the offline mock so nothing
    surprises a fresh install."""
    from .runtime import LocalMockBackend, OpenAIBackend, FleetBackend
    kind = os.environ.get("AGENTFORGE_BACKEND", "mock").lower()
    if kind == "mock":
        return LocalMockBackend()
    base = os.environ.get("AGENTFORGE_BASE_URL")
    key = os.environ.get("AGENTFORGE_API_KEY", "local")
    model = os.environ.get("AGENTFORGE_MODEL", "default")
    if kind == "fleet":
        return FleetBackend(base_url=base or "http://127.0.0.1:8080/v1",
                            api_key=key, default_model=model)
    return OpenAIBackend(base_url=base or "https://api.openai.com/v1",
                         api_key=key, default_model=model)
