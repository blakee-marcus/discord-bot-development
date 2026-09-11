#!/usr/bin/env python3
"""verify_public_surface.py — public-surface CI gate."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent


# Patterns that indicate hardcoded credentials
TOKEN_PATTERNS = [
    # Standard Discord token format: base64.base64.base64
    re.compile(r'["\'][\w-]{20,}\.[\w-]+\.[\w-]+["\']'),
    # Bot token prefix
    re.compile(r'["\'][A-Za-z0-9_-]{24,}\.[A-Za-z0-9_-]{6,}\.[A-Za-z0-9_-]{27,}["\']'),
]

# Patterns for source manifests / credentials in examples
ENV_PATTERNS = [
    re.compile(r'TOKEN\s*=\s*["\'][^"\']{20,}["\']'),
    re.compile(r'CLIENT_SECRET\s*=\s*["\'][^"\']{20,}["\']'),
]

SKILL_FRONTMATTER_KEYS = {"name", "version", "description", "author", "license"}

SKILL_REQUIRED_FILES = [
    "references/application-setup.md",
    "references/interactions-and-commands.md",
    "references/gateway-and-intents.md",
    "references/permissions-and-oauth2.md",
    "references/rate-limits.md",
    "references/security-and-policy.md",
    "references/sharding-and-operations.md",
    "references/testing-and-deployment.md",
    "references/discord-js.md",
    "references/discord-py.md",
    "references/official-sources.md",
]


def verify_no_hardcoded_tokens() -> list[str]:
    """Scan repo for hardcoded tokens in non-fixture files."""
    issues: list[str] = []

    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in (".py", ".js", ".ts", ".md", ".json"):
            continue
        if ".git" in path.parts:
            continue

        # Skip broken fixtures (intentionally contain bad patterns)
        parts = path.parts
        if "fixtures" in parts and any("broken" in p for p in parts):
            continue

        if "node_modules" in path.parts:
            continue

        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        for i, line in enumerate(content.splitlines(), 1):
            for pattern in TOKEN_PATTERNS:
                if pattern.search(line):
                    issues.append(f"  {path.relative_to(REPO_ROOT)}:{i}")
                    break

    return issues


def verify_skill_frontmatter() -> list[str]:
    """Verify SKILL.md has required frontmatter."""
    skill_path = REPO_ROOT / "SKILL.md"
    if not skill_path.exists():
        return ["SKILL.md missing"]

    try:
        content = skill_path.read_text(encoding="utf-8")
    except OSError as e:
        return [f"Cannot read SKILL.md: {e}"]

    if not content.startswith("---"):
        return ["SKILL.md missing frontmatter"]

    # Extract frontmatter
    end = content.find("---", 3)
    if end == -1:
        return ["SKILL.md frontmatter not closed"]

    fm_text = content[3:end].strip()
    keys_found = set()
    for line in fm_text.splitlines():
        if ":" in line:
            key = line.split(":", 1)[0].strip()
            keys_found.add(key)

    missing = SKILL_FRONTMATTER_KEYS - keys_found
    if missing:
        return [f"SKILL.md frontmatter missing keys: {', '.join(sorted(missing))}"]

    return []


def verify_plugin_manifest() -> list[str]:
    """Verify plugin.json is valid."""
    plugin_path = REPO_ROOT / ".claude-plugin" / "plugin.json"
    if not plugin_path.exists():
        return [".claude-plugin/plugin.json missing"]

    try:
        data = json.loads(plugin_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return [f"plugin.json invalid: {e}"]

    required = {"name", "description", "version"}
    missing = required - set(data.keys())
    if missing:
        return [f"plugin.json missing keys: {', '.join(sorted(missing))}"]

    return []


def verify_references_exist() -> list[str]:
    """Verify all required reference files exist."""
    missing = []
    for ref in SKILL_REQUIRED_FILES:
        if not (REPO_ROOT / ref).exists():
            missing.append(ref)
    return missing


def main() -> int:
    all_issues: dict[str, list[str]] = {}

    issues = verify_no_hardcoded_tokens()
    if issues:
        all_issues["hardcoded_tokens"] = issues

    issues = verify_skill_frontmatter()
    if issues:
        all_issues["skill_frontmatter"] = issues

    issues = verify_plugin_manifest()
    if issues:
        all_issues["plugin_manifest"] = issues

    issues = verify_references_exist()
    if issues:
        all_issues["missing_references"] = issues

    if all_issues:
        print("FAIL: Issues found")
        for check, issues in all_issues.items():
            print(f"\n{check}:")
            for issue in issues:
                print(f"  {issue}")
        return 1

    print("PASS: No hardcoded tokens")
    print("PASS: SKILL.md frontmatter")
    print("PASS: Plugin manifest")
    print("PASS: References exist")
    print("\nAll checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
