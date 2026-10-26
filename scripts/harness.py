#!/usr/bin/env python3
"""Run hardware-free repository checks or an explicitly selected module's CI."""

from __future__ import annotations

import argparse
from pathlib import Path
import shlex
import subprocess
import sys

HARNESS_ROOT = Path(__file__).resolve().parents[1]
MODULES = ("pinky", "omx", "control-server", "ai-server", "service-server", "web")


def module_commands(module: str) -> list[list[str]]:
    """Keep commands aligned with .github/workflows/<module>-ci.yml."""
    if module == "pinky":
        return [["bash", "ci/test.sh"]]
    if module == "service-server":
        return [["mvn", "--batch-mode", "--no-transfer-progress", "verify"]]
    if module == "web":
        return [["npm", "ci"], ["npm", "run", "typecheck"], ["npm", "run", "build"]]
    if module not in ("omx", "control-server", "ai-server"):
        raise ValueError(f"Unknown module: {module}")
    scope = "src" if module == "omx" else "."
    commands = [
        ["uv", "sync", "--locked"],
        ["uv", "run", "ruff", "check", scope],
        ["uv", "run", "ruff", "format", "--check", scope],
    ]
    if module == "omx":
        commands += [
            ["uv", "run", "python", "-c", "import roport_omx"],
            ["bash", "ci/test.sh"],
        ]
    else:
        commands.append(["uv", "run", "pytest"])
    return commands + [["uv", "build"]]


def check_commands() -> list[list[str]]:
    return [
        [sys.executable, str(HARNESS_ROOT / ".agents/skills/harness/scripts/validate.py"), "--project", "."],
        ["npm", "run", "test:commit"],
        [sys.executable, "-m", "unittest", "discover", "-s", "services/roport-pinky/ci", "-p", "test_*.py", "-v"],
        [sys.executable, "-m", "unittest", "discover", "-s", "services/roport-omx/ci", "-p", "test_*.py", "-v"],
    ]


def execute(commands: list[list[str]], cwd: Path, *, dry_run: bool = False) -> int:
    for command in commands:
        print(f"[{cwd or '.'}] {shlex.join(command)}", flush=True)
        if dry_run:
            continue
        try:
            result = subprocess.run(command, cwd=cwd, check=False)
        except FileNotFoundError as exc:
            print(f"Missing executable: {exc.filename}", file=sys.stderr)
            return 127
        if result.returncode:
            return result.returncode if result.returncode > 0 else 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True, help="RO:PORT application root, separate from this harness checkout.")
    subparsers = parser.add_subparsers(dest="action", required=True)
    check = subparsers.add_parser("check", help="Static and mock/source checks; no dependency installation or hardware.")
    check.add_argument("--dry-run", action="store_true")
    ci = subparsers.add_parser("ci", help="Run one module's existing CI; may install locked dependencies.")
    ci.add_argument("--module", choices=MODULES, required=True)
    ci.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    project = args.project.expanduser().resolve()
    if not (project / "AGENTS.md").is_file() or not (project / "services").is_dir():
        parser.error("--project must point to the RO:PORT application root (AGENTS.md and services/).")
    if args.action == "check":
        return execute(check_commands(), project, dry_run=args.dry_run)
    return execute(module_commands(args.module), project / "services" / f"roport-{args.module}", dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
