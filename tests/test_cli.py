"""Tests for the CLI surface of discord-bot-development."""

import json
import subprocess
import sys
from pathlib import Path

from discord_bot_development.doctor import CheckResult, check_path

FIXTURES = Path(__file__).parent / "fixtures"


def run(*args: str) -> subprocess.CompletedProcess:
    """Run a CLI command in a subprocess, returning the completed process."""
    return subprocess.run(
        [sys.executable, "-m", "discord_bot_development", *args],
        capture_output=True,
        text=True,
    )


def test_help_exits_zero() -> None:
    """--help should exit 0 and print usage."""
    result = run("--help")
    assert result.returncode == 0
    assert "usage" in result.stdout.lower() or "discord" in result.stdout.lower()


def test_rules_exits_zero() -> None:
    """--rules should exit 0 and list rule IDs."""
    result = run("--rules")
    assert result.returncode == 0
    assert "DB001" in result.stdout
    assert "DB011" in result.stdout


def test_clean_fixture_exits_zero() -> None:
    """A clean fixture should produce exit code 0."""
    result = run(str(FIXTURES / "js_ok" / "clean_bot.js"))
    assert result.returncode == 0, result.stdout


def test_broken_fixture_exits_nonzero() -> None:
    """A broken fixture should produce exit code 1."""
    result = run(str(FIXTURES / "js_broken" / "hardcoded_token.js"))
    assert result.returncode == 1, result.stdout


def test_missing_path_exits_nonzero() -> None:
    """A missing path should produce a non-zero exit code."""
    result = run("/nonexistent/path")
    assert result.returncode != 0


def test_json_output_is_valid() -> None:
    """--json should return valid JSON with expected schema."""
    result = run(str(FIXTURES / "js_broken" / "hardcoded_token.js"), "--json")
    assert result.returncode == 1
    data = json.loads(result.stdout)
    assert "passed" in data
    assert "fail_count" in data
    assert "warn_count" in data
    assert "files_checked" in data
    assert "findings" in data
    assert isinstance(data["findings"], list)
    assert data["passed"] is False
    assert data["fail_count"] > 0


def test_module_and_script_invocation_equivalent() -> None:
    """Module invocation and the compatibility script produce equivalent results."""
    # Direct API
    result_direct = CheckResult()
    check_path(FIXTURES / "js_broken" / "hardcoded_token.js", result_direct)

    # CLI module invocation
    cli_result = run(str(FIXTURES / "js_broken" / "hardcoded_token.js"), "--json")
    cli_data = json.loads(cli_result.stdout)

    assert result_direct.fail_count == cli_data["fail_count"]
    assert result_direct.passed == cli_data["passed"]


def test_clean_fixture_json_passed_true() -> None:
    """A clean fixture should have passed=true in JSON."""
    result = run(str(FIXTURES / "js_ok" / "clean_bot.js"), "--json")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["passed"] is True
    assert data["fail_count"] == 0
