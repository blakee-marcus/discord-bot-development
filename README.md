# Discord Bot Development — Agent Skill

A source-backed agent skill for building **production-quality Discord bots**.
It teaches Discord platform fundamentals first, then provides stable
playbooks for discord.js and discord.py.

**Author:** Blake Marcus, Hermes Agent
**License:** MIT
**Version:** 0.1.0

## Install

```bash
git clone https://github.com/blakee-marcus/discord-bot-development.git
```

This repository is documentation + a deterministic checker. It ships no bot
runtime. To use it as a Hermes Agent skill, point Hermes at the `SKILL.md`.

## What's Inside

- `SKILL.md` — the skill entry point with a detect→classify→design→implement→verify workflow
- `references/` — canonical, non-duplicated reference pages for each topic
- `scripts/discord_doctor.py` — deterministic checker (PASS/WARN/FAIL)
- `tests/` — checker fixtures and public-surface verification

## Usage

```bash
# Run the checker
python scripts/discord_doctor.py <path-to-bot>

# JSON output
python scripts/discord_doctor.py <path-to-bot> --json

# List rules
python scripts/discord_doctor.py <path-to-bot> --rules

# Run tests
pytest tests/
```

## Why

LLMs repeatedly make the same mistakes when generating Discord bots: hardcoded
tokens, missing intents, registration inside `ready`, unbounded collectors,
legacy APIs. This skill teaches the current stable patterns and audits code
for the known-failure modes.

## Coverage

| Topic | Reference |
|-------|-----------|
| Application setup | `references/application-setup.md` |
| Interactions & commands | `references/interactions-and-commands.md` |
| Gateway & intents | `references/gateway-and-intents.md` |
| Permissions & OAuth2 | `references/permissions-and-oauth2.md` |
| Rate limits | `references/rate-limits.md` |
| Security & policy | `references/security-and-policy.md` |
| Sharding & operations | `references/sharding-and-operations.md` |
| Testing & deployment | `references/testing-and-deployment.md` |
| discord.js 14.27 | `references/discord-js.md` |
| discord.py 2.7 | `references/discord-py.md` |
| Official sources | `references/official-sources.md` |

## Verified Runtime Claims

This skill makes the following **verified** runtime compatibility claims:

- discord.js 14.27.0 — stable, Node >=18 (package) / >=22.12.0 (guide)
- discord.py 2.7.1 — stable, Python >=3.8

These are **snapshots** and drift-sensitive. Always check current versions.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

See [SECURITY.md](SECURITY.md).

## License

MIT — see [LICENSE](LICENSE).
