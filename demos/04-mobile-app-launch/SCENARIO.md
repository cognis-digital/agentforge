# Demo 04 — Mobile App Launch Squad

**Where the data came from.** A cross-functional squad shipping v1.0 of a consumer
mobile app to both app stores: PM, iOS, Android, Backend, Mobile QA, Product
Designer, and a Growth Analyst who instruments the funnel. Seven agents — the
largest single-team demo — all reporting to the PM.

**What to expect.** A realistic launch board when synced to PM tooling, and a full
seven-agent export to any framework. The QA agent is a `skeptic` (gates the
release); the designer is a `creative`.

## Run it

```sh
agentforge schema --file demos/04-mobile-app-launch/org.json

# Turn the launch checklist into a Trello board (Backlog/In Progress/Review/Done)
agentforge pm --file demos/04-mobile-app-launch/org.json --platform trello \
  --task "Submit iOS build to TestFlight" \
  --task "Roll out Android internal track" \
  --task "Wire activation + retention analytics" \
  --task "Store listing + screenshots" --format json

# Or a GitHub project board
agentforge pm --file demos/04-mobile-app-launch/org.json --platform github \
  --task "Cut release branch 1.0" --format json

# Run the squad on a launch-readiness review
agentforge run --file demos/04-mobile-app-launch/org.json --team squad \
  --task "Are we ready to submit v1.0? Each role: your go/no-go and your one blocker"

# Export to AutoGen group chat
agentforge export --file demos/04-mobile-app-launch/org.json --framework autogen --code
```

## How to act on it

- **pm** gives you a board where each launch task is a card/issue; the `members`
  list maps each agent to an assignee.
- The **run** "go/no-go" task is a quick way to get every role's launch-readiness
  read in one pass.
