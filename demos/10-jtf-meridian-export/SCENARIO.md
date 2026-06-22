# Demo 10 — Export the Cognis JTF MERIDIAN command structure

**Where the data came from.** The built-in `jtf_meridian` template — Cognis
Digital's six-division command structure (BLACKBOOK, NULLBYTE, ATHENA-PRIME,
IRONCLAD, PROMETHEUS, FOUNDRY) plus the ARCHON command element — expressed as an
agentforge org. No file needed; it ships with the tool. This demo is about the
**export and schema** surface rather than a custom org.

**What to expect.** Seven teams (a `command` team + six divisions). It validates
against the schema, exports to every supported framework, and renders as a Mermaid
org chart.

## Run it

```sh
# The whole command structure as agents
agentforge org --template jtf_meridian

# Validate the built-in template against the published contract (expect ok:true)
agentforge schema --template jtf_meridian

# Emit the JSON Schema itself — drop it in CI or reference it from your org files
agentforge schema --format json > org.schema.json

# Export to each framework
agentforge export --template jtf_meridian --framework crewai --format json
agentforge export --template jtf_meridian --framework autogen --code
agentforge export --template jtf_meridian --framework metagpt --format json

# Render the command structure as a Mermaid diagram (paste into any Markdown)
agentforge export --template jtf_meridian --framework mermaid --code
```

## How to act on it

- `agentforge schema --format json` gives you a standards-compliant **JSON Schema
  (Draft 2020-12)**. Add `"$schema": "...org.schema.json"` to your own org files for
  editor autocomplete + linting, and run `agentforge schema --file your_org.json` in
  CI to gate changes.
- The **mermaid** export is the fastest way to put any org — including this one — in
  front of humans as a diagram.

## Make your own

Every demo in this folder is a plain `org.json`. Copy one, edit the agents
(`key`, `role`, `persona.archetype`, `experience`, `skills`, `tools`,
`reports_to`), then validate and run:

```sh
agentforge schema --file demos/01-incident-response/org.json   # must be ok:true
agentforge run --file your_org.json --team <team-key> --task "..."
```

`agentforge skills` and `agentforge tools` list the valid skill/tool keys;
`agentforge personas` lists the archetypes.
