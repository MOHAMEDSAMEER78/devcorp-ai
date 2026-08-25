"""Unit tests for Provider Registry and LiteLLM Export."""
from pathlib import Path
import pytest
from packages.core.provider_registry import ProviderRegistry, ProviderConfig


def test_load_providers_yaml():
    registry = ProviderRegistry.from_yaml("providers.yaml")
    assert len(registry.providers) > 0

    enabled = registry.get_enabled()
    assert len(enabled) > 0

    primaries = registry.get_by_tier("primary")
    assert len(primaries) >= 2


def test_filter_by_capability():
    registry = ProviderRegistry.from_yaml("providers.yaml")
    coding_models = registry.get_by_capability("coding")
    assert len(coding_models) > 0


def test_litellm_export():
    registry = ProviderRegistry.from_yaml("providers.yaml")
    config_dict = registry.to_litellm_config()

    assert "model_list" in config_dict
    assert "router_settings" in config_dict
    assert "fallbacks" in config_dict["router_settings"]
    assert len(config_dict["model_list"]) > 0
