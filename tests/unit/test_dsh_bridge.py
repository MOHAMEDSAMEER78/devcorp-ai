"""Unit tests for DSH Bridge Dispatcher."""
import pytest
from packages.core.dsh_bridge import DSHBridge


def test_dsh_bridge_endpoints():
    bridge = DSHBridge()
    client = bridge.get_client("backend_engineer")
    assert client.base_url == "http://localhost:8089"


def test_dsh_bridge_unknown_role():
    bridge = DSHBridge()
    with pytest.raises(KeyError):
        bridge.get_client("unknown_agent_role")
