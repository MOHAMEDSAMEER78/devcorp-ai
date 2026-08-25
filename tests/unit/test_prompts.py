"""Unit tests verifying all 13 Specialist Agent System Prompts."""
from pathlib import Path
import pytest
from packages.core.prompt_loader import PromptLoader

EXPECTED_ROLES = [
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


@pytest.mark.parametrize("role_name", EXPECTED_ROLES)
def test_system_prompt_exists_and_loaded(role_name):
    loader = PromptLoader(prompts_dir="prompts")
    prompt_text = loader.load_prompt(role_name)
    assert len(prompt_text) > 100
    assert "Role:" in prompt_text
