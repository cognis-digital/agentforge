# Demo 08 — Customer Support Escalation Pod

**Where the data came from.** The pod that handles escalated enterprise support
tickets: a Support Manager, a Tier-2 Engineer (reproduce + resolve), a Tier-3 / Eng
Liaison (patch root causes), and a Knowledge Base Curator (turns every resolution
into a reusable article). Four agents — the smallest, tightest demo — one `pod` team.

**What to expect.** A clean four-agent org with a full chain of command. Good for
showing the **run → synthesis** loop: each tier contributes, and the lead
(Support Manager) synthesizes one customer-facing answer.

## Run it

```sh
agentforge schema --file demos/08-customer-support-escalation/org.json

# Run the pod on an escalated ticket — note the lead's synthesis at the end
agentforge run --file demos/08-customer-support-escalation/org.json --team pod \
  --task "Enterprise customer: webhooks stopped firing after their SSO migration. Triage and propose a fix."

# JSON form, so you can see usage metering (agent_calls / errors) and the synthesis
agentforge run --file demos/08-customer-support-escalation/org.json --team pod \
  --task "SLA-breaching ticket: data export endpoint returns 500 for one tenant" --format json

# Sync the follow-up work to Asana
agentforge pm --file demos/08-customer-support-escalation/org.json --platform asana \
  --task "Root-cause the webhook regression" --task "Publish KB: SSO + webhooks" --format json
```

## How to act on it

- The **synthesis** field is the Support Manager folding Tier-2/Tier-3/KB input into
  one decision — that's the artifact you'd actually send the customer.
- The JSON `usage` block (`agent_calls`, `errors`) is your cost/limit signal when
  running against a real backend.
