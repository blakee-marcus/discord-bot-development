# Discord Bot Development

[![CI](https://github.com/blakee-marcus/discord-bot-development/actions/workflows/ci.yml/badge.svg)](https://github.com/blakee-marcus/discord-bot-development/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Production-oriented Discord engineering guidance plus a deterministic auditor for common Discord bot mistakes.

**Author:** Blake Marcus
**License:** MIT

## What It Is

This repository has two public surfaces:

1. **Agent skill** — `SKILL.md` + `references/` teach Discord platform fundamentals and stable patterns for discord.js 14.27 and discord.py 2.7.
2. **Deterministic developer tool** — `discord-doctor` CLI audits bot code for the mistakes LLMs repeatedly make: hardcoded tokens, missing intents, registration inside `ready`, unbounded collectors, legacy APIs.

## Features

- **14 deterministic rules** — high-confidence static analysis for JS/TS/Python Discord code
- **Machine-readable output** — `--json` for CI consumption
- **Agent skill** — source-backed references for building production-quality bots
- **Cross-platform CI** — tested on Ubuntu + Windows, Python 3.10–3.13

## Installation

### As a tool

```bash
git clone https://github.com/blakee-marcus/discord-bot-development.git
cd discord-bot-development
python -m pip install -e .
discord-doctor /path/to/your/bot
```

### As an agent skill

Point your agent at `SKILL.md`. The skill entry point, references, and plugin manifest are all at the repository root.

## Quick Start

```bash
# Check a bot directory
discord-doctor ./my-bot

# JSON output for CI
discord-doctor ./my-bot --json > findings.json

# List all rule IDs
discord-doctor --rules

# Check version
discord-doctor --version
```

## Discord Doctor

The `discord-doctor` CLI is a deterministic static-analysis tool for Discord bot code.

### Exit codes

| Code | Meaning |
|------|---------|
| 0 | Scan completed, no FAIL findings |
| 1 | Scan completed, FAIL findings present |
| 2 | Invalid invocation / target not found |

### Rules

| ID | Severity | Description |
|----|----------|-------------|
| DB001 | FAIL | Hardcoded bot token detected |
| DB002 | FAIL | Legacy discord.js v12/v13 API usage |
| DB003 | FAIL | Command registration inside ready/on_ready handler |
| DB004 | WARN | Client/Bot constructed without explicit intents |
| DB005 | WARN | Collector/modal await without timeout |
| DB006 | FAIL | Deprecated response method |
| DB007 | WARN | Deprecated DM option or method |
| DB008 | FAIL | Python file/package shadows 'discord' |
| DB009 | FAIL | time.sleep() used in async context |
| DB010 | WARN | tree.sync() called from on_ready |
| DB011 | FAIL | Literal token passed to run/start/login |
| DB012 | WARN | Bot() without intents parameter |
| DB013 | WARN | Multiple response calls without is_done() guard |
| DB014 | WARN | Response call after defer without followup |

## Agent Skill

The `SKILL.md` and `references/` directory form a complete agent skill for Discord bot development:

- **detect** → framework, version, intents, permissions, scope
- **classify** → new bot / add feature / migrate / audit / debug
- **design** → interaction type, registration path, intent set, permission bitmap
- **implement** → follow framework reference, REST-only registration, ACK/defer within 3s
- **verify** → run the checker, lint, typecheck, test matrix

## Supported Frameworks

| Framework | Version | Runtime |
|-----------|---------|---------|
| discord.js | 14.27.0 | Node >=18 (package); >=22.12.0 recommended |
| discord.py | 2.7.1 | Python >=3.8 |

## Project Structure

```text
discord-bot-development/
├── .claude-plugin/          # Plugin manifest
├── .github/                 # CI workflow + dependabot
├── references/              # Canonical reference pages
├── scripts/
│   ├── discord_doctor.py    # Backward-compatible wrapper
│   └── verify_public_surface.py
├── src/
│   └── discord_bot_development/
│       ├── __init__.py      # Public API exports
│       ├── __main__.py      # Module invocation
│       └── doctor.py        # Checker implementation
├── tests/
│   ├── fixtures/            # Positive + negative test fixtures
│   ├── test_checker.py      # Library API tests
│   └── test_cli.py          # CLI surface tests
├── pyproject.toml           # Package metadata + build config
├── SKILL.md                 # Agent skill entry point
└── skills.sh.json           # Skill loader manifest
```

## Development

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
ruff check .
python -m build
```

## Security

See [SECURITY.md](SECURITY.md). The checker rejects hardcoded tokens (DB001). The repository ships no bot runtime, no credentials, and makes no network calls.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
