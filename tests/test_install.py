import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('personal_install', ROOT / 'scripts/install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name) / 'project'
        self.project.mkdir()
        self.git('init', '-q')
        for name in ('AGENTS.md', 'README.md', 'package.json', '.gitignore'):
            (self.project / name).write_text('team-owned\n')
        self.git('add', '.')

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.project), *args], text=True)

    def test_install_is_private_to_checkout_and_preserves_team_files(self):
        before = self.git('status', '--porcelain')
        installer.install(self.project)
        self.assertEqual(self.git('status', '--porcelain'), before)
        for name in ('AGENTS.md', 'README.md', 'package.json', '.gitignore'):
            self.assertEqual((self.project / name).read_text(), 'team-owned\n')
        self.assertTrue((self.project / '.agents/skills/roport-orchestrator/SKILL.md').is_file())
        self.assertTrue((self.project / '.agents/skills/harness/NOTICE').is_file())
        self.assertFalse((self.project / 'scripts').exists())

    def test_dry_run_creates_no_assets_or_excludes(self):
        exclude = self.project / '.git/info/exclude'
        before = exclude.read_bytes()
        self.assertTrue(installer.install(self.project, dry_run=True))
        self.assertFalse((self.project / '.agents').exists())
        self.assertEqual(exclude.read_bytes(), before)

    def test_second_install_is_noop(self):
        installer.install(self.project)
        self.assertEqual(installer.install(self.project), [])

    def test_conflict_is_rejected_before_other_writes(self):
        conflict = self.project / '.agents/skills/roport-orchestrator/SKILL.md'
        conflict.parent.mkdir(parents=True)
        conflict.write_text('user edits\n')
        with self.assertRaisesRegex(ValueError, 'Conflicting'):
            installer.install(self.project)
        self.assertEqual(conflict.read_text(), 'user edits\n')
        self.assertFalse((self.project / '.codex').exists())
        self.assertFalse((self.project / '.agents/skills/harness').exists())

    def test_tracked_files_are_never_taken_over(self):
        path = self.project / '.codex/agents/harness-worker.toml'
        path.parent.mkdir(parents=True)
        path.write_bytes((ROOT / '.codex/agents/harness-worker.toml').read_bytes())
        self.git('add', '.codex')
        with self.assertRaisesRegex(ValueError, 'tracked project file'):
            installer.install(self.project)
        self.assertFalse((self.project / '.agents').exists())

    def test_existing_model_and_agent_preferences_are_preserved(self):
        config = self.project / '.codex/config.toml'
        config.parent.mkdir()
        text = 'model = "keep-my-model"\n[agents]\nenabled = false\nmax_threads = 2\n'
        config.write_text(text)
        installer.install(self.project)
        self.assertEqual(config.read_text(), text)

    def test_tracked_config_needing_changes_is_rejected(self):
        config = self.project / '.codex/config.toml'
        config.parent.mkdir()
        config.write_text('model = "keep-my-model"\n')
        self.git('add', '.codex')
        with self.assertRaisesRegex(ValueError, 'Tracked .codex/config.toml'):
            installer.install(self.project)
        self.assertFalse((self.project / '.agents').exists())

    def test_symlink_destination_is_rejected(self):
        link = Path(self.tmp.name) / 'link'
        link.symlink_to(self.project, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            installer.install(link)

    def test_non_git_and_nested_targets_are_rejected(self):
        empty = Path(self.tmp.name) / 'empty'
        empty.mkdir()
        with self.assertRaises(ValueError):
            installer.install(empty)
        nested = self.project / 'nested'
        nested.mkdir()
        with self.assertRaisesRegex(ValueError, 'project root'):
            installer.install(nested)


if __name__ == '__main__':
    unittest.main()
