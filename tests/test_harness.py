"""Check execution boundaries without installing dependencies or starting devices."""

import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("roport_harness", Path(__file__).resolve().parents[1] / "scripts/harness.py")
harness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(harness)


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name)
        (self.project / "AGENTS.md").write_text("team rules\n")
        (self.project / "services").mkdir()

    def invoke(self, args):
        return harness.main(["--project", str(self.project), *args])

    def test_project_is_required(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                harness.main(["check"])
        self.assertEqual(raised.exception.code, 2)

    def test_harness_source_is_not_an_application_target(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                harness.main(["--project", str(harness.HARNESS_ROOT), "check"])
        self.assertEqual(raised.exception.code, 2)

    def test_module_is_required_and_unknown_modules_are_rejected(self):
        for args in (["ci"], ["ci", "--module", "unknown"]):
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    self.invoke(args)
                self.assertEqual(raised.exception.code, 2)

    def test_dry_run_never_starts_a_process(self):
        with patch.object(harness.subprocess, "run") as run, contextlib.redirect_stdout(io.StringIO()):
            for module in harness.MODULES:
                self.assertEqual(self.invoke(["ci", "--module", module, "--dry-run"]), 0)
            self.assertEqual(self.invoke(["check", "--dry-run"]), 0)
        run.assert_not_called()

    def test_module_runs_in_its_own_directory(self):
        with patch.object(harness.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)) as run:
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(self.invoke(["ci", "--module", "web"]), 0)
        self.assertEqual(run.call_count, 3)
        for call in run.call_args_list:
            self.assertEqual(call.kwargs["cwd"], self.project / "services/roport-web")
            self.assertNotIn("shell", call.kwargs)

    def test_failure_stops_before_later_commands(self):
        with patch.object(harness.subprocess, "run", return_value=subprocess.CompletedProcess([], 7)) as run:
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(self.invoke(["ci", "--module", "web"]), 7)
        self.assertEqual(run.call_count, 1)

    def test_missing_executable_is_reported(self):
        error = FileNotFoundError(2, "No such file", "mvn")
        with patch.object(harness.subprocess, "run", side_effect=error):
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()) as stderr:
                self.assertEqual(self.invoke(["ci", "--module", "service-server"]), 127)
        self.assertIn("mvn", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
