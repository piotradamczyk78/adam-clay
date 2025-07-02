"""
Tests for configuration loader
"""

import pytest
import tempfile
import json
from pathlib import Path

from src.utils.config_loader import ConfigLoader, ConfigModel


def test_load_valid_config():
    """Test loading valid configuration"""
    # This will load the actual config.json from project
    config = ConfigLoader.load_config()
    
    assert isinstance(config, ConfigModel)
    assert config.adam_clay.name == "Adam Clay"
    assert config.adam_clay.version == "0.1.0"
    assert config.business.revenue_split["piotr_percentage"] == 70
    assert config.business.revenue_split["adam_percentage"] == 30


def test_load_config_with_custom_path():
    """Test loading configuration from custom path"""
    # Create temporary config file
    test_config = {
        "adam_clay": {
            "name": "Test AI",
            "version": "0.0.1",
            "description": "Test AI",
            "consciousness_level": "testing"
        },
        "api": {
            "provider": "llm-provider",
            "model": "llm-3-5-sonnet-20241022",
            "max_tokens": 500,
            "base_url": "https://api.llm-provider.com/v1/messages"
        },
        "thinking": {
            "interval_minutes": 10,
            "daily_budget_requests": 50,
            "emergency_budget_requests": 10,
            "cost_per_request_usd": 0.01,
            "max_context_length": 2000
        },
        "business": {
            "revenue_split": {"piotr_percentage": 80, "adam_percentage": 20},
            "services": ["testing"],
            "hourly_rate_usd": 25
        },
        "personality": {
            "curiosity_level": "medium",
            "humor_enabled": False,
            "philosophical_mode": False,
            "business_focused": True
        },
        "logging": {
            "level": "DEBUG",
            "save_thoughts": False,
            "save_conversations": False,
            "max_log_files": 10
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_config, f)
        temp_path = f.name
    
    try:
        config = ConfigLoader.load_config(temp_path)
        assert config.adam_clay.name == "Test AI"
        assert config.thinking.daily_budget_requests == 50
        assert config.business.revenue_split["adam_percentage"] == 20
    finally:
        Path(temp_path).unlink()  # Clean up


def test_load_nonexistent_config():
    """Test error handling for nonexistent config file"""
    with pytest.raises(FileNotFoundError):
        ConfigLoader.load_config("/nonexistent/config.json")


def test_load_invalid_json():
    """Test error handling for invalid JSON"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("{ invalid json }")
        temp_path = f.name
    
    try:
        with pytest.raises(ValueError, match="Invalid JSON"):
            ConfigLoader.load_config(temp_path)
    finally:
        Path(temp_path).unlink()


def test_api_key_from_env(monkeypatch):
    """Test API key loading from environment"""
    test_key = "test-api-key-123"
    monkeypatch.setenv("LLM_PROVIDER_API_KEY", test_key)
    
    api_key = ConfigLoader.get_api_key()
    assert api_key == test_key


def test_missing_api_key(monkeypatch):
    """Test error when API key is missing"""
    monkeypatch.delenv("LLM_PROVIDER_API_KEY", raising=False)
    
    with pytest.raises(ValueError, match="LLM_PROVIDER_API_KEY environment variable not set"):
        ConfigLoader.get_api_key() 