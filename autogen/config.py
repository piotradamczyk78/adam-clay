import os
from pathlib import Path
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

class DatabaseConfig(BaseModel):
    host: str = "localhost"
    port: int = 3306
    username: str = "root"
    password: str = ""
    database: str = "adam_clay_autogen"
    
class AdamClayIntegration(BaseModel):
    """Konfiguracja integracji z głównym systemem Adam Clay"""
    consciousness_api_url: str = "http://localhost:8004/api"
    laravel_api_url: str = "http://localhost:8000/api"
    websocket_url: str = "ws://localhost:8005/ws"
    api_key: str = ""
    
class AgentConfig(BaseModel):
    """Konfiguracja domyślna dla agentów"""
    max_tokens: int = 1000
    temperature: float = 0.7
    model: str = "gpt-4-turbo-preview"
    max_conversation_history: int = 50
    
class AutoGenConfig(BaseSettings):
    """Główna konfiguracja serwisu AutoGen"""
    
    # Podstawowe ustawienia serwisu
    service_name: str = "Adam Clay AutoGen Subconscious"
    version: str = "1.0.0"
    host: str = "0.0.0.0"
    port: int = 8005
    debug: bool = True
    
    # Konfiguracja bazy danych
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    
    # Integracja z Adam Clay
    adam_clay: AdamClayIntegration = Field(default_factory=AdamClayIntegration)
    
    # Ustawienia agentów
    agents: AgentConfig = Field(default_factory=AgentConfig)
    
    # Ścieżki
    project_root: Path = Path(__file__).parent.parent
    data_dir: Path = project_root / "data"
    logs_dir: Path = project_root / "autogen" / "logs"
    
    # Klucze API
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    # Ustawienia logowania
    log_level: str = "INFO"
    log_file: str = "autogen.log"
    
    class Config:
        env_file = ".env"
        env_prefix = "AUTOGEN_"
        env_nested_delimiter = "__"
        extra = "allow"
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Tworzenie katalogów jeśli nie istnieją
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)

# Globalna instancja konfiguracji
config = AutoGenConfig() 