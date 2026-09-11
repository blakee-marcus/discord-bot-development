#!/usr/bin/env python3
"""discord_doctor.py — deterministic checker for Discord bot code.

High-confidence rules only. Anything requiring control/data flow analysis
stays WARN and must not be overclaimed.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class Severity(str, Enum):
    FAIL = "FAIL"
    WARN = "WARN"
    INFO = "INFO"


RULES = {
    "DB001": ("hardcoded_token", Severity.FAIL, "Hardcoded bot token detected"),
    "DB002": ("legacy_discord_js_api", Severity.FAIL, "Legacy discord.js v12/v13 API usage"),
    "DB003": ("registration_in_ready", Severity.FAIL, "Command registration inside ready/on_ready handler"),
    "DB004": ("missing_intents", Severity.WARN, "Client/Bot constructed without explicit intents"),
    "DB005": ("unbounded_collector", Severity.WARN, "Collector/modal await without timeout"),
    "DB006": ("deprecated_response", Severity.FAIL, "Deprecated response method"),
    "DB007": ("deprecated_dm", Severity.WARN, "Deprecated DM option or method"),
    "DB008": ("python_shadow", Severity.FAIL, "Python file/package shadows 'discord'"),
    "DB009": ("time_sleep_async", Severity.FAIL, "time.sleep() used in async context"),
    "DB010": ("tree_sync_ready", Severity.WARN, "tree.sync() called from on_ready"),
    "DB011": ("literal_token_run", Severity.FAIL, "Literal token passed to run/start/login"),
    "DB012": ("missing_intents_constructor", Severity.WARN, "Bot() without intents parameter"),
    "DB013": ("double_response", Severity.WARN, "Multiple response calls without is_done() guard"),
    "DB014": ("ack_after_defer", Severity.WARN, "Response call after defer without followup"),
}


@dataclass
class Finding:
    rule_id: str
    severity: Severity
    message: str
    file: str
    line: int
    snippet: str = ""


@dataclass
class CheckResult:
    findings: list[Finding] = field(default_factory=list)
    files_checked: int = 0
    errors: list[str] = field(default_factory=list)

    @property
    def fail_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == Severity.FAIL)

    @property
    def warn_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == Severity.WARN)

    @property
    def passed(self) -> bool:
        return self.fail_count == 0


def _read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []


def check_js_file(path: Path, result: CheckResult) -> None:
    lines = _read_lines(path)
    if not lines:
        return

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # DB001: Hardcoded token
        if re.search(r'["\'][\w-]{20,}\.[\w-]+\.[\w-]+["\']', stripped):
            result.findings.append(Finding(
                rule_id="DB001",
                severity=Severity.FAIL,
                message=RULES["DB001"][2],
                file=str(path),
                line=i,
                snippet=stripped[:100],
            ))

        # DB011: Literal token in run/start/login
        if re.search(r'\.(run|start|login)\s*\(\s*["\']', stripped):
            result.findings.append(Finding(
                rule_id="DB011",
                severity=Severity.FAIL,
                message=RULES["DB011"][2],
                file=str(path),
                line=i,
                snippet=stripped[:100],
            ))

        # DB002: Legacy discord.js APIs
        legacy_patterns = [
            r"new\s+Discord\s*\.\s*Client\s*\(\s*\)",
            r"\.createReactionCollector\s*\(",
            r"\.awaitReactions\s*\(",
            r"client\s*\.\s*on\s*\(\s*['\"]message['\"]",
            r"new\s+Discord\s*\.\s*MessageEmbed\s*\(",
            r"\.addField\s*\(",
            r"\.addFields\s*\(",
        ]
        for pattern in legacy_patterns:
            if re.search(pattern, stripped):
                result.findings.append(Finding(
                    rule_id="DB002",
                    severity=Severity.FAIL,
                    message=RULES["DB002"][2],
                    file=str(path),
                    line=i,
                    snippet=stripped[:100],
                ))
                break

        # DB004: Missing intents — look for `new Client(` without intents nearby
        if re.search(r"new\s+(Client|ShardingManager)\s*\(", stripped):
            window = "\n".join(lines[i:i+8])
            if "intents" not in window.lower():
                result.findings.append(Finding(
                    rule_id="DB004",
                    severity=Severity.WARN,
                    message=RULES["DB004"][2],
                    file=str(path),
                    line=i,
                    snippet=stripped[:100],
                ))

        # DB005: Unbounded collector
        if re.search(r"(createMessageComponentCollector|createReactionCollector)\s*\(\s*\{", stripped):
            window = "\n".join(lines[i:i+4])
            if "time" not in window.lower():
                result.findings.append(Finding(
                    rule_id="DB005",
                    severity=Severity.WARN,
                    message=RULES["DB005"][2],
                    file=str(path),
                    line=i,
                    snippet=stripped[:100],
                ))

        # DB013: Double response without guard
        if re.search(r"interaction\s*\.\s*response\s*\.\s*(sendMessage|reply|editReply)\s*\(", stripped):
            context = "\n".join(lines[max(0, i-3):i])
            if "is_done" not in context.lower():
                result.findings.append(Finding(
                    rule_id="DB013",
                    severity=Severity.WARN,
                    message=RULES["DB013"][2],
                    file=str(path),
                    line=i,
                    snippet=stripped[:100],
                ))

    # DB003: Registration in ready — multi-line window search
    for i, line in enumerate(lines):
        if re.search(r"client\s*\.\s*on\s*\(\s*['\"]ready['\"]", line):
            # Look at the next 15 lines for command registration
            window = "\n".join(lines[i:i+16])
            if re.search(r"(application\.commands|applicationCommands|\.commands)\.\s*(set|create|bulkOverwrite)", window, re.IGNORECASE):
                result.findings.append(Finding(
                    rule_id="DB003",
                    severity=Severity.FAIL,
                    message=RULES["DB003"][2],
                    file=str(path),
                    line=i+1,
                    snippet=line.strip()[:100],
                ))


def check_python_file(path: Path, result: CheckResult) -> None:
    lines = _read_lines(path)
    if not lines:
        return

    # DB008: Python file shadows discord
    if path.name == "discord.py" or (path.name == "discord" and path.is_dir()):
        result.findings.append(Finding(
            rule_id="DB008",
            severity=Severity.FAIL,
            message=RULES["DB008"][2],
            file=str(path),
            line=0,
            snippet=str(path),
        ))
        return

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # DB009: time.sleep in async
        if re.search(r"\btime\.sleep\s*\(", stripped):
            result.findings.append(Finding(
                rule_id="DB009",
                severity=Severity.FAIL,
                message=RULES["DB009"][2],
                file=str(path),
                line=i,
                snippet=stripped[:100],
            ))

        # DB001: Hardcoded token in Python
        if re.search(r'["\'][\w-]{20,}\.[\w-]+\.[\w-]+["\']', stripped):
            result.findings.append(Finding(
                rule_id="DB001",
                severity=Severity.FAIL,
                message=RULES["DB001"][2],
                file=str(path),
                line=i,
                snippet=stripped[:100],
            ))

        # DB011: Literal token in run()
        if re.search(r"\.run\s*\(\s*[\"']", stripped):
            result.findings.append(Finding(
                rule_id="DB011",
                severity=Severity.FAIL,
                message=RULES["DB011"][2],
                file=str(path),
                line=i,
                snippet=stripped[:100],
            ))

        # DB012: Bot constructor without intents
        if re.search(r"(commands\.)?Bot\s*\(\s*command_prefix", stripped) and "intents" not in stripped:
            result.findings.append(Finding(
                rule_id="DB012",
                severity=Severity.WARN,
                message=RULES["DB012"][2],
                file=str(path),
                line=i,
                snippet=stripped[:100],
            ))

    # DB010: tree.sync() in on_ready — multi-line window search
    for i, line in enumerate(lines):
        if re.search(r"async\s+def\s+on_ready", line):
            window = "\n".join(lines[i:i+10])
            if re.search(r"tree\.sync\s*\(", window):
                result.findings.append(Finding(
                    rule_id="DB010",
                    severity=Severity.WARN,
                    message=RULES["DB010"][2],
                    file=str(path),
                    line=i+1,
                    snippet=line.strip()[:100],
                ))


def check_file(path: Path, result: CheckResult) -> None:
    suffix = path.suffix.lower()
    result.files_checked += 1

    if suffix in (".js", ".ts", ".mjs", ".cjs"):
        check_js_file(path, result)
    elif suffix == ".py":
        check_python_file(path, result)


def check_path(target: Path, result: CheckResult) -> None:
    if target.is_file():
        check_file(target, result)
    elif target.is_dir():
        for path in target.rglob("*"):
            if path.is_file() and path.suffix.lower() in (".js", ".ts", ".py", ".mjs", ".cjs"):
                if any(part in path.parts for part in ("node_modules", ".venv", "__pycache__", "dist", "build")):
                    continue
                check_file(path, result)


def format_report(result: CheckResult) -> str:
    lines = []
    if not result.findings:
        lines.append("PASS: No issues found")
        lines.append(f"Files checked: {result.files_checked}")
        return "\n".join(lines)

    grouped: dict[str, list[Finding]] = {}
    for f in result.findings:
        grouped.setdefault(f.severity.value, []).append(f)

    for severity in ["FAIL", "WARN", "INFO"]:
        if severity not in grouped:
            continue
        lines.append(f"\n=== {severity} ({len(grouped[severity])}) ===")
        for finding in grouped[severity]:
            lines.append(f"\n[{finding.rule_id}] {finding.message}")
            lines.append(f"  {finding.file}:{finding.line}")
            if finding.snippet:
                lines.append(f"  {finding.snippet[:80]}")

    lines.append("\n--- Summary ---")
    lines.append(f"FAIL: {result.fail_count}  WARN: {result.warn_count}")
    lines.append(f"Files checked: {result.files_checked}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Discord bot code checker")
    parser.add_argument("path", help="File or directory to check")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--rules", action="store_true", help="List rule IDs")
    args = parser.parse_args()

    if args.rules:
        for rule_id, (name, sev, desc) in sorted(RULES.items()):
            print(f"{rule_id}: {sev.value} - {name}")
        return 0

    target = Path(args.path)
    if not target.exists():
        print(f"Error: {args.path} not found", file=sys.stderr)
        return 1

    result = CheckResult()
    check_path(target, result)

    if args.json:
        output = {
            "passed": result.passed,
            "fail_count": result.fail_count,
            "warn_count": result.warn_count,
            "files_checked": result.files_checked,
            "findings": [
                {
                    "rule_id": f.rule_id,
                    "severity": f.severity.value,
                    "message": f.message,
                    "file": f.file,
                    "line": f.line,
                }
                for f in result.findings
            ],
        }
        print(json.dumps(output, indent=2))
    else:
        print(format_report(result))

    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
