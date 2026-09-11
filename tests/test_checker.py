"""
Test fixtures for the discord-bot-development checker.

Each fixture tests one or more rules with positive (should trigger) and
negative (should not trigger) examples.
"""

import sys
from pathlib import Path

# Add scripts to path BEFORE importing discord_doctor
# From tests/test_checker.py, scripts/ is at ../scripts
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from discord_doctor import (
    CheckResult,
    check_path,
)


def test_clean_js_file_passes() -> None:
    """A clean JS file should produce no findings."""
    fixture = Path(__file__).parent / "fixtures" / "js_ok" / "clean_bot.js"
    result = CheckResult()
    check_path(fixture, result)
    assert result.passed, f"Expected PASS, got: {[f.rule_id for f in result.findings]}"


def test_hardcoded_token_js_fails() -> None:
    """Hardcoded token in JS should trigger DB001."""
    fixture = Path(__file__).parent / "fixtures" / "js_broken" / "hardcoded_token.js"
    result = CheckResult()
    check_path(fixture, result)
    assert not result.passed
    assert any(f.rule_id == "DB001" for f in result.findings), "Expected DB001"


def test_legacy_discord_js_api_fails() -> None:
    """Legacy discord.js APIs should trigger DB002."""
    fixture = Path(__file__).parent / "fixtures" / "js_broken" / "legacy_api.js"
    result = CheckResult()
    check_path(fixture, result)
    assert not result.passed
    assert any(f.rule_id == "DB002" for f in result.findings), "Expected DB002"


def test_registration_in_ready_fails() -> None:
    """Command registration in ready handler should trigger DB003."""
    fixture = Path(__file__).parent / "fixtures" / "js_broken" / "ready_registration.js"
    result = CheckResult()
    check_path(fixture, result)
    assert not result.passed
    assert any(f.rule_id == "DB003" for f in result.findings), "Expected DB003"


def test_missing_intents_warns() -> None:
    """Client without explicit intents should trigger DB004."""
    fixture = Path(__file__).parent / "fixtures" / "js_broken" / "missing_intents.js"
    result = CheckResult()
    check_path(fixture, result)
    assert any(f.rule_id == "DB004" for f in result.findings), "Expected DB004"


def test_unbounded_collector_warns() -> None:
    """Collector without timeout should trigger DB005."""
    fixture = Path(__file__).parent / "fixtures" / "js_broken" / "unbounded_collector.js"
    result = CheckResult()
    check_path(fixture, result)
    assert any(f.rule_id == "DB005" for f in result.findings), "Expected DB005"


def test_literal_token_run_fails() -> None:
    """Literal token in client.run() should trigger DB011."""
    fixture = Path(__file__).parent / "fixtures" / "js_broken" / "literal_token.js"
    result = CheckResult()
    check_path(fixture, result)
    assert not result.passed
    assert any(f.rule_id == "DB011" for f in result.findings), "Expected DB011"


def test_clean_python_file_passes() -> None:
    """A clean Python file should produce no findings."""
    fixture = Path(__file__).parent / "fixtures" / "python_ok" / "clean_bot.py"
    result = CheckResult()
    check_path(fixture, result)
    assert result.passed, f"Expected PASS, got: {[f.rule_id for f in result.findings]}"


def test_time_sleep_in_async_fails() -> None:
    """time.sleep() in async Python should trigger DB009."""
    fixture = Path(__file__).parent / "fixtures" / "python_broken" / "time_sleep.py"
    result = CheckResult()
    check_path(fixture, result)
    assert not result.passed
    assert any(f.rule_id == "DB009" for f in result.findings), "Expected DB009"


def test_tree_sync_in_on_ready_warns() -> None:
    """tree.sync() in on_ready should trigger DB010."""
    fixture = Path(__file__).parent / "fixtures" / "python_broken" / "tree_sync_ready.py"
    result = CheckResult()
    check_path(fixture, result)
    assert any(f.rule_id == "DB010" for f in result.findings), "Expected DB010"


def test_missing_intents_constructor_warns() -> None:
    """Bot constructor without intents should trigger DB012."""
    fixture = Path(__file__).parent / "fixtures" / "python_broken" / "missing_intents.py"
    result = CheckResult()
    check_path(fixture, result)
    assert any(f.rule_id == "DB012" for f in result.findings), "Expected DB012"


def test_python_shadow_fails(tmp_path: Path) -> None:
    """A file named discord.py should trigger DB008."""
    # Create a temporary file named discord.py to test shadowing detection
    shadow_file = tmp_path / "discord.py"
    shadow_file.write_text("# This file shadows the discord module\n")
    result = CheckResult()
    check_path(shadow_file, result)
    assert not result.passed
    assert any(f.rule_id == "DB008" for f in result.findings), "Expected DB008"


def test_checker_on_broken_fixtures_dir() -> None:
    """Running checker on broken fixtures should produce failures."""
    fixture_dir = Path(__file__).parent / "fixtures" / "js_broken"
    result = CheckResult()
    check_path(fixture_dir, result)
    assert result.fail_count > 0, "Expected some FAIL findings in js_broken"


def test_checker_on_ok_fixtures_dir() -> None:
    """Running checker on ok fixtures should produce no failures."""
    fixture_dir = Path(__file__).parent / "fixtures" / "js_ok"
    result = CheckResult()
    check_path(fixture_dir, result)
    assert result.passed, f"Expected PASS on ok fixtures, got: {[f.rule_id for f in result.findings]}"
