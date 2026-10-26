#!/usr/bin/env python3
"""Install personal Codex assets locally without editing tracked project rules."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.agents/skills/harness/scripts'))
from common import agent_names, apply_files, existing_bytes, safe_path


def merge_config(current: str) -> str:
    """Adapted from revfactory/codex-harness scripts/install.py at pinned SHA."""
    data = tomllib.loads(current)
    agents = data.get('agents', {})
    if not isinstance(agents, dict):
        raise ValueError('Expected a TOML table for agents.')
    additions = {}
    if 'enabled' not in agents:
        additions['enabled'] = True
    if not {'max_concurrent_threads_per_session', 'max_threads'} & agents.keys():
        additions['max_concurrent_threads_per_session'] = 3
    if not additions:
        return current
    lines = ''.join(f'{key} = {str(value).lower()}\n' for key, value in additions.items())
    header = re.search(r'(?m)^\[\s*(?:agents|\x27agents\x27|"agents")\s*\][ \t]*(?:#[^\n]*)?(?:\n|$)', current)
    if header:
        point = header.end()
        merged = current[:point] + ('' if current[:point].endswith('\n') else '\n') + lines + current[point:]
    else:
        merged = current + ('\n' if current else '') + '[agents]\n' + lines
        try:
            tomllib.loads(merged)
        except tomllib.TOMLDecodeError:
            merged = ''.join(f'agents.{key} = {str(value).lower()}\n' for key, value in additions.items()) + current
    try:
        actual = tomllib.loads(merged)
    except tomllib.TOMLDecodeError as exc:
        raise ValueError('Cannot safely extend inline agents config; use an [agents] table.') from exc
    expected = {**data, 'agents': {**agents, **additions}}
    if actual != expected:
        raise ValueError('Config merge would alter existing settings.')
    return merged


def git(target: Path, *args: str) -> str:
    result = subprocess.run(['git', '-C', str(target), *args], capture_output=True, text=True)
    if result.returncode:
        raise ValueError(result.stderr.strip() or 'Target must be a Git project root.')
    return result.stdout.rstrip('\n')


def merge_excludes(current: str, entries: list[str]) -> str:
    start, end = '# roport-codex-harness:start', '# roport-codex-harness:end'
    block = start + '\n' + '\n'.join(entries) + '\n' + end + '\n'
    if start not in current and end not in current:
        return current + ('\n' if current and not current.endswith('\n') else '') + block
    if current.count(start) != 1 or current.count(end) != 1 or current.index(start) > current.index(end):
        raise ValueError('Malformed local harness exclude markers.')
    return current[:current.index(start)] + block.rstrip('\n') + current[current.index(end) + len(end):]


def install(target: Path, *, dry_run: bool = False) -> list[Path]:
    target = safe_path(target)
    if target == ROOT:
        raise ValueError('Install into the application project, not the harness source.')
    if Path(git(target, 'rev-parse', '--show-toplevel')).resolve() != target:
        raise ValueError('Target must be the Git project root.')
    tracked = set(filter(None, git(target, 'ls-files', '-z').split('\0')))
    names = agent_names(target)
    sources = []
    for name in ('harness', 'roport-orchestrator'):
        directory = ROOT / '.agents/skills' / name
        if not (directory / 'SKILL.md').is_file():
            raise ValueError(f'Missing source skill: {name}')
        sources.extend(p for p in sorted(directory.rglob('*')) if p.is_file()
                       and '__pycache__' not in p.parts and p.suffix not in {'.pyc', '.pyo'})
    sources.extend(sorted((ROOT / '.codex/agents').glob('*.toml')))
    payload = {}
    for source in sources:
        relative = source.relative_to(ROOT)
        path = target / relative
        if relative.as_posix() in tracked:
            raise ValueError(f'Refusing to manage a tracked project file: {relative}')
        content = source.read_bytes()
        previous = existing_bytes(path)
        if previous is not None and previous != content:
            raise ValueError(f'Conflicting existing file (left unchanged): {path}')
        if source.suffix == '.toml' and source.parent == ROOT / '.codex/agents':
            name = tomllib.loads(content.decode())['name']
            if name in names and names[name] != path:
                raise ValueError(f'Duplicate existing agent: {name}')
        payload[path] = content
    config = target / '.codex/config.toml'
    previous = existing_bytes(config)
    merged = merge_config(previous.decode() if previous is not None else '').encode()
    if '.codex/config.toml' in tracked and merged != previous:
        raise ValueError('Tracked .codex/config.toml needs defaults; update it separately.')
    payload[config] = merged
    exclude = Path(git(target, 'rev-parse', '--git-path', 'info/exclude'))
    if not exclude.is_absolute():
        exclude = target / exclude
    previous_exclude = existing_bytes(exclude)
    entries = ['/.agents/skills/harness/', '/.agents/skills/roport-orchestrator/']
    entries += ['/' + source.relative_to(ROOT).as_posix() for source in sources
                if source.parent == ROOT / '.codex/agents']
    if '.codex/config.toml' not in tracked:
        entries.append('/.codex/config.toml')
    entries += ['/.harness/', '/_workspace/communications/']
    payload[exclude] = merge_excludes(previous_exclude.decode() if previous_exclude else '', entries).encode()
    return apply_files(payload, dry_run=dry_run)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, required=True)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        changed = install(args.target, dry_run=args.dry_run)
        for path in changed:
            print(f'{"Would write" if args.dry_run else "Wrote"} {path}')
        print(f'{len(changed)} file(s) {"planned" if args.dry_run else "changed"}.')
        print('Open a new Codex chat in the target and invoke $roport-orchestrator.')
        return 0
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
