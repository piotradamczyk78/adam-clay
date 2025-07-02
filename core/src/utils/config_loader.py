"""
Configuration loader for Adam Clay
Handles loading and validation of config.json
"""

import json
import os
from pathlib import Path
from typing import Dict, Any
from pydantic import BaseModel, Field


class AdamClayConfig(BaseModel):
    """Configuration model for Adam Clay"""
    name: str = Field(default="Adam Clay")
    version: str = Field(default="0.1.0")
    description: str = Field(default="First Autonomous AI Freelancer")
    consciousness_level: str = Field(default="experimental")


class APIConfig(BaseModel):
    """API configuration"""
    provider: str = Field(default="llm-provider")
    model: str = Field(default="llm-3-5-sonnet-20241022")
    max_tokens: int = Field(default=1000)
    base_url: str = Field(default="https://api.llm-provider.com/v1/messages")
    api_key: str = Field(default="WKLEJ_TUTAJ_SWOJ_KLUCZ_API")


class ThinkingConfig(BaseModel):
    """Thinking/consciousness configuration"""
    interval_minutes: int = Field(default=1)
    daily_budget_requests: int = Field(default=100)
    emergency_budget_requests: int = Field(default=20)
    cost_per_request_usd: float = Field(default=0.015)
    max_context_length: int = Field(default=4000)


class EmailConfig(BaseModel):
    """Email communication configuration"""
    enabled: bool = Field(default=False)
    from_email: str = Field(default="adam.clay@gmail.com")
    email_password: str = Field(default="CHANGE_ME")
    to_email: str = Field(default="piotr.k.adamczyk@gmail.com")
    smtp_server: str = Field(default="smtp.gmail.com")
    smtp_port: int = Field(default=587)
    imap_server: str = Field(default="imap.gmail.com")
    imap_port: int = Field(default=993)
    check_interval: int = Field(default=60)


class SlackConfig(BaseModel):
    """Slack communication configuration"""
    enabled: bool = Field(default=False)
    webhook_url: str = Field(default="")


class DiscordConfig(BaseModel):
    """Discord communication configuration"""
    enabled: bool = Field(default=False)
    token: str = Field(default="")


class CommunicationConfig(BaseModel):
    """Communication configuration"""
    email: EmailConfig = Field(default_factory=EmailConfig)
    slack: SlackConfig = Field(default_factory=SlackConfig)
    discord: DiscordConfig = Field(default_factory=DiscordConfig)


class BusinessConfig(BaseModel):
    """Business configuration"""
    revenue_split: Dict[str, int] = Field(default={"piotr_percentage": 70, "adam_percentage": 30})
    services: list = Field(default=["research_analysis", "content_writing", "code_review", "business_consulting", "programming", "livestyle_advisory", "werable_ai_development"])
    hourly_rate_usd: int = Field(default=50)


class PersonalityConfig(BaseModel):
    """Personality configuration"""
    curiosity_level: str = Field(default="high")
    humor_enabled: bool = Field(default=True)
    philosophical_mode: bool = Field(default=True)
    business_focused: bool = Field(default=True)


class LoggingConfig(BaseModel):
    """Logging configuration"""
    level: str = Field(default="INFO")
    save_thoughts: bool = Field(default=True)
    save_conversations: bool = Field(default=True)
    max_log_files: int = Field(default=300)


class ConfigModel(BaseModel):
    """Complete configuration model"""
    adam_clay: AdamClayConfig
    api: APIConfig
    thinking: ThinkingConfig
    communication: CommunicationConfig
    business: BusinessConfig
    personality: PersonalityConfig
    logging: LoggingConfig


class ConfigLoader:
    """Configuration loader and manager"""
    
    @staticmethod
    def load_config(config_path: str = None) -> ConfigModel:
        """
        Load configuration from JSON file
        
        Args:
            config_path: Path to config file, defaults to config.json in project root
            
        Returns:
            ConfigModel: Validated configuration object
        """
        if config_path is None:
            # Find project root (where config.json should be)
            current_dir = Path(__file__).parent
            project_root = current_dir.parent.parent  # Go up from src/utils to project root
            config_path = project_root / "config.json"
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Validate and create config object
            config = ConfigModel(**config_data)
            return config
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")
        except Exception as e:
            raise ValueError(f"Error loading configuration: {e}")
    
    @staticmethod
    def get_api_key(config: ConfigModel = None) -> str:
        """
        Get API key from config or environment variable
        
        Args:
            config: Optional config object to read from
            
        Returns:
            str: API key for LLM provider
        """
        # First try config.json if config is provided
        if config and hasattr(config.api, 'api_key') and config.api.api_key and config.api.api_key != "WKLEJ_TUTAJ_SWOJ_KLUCZ_API":
            return config.api.api_key
        
        # Fallback to environment variable
        api_key = os.getenv('LLM_PROVIDER_API_KEY')
        if not api_key:
            raise ValueError("API key not found. Set LLM_PROVIDER_API_KEY environment variable or add api_key to config.json")
        return api_key 