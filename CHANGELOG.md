# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Installable Python package with `src/` layout
- `discord-doctor` CLI console entry point
- `pyproject.toml` with modern PEP 517 packaging (hatchling)
- `__main__.py` for `python -m discord_bot_development` invocation
- CLI test suite (`tests/test_cli.py`)
- Public surface verification extended with required-files and entry-point checks
- Pre-commit hooks (ruff, ruff-format)
- Dependabot configuration for pip and github-actions
- Cross-platform CI with wheel-install smoke test

### Changed
- Checker implementation moved from `scripts/discord_doctor.py` to `src/discord_bot_development/doctor.py`
- `scripts/discord_doctor.py` is now a thin backward-compatible wrapper
- Tests now import from the installed package, not from `scripts/`
- README rewritten as landing page for the project
- CONTRIBUTING.md updated with dev dependency install + `discord-doctor` usage
- CI now installs the project, runs lint, tests, public surface check, builds, and smoke-tests the wheel

### Compatibility
- `scripts/discord_doctor.py` remains supported as a wrapper around the package

## [0.1.0] - 2026-09-10

### Added
- Initial release of the Discord Bot Development agent skill.
- `SKILL.md` with detect→classify→design→implement→verify workflow.
- Reference pages covering all major Discord bot development topics.
- `scripts/discord_doctor.py` — deterministic checker with 14 rules.
- Checker fixture tests with positive and negative examples.
- Public surface verification script.
- README, LICENSE, CONTRIBUTING, SECURITY documentation.
- GitHub Actions CI workflow.
