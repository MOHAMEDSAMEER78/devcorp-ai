"""Unit tests for Centralized App Configuration."""
from packages.core.config import AppConfig


def test_default_config():
    cfg = AppConfig()
    assert cfg.project_name == "DevCorp AI"
    assert "devcorp" in cfg.postgres_url
    assert cfg.litellm_proxy_url == "http://localhost:4000"
