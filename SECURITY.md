# Security Policy

## Reporting Security Issues

If you discover a security vulnerability in this repository, please report it
privately by opening a **security advisory** on GitHub.

**Do not** open public issues for security vulnerabilities.

## What This Is

This repository is an Agent Skill — documentation and a deterministic checker
for Discord bot development. It ships **no bot runtime**, no credentials, and
makes no network calls.

## What This Is NOT

- A Discord bot runtime
- A service that handles tokens or secrets
- Connected to any Discord account

## Verified Clean

The repository contains:
- Documentation (`.md` files)
- Checker script (`scripts/discord_doctor.py`)
- Tests (no live tokens, no network)
- CI workflow

The checker **rejects** hardcoded tokens in source code (rule DB001).

## Scope

Out of scope:
- The actual Discord bot project this skill teaches
- Live bot tokens or credentials
- Third-party bot frameworks beyond documentation references
