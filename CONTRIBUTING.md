# Contributing to Discord Bot Development

Thank you for your interest in contributing! This repository is an Agent Skill
that teaches production-quality Discord bot development.

## How to Contribute

### Reporting Issues

If you find errors in the documentation, checker rules, or examples:

1. Check if the issue already exists.
2. Open a new issue with:
   - A clear description
   - The file/line affected
   - The correct information with source URL

### Submitting Changes

1. Fork the repository.
2. Create a feature branch (`git checkout -b fix/your-fix`).
3. Make your changes.
4. Run the test suite: `pytest tests/`
5. Run the checker on fixtures: `python scripts/discord_doctor.py tests/fixtures/`
6. Commit with a clear message.
7. Push and open a pull request.

### Documentation Style

- **Cite sources**: Every implementation-sensitive fact should cite the official Discord URL.
- **No duplication**: Each topic has exactly one canonical owner reference file.
- **Preserve contradictions**: If docs conflict, note both sides; don't silently resolve.
- **Drift-sensitive**: Version numbers, rate limits, thresholds — label with checked-on date.

### Code Style

- Python: PEP 8, type hints where helpful.
- JavaScript/TypeScript: Standard JS style.
- Tests: pytest for Python, Jest/Vitest for JS (if applicable).

## Code of Conduct

Be respectful and constructive. This is a technical documentation project.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
