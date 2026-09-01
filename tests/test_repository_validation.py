import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_audit(*args):
    return subprocess.run(
        [sys.executable, "scripts/audit_system_design.py", "--root", str(ROOT), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_system_design_audit_accepts_current_baseline():
    result = run_audit("--max-structural-filler", "27", "--max-copied-capacity", "134")

    assert result.returncode == 0
    assert "Structural filler guides: 27" in result.stdout
    assert "Copied-capacity guides: 134" in result.stdout
    assert "16-networking" in result.stdout


def test_system_design_audit_fails_only_when_threshold_is_exceeded():
    result = run_audit("--max-structural-filler", "26", "--max-copied-capacity", "134")

    assert result.returncode == 1
    assert "structural filler 27 > 26" in result.stderr
