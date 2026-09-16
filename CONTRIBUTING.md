# Contributing to Discord Bot Development

Thank you for your interest in contributing! This repository is both an agent skill and a deterministic Discord bot code auditor.

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
4. Install dev dependencies: `python -m pip install -e ".[dev]"`
5. Run the test suite: `pytest`
6. Run the linter: `ruff check .`
7. Run the checker on fixtures: `discord-doctor tests/fixtures/`
8. Commit with a clear message.
9. Push and open a pull request.

### Documentation Style

- **Cite sources**: Every implementation-sensitive fact should cite the official Discord URL.
- **No duplication**: Each topic has exactly one canonical owner reference file.
- **Preserve contradictions**: If docs conflict, note both sides; don't silently resolve.
- **Drift-sensitive**: Version numbers, rate limits, thresholds — label with checked-on date.

### Code Style

- Python: PEP 8, type hints where helpful, line length 100.
- JavaScript/TypeScript: Standard JS style.
- Tests: pytest for Python, Jest/Vitest for JS (if applicable).

### Development Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
pytest
ruff check .
```

## Code of Conduct

Be respectful and constructive. This is a technical documentation project.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
