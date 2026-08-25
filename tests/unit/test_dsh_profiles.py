"""Unit tests validating all 13 DSH Cordis YAML Profiles."""
from pathlib import Path
import yaml
import pytest

EXPECTED_PROFILES = [
    "product-manager",
    "architect-requirements",
    "architect-system",
    "architect-data",
    "architect-ux",
    "architect-security",
    "agent-router",
    "engineering-manager",
    "engineer-backend",
    "engineer-frontend",
    "engineer-ux",
    "qa-reviewer",
    "demo-release",
]


@pytest.mark.parametrize("profile_name", EXPECTED_PROFILES)
def test_dsh_profile_valid_and_complete(profile_name):
    path = Path(f"profiles/{profile_name}.cordis.yml")
    assert path.exists(), f"Profile {path} does not exist"

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert data["name"] == profile_name
    assert "version" in data
    assert "plugins" in data
    assert len(data["plugins"]) >= 2

    plugin_names = [p["name"] for p in data["plugins"]]
    assert "dsh-model-litellm" in plugin_names
    assert "dsh-a2a" in plugin_names
    assert "dsh-trajectory" in plugin_names

    # Check A2A card structure
    a2a_plugin = next(p for p in data["plugins"] if p["name"] == "dsh-a2a")
    assert "card" in a2a_plugin["config"]
    assert "skills" in a2a_plugin["config"]["card"]
    assert len(a2a_plugin["config"]["card"]["skills"]) >= 1


def test_engineering_profiles_have_mcp_and_sandbox():
    eng_profiles = ["engineer-backend", "engineer-frontend", "engineer-ux", "qa-reviewer"]

    for name in eng_profiles:
        path = Path(f"profiles/{name}.cordis.yml")
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        plugin_names = [p["name"] for p in data["plugins"]]
        assert "dsh-mcp" in plugin_names, f"{name} must have dsh-mcp plugin"
        assert "dsh-sandbox" in plugin_names, f"{name} must have dsh-sandbox plugin"
