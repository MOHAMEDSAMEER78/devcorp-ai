"""Unit tests for Demo Synthesis Engine."""
import pytest
from pathlib import Path
from packages.demo_engine import (
    EphemeralEnvironment,
    DemoRecorderConfig,
    DemoBundler,
    get_cursor_script,
)


def test_demo_recorder_config(tmp_path):
    cfg = DemoRecorderConfig(output_dir=str(tmp_path / "demos"))
    assert cfg.viewport["width"] == 1280
    assert cfg.slow_mo_ms == 500
    assert "demo-cursor-indicator" in get_cursor_script()


def test_demo_bundler(tmp_path):
    output_dir = tmp_path / "demos"
    output_dir.mkdir()
    sample_mp4 = output_dir / "walkthrough.mp4"
    sample_mp4.write_text("fake video binary stream")

    bundler = DemoBundler(bundle_dir=str(output_dir))
    bundle = bundler.package_bundle(sprint_id="sprint-1")

    assert bundle.bundle_id == "demo-sprint-1"
    assert len(bundle.items) == 1
    assert bundle.items[0].artifact_type == "mp4_video"
    assert (output_dir / "manifest.json").exists()


def test_ephemeral_environment():
    env = EphemeralEnvironment(frontend_port=3000, backend_port=8000)
    health = env.check_health()
    assert "frontend" in health
    assert "backend" in health
    env.teardown()
