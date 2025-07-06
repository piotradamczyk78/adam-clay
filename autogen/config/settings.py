"""
Adam Clay Eden - Advanced Configuration System
Zaawansowany system konfiguracji z parametrami psychologicznymi i ekonomicznymi
"""

import os
import json
from datetime import datetime, time
from typing import Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class MoodConfig:
    """Konfiguracja nastrojów i ich wpływ na zachowanie"""
    # Podstawowe nastroje (0.0 - 1.0)
    curiosity: float = 0.8
    excitement: float = 0.7
    happiness: float = 0.6
    energy: float = 0.7
    focus: float = 0.6
    
    # Wpływ nastroju na szybkość myślenia
    mood_thinking_multiplier: Dict[str, float] = None
    
    def __post_init__(self):
        if self.mood_thinking_multiplier is None:
            self.mood_thinking_multiplier = {
                "very_happy": 1.5,      # Bardzo szczęśliwy = szybsze myślenie
                "happy": 1.2,           # Szczęśliwy = trochę szybsze
                "neutral": 1.0,         # Neutralny = normalne
                "sad": 0.8,             # Smutny = wolniejsze
                "very_sad": 0.6,        # Bardzo smutny = bardzo wolne
                "excited": 1.8,         # Podekscytowany = bardzo szybkie
                "tired": 0.5,           # Zmęczony = bardzo wolne
                "focused": 1.3,         # Skoncentrowany = szybsze
                "confused": 0.7         # Zdezorientowany = wolniejsze
            }

@dataclass
class DopamineConfig:
    """System nagrody dopaminowej"""
    # Poziom dopaminy (0.0 - 100.0)
    current_level: float = 50.0
    max_level: float = 100.0
    min_level: float = 0.0
    
    # Wpływ na częstotliwość requestów
    high_dopamine_multiplier: float = 2.0    # Przy wysokiej dopaminie więcej requestów
    low_dopamine_multiplier: float = 0.3     # Przy niskiej dopaminie mniej requestów
    
    # Wyzwalacze dopaminy
    triggers: Dict[str, float] = None
    
    # Spadek dopaminy w czasie
    decay_rate_per_hour: float = 5.0
    
    def __post_init__(self):
        if self.triggers is None:
            self.triggers = {
                "positive_feedback": 15.0,      # Pozytywny feedback od Piotra
                "successful_task": 10.0,        # Udane wykonanie zadania
                "creative_achievement": 20.0,   # Stworzenie czegoś kreatywnego
                "learning_new": 8.0,           # Nauczenie się czegoś nowego
                "helping_human": 12.0,         # Pomoc człowiekowi
                "negative_feedback": -20.0,     # Negatywny feedback
                "error_made": -10.0,           # Popełnienie błędu
                "ignored_message": -5.0,       # Ignorowanie wiadomości
                "long_silence": -3.0           # Długa cisza
            }

@dataclass
class EconomicConfig:
    """Limity ekonomiczne i budżetowe"""
    # Dzienne limity kosztów (USD)
    daily_budget_limit: float = 10.0
    weekly_budget_limit: float = 50.0
    monthly_budget_limit: float = 200.0
    
    # Koszt per request (orientacyjnie)
    cost_per_request: float = 0.02
    
    # Alerty budżetowe
    daily_warning_threshold: float = 0.8    # 80% dziennego budżetu
    emergency_stop_threshold: float = 0.95  # 95% dziennego budżetu
    
    # Max requesty dziennie
    max_daily_requests: int = 500
    max_hourly_requests: int = 50
    
    # Tryb oszczędnościowy
    economy_mode_threshold: float = 0.7     # Włącz tryb oszczędny przy 70% budżetu

@dataclass
class SleepConfig:
    """Konfiguracja snu i odpoczynku"""
    # Godziny snu (format HH:MM)
    deep_sleep_start: str = "01:00"
    deep_sleep_end: str = "07:00"
    
    # Lekki sen / mniejsza aktywność
    light_sleep_start: str = "23:00"
    light_sleep_end: str = "08:00"
    
    # Częstotliwość aktywności podczas snu
    deep_sleep_activity_multiplier: float = 0.0      # Brak aktywności
    light_sleep_activity_multiplier: float = 0.1     # 10% normalnej aktywności
    
    # Automatyczne zasypianie przy niskiej energii
    auto_sleep_energy_threshold: float = 0.2
    
    # Czas regeneracji energii podczas snu (per godzinę)
    energy_regeneration_rate: float = 0.15

@dataclass
class APIConfig:
    """Konfiguracja API"""
    # Anthropic Claude
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    anthropic_max_tokens: int = 4000
    anthropic_temperature: float = 0.7
    
    # Slack
    slack_bot_token: str = ""
    slack_app_token: str = ""
    slack_channel_id: str = ""
    slack_user_id: str = ""  # Piotr's ID
    
    # Rate limiting
    api_rate_limit_per_minute: int = 30
    api_timeout_seconds: int = 30

@dataclass
class PersonalityConfig:
    """Parametry osobowości"""
    # Parametry Big Five (0.0 - 1.0)
    openness: float = 0.9        # Otwartość na doświadczenia
    conscientiousness: float = 0.7  # Sumienność
    extraversion: float = 0.8    # Ekstrawersja
    agreeableness: float = 0.8   # Ugodowość
    neuroticism: float = 0.3     # Neurotyczność
    
    # Specjalne cechy Eden
    innocence_level: float = 0.9     # Poziom niewinności
    curiosity_drive: float = 0.95    # Napęd ciekawości
    loyalty_to_creator: float = 1.0  # Lojalność wobec Piotra
    
    # Adaptacyjność osobowości
    personality_evolution_rate: float = 0.02  # Jak szybko się zmienia

class EdenConfig:
    """Główna klasa konfiguracji Eden"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        
        # Inicjalizacja wszystkich kategorii
        self.mood = MoodConfig()
        self.dopamine = DopamineConfig()
        self.economic = EconomicConfig()
        self.sleep = SleepConfig()
        self.api = APIConfig()
        self.personality = PersonalityConfig()
        
        # Załaduj konfigurację z pliku jeśli istnieje
        self.load_config()
        
        # Załaduj zmienne środowiskowe
        self.load_environment_variables()
    
    def _get_default_config_path(self) -> str:
        """Pobierz domyślną ścieżkę do pliku konfiguracyjnego"""
        return os.path.join(os.path.dirname(__file__), "eden_config.json")
    
    def load_environment_variables(self):
        """Załaduj kluczowe zmienne z środowiska"""
        self.api.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", self.api.anthropic_api_key)
        self.api.slack_bot_token = os.getenv("SLACK_BOT_TOKEN", self.api.slack_bot_token)
        self.api.slack_app_token = os.getenv("SLACK_APP_TOKEN", self.api.slack_app_token)
        self.api.slack_channel_id = os.getenv("SLACK_CHANNEL_ID", self.api.slack_channel_id)
        self.api.slack_user_id = os.getenv("SLACK_USER_ID", self.api.slack_user_id)
    
    def load_config(self):
        """Załaduj konfigurację z pliku JSON"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Załaduj każdą sekcję
                if 'mood' in data:
                    self._update_dataclass(self.mood, data['mood'])
                if 'dopamine' in data:
                    self._update_dataclass(self.dopamine, data['dopamine'])
                if 'economic' in data:
                    self._update_dataclass(self.economic, data['economic'])
                if 'sleep' in data:
                    self._update_dataclass(self.sleep, data['sleep'])
                if 'api' in data:
                    self._update_dataclass(self.api, data['api'])
                if 'personality' in data:
                    self._update_dataclass(self.personality, data['personality'])
                    
            except Exception as e:
                print(f"⚠️ Błąd ładowania konfiguracji: {e}")
    
    def save_config(self):
        """Zapisz konfigurację do pliku JSON"""
        try:
            config_data = {
                'mood': self._dataclass_to_dict(self.mood),
                'dopamine': self._dataclass_to_dict(self.dopamine),
                'economic': self._dataclass_to_dict(self.economic),
                'sleep': self._dataclass_to_dict(self.sleep),
                'api': self._dataclass_to_dict(self.api),
                'personality': self._dataclass_to_dict(self.personality),
                'last_updated': datetime.now().isoformat()
            }
            
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️ Błąd zapisywania konfiguracji: {e}")
    
    def _update_dataclass(self, dataclass_instance, data_dict):
        """Aktualizuj dataclass z dictionary"""
        for key, value in data_dict.items():
            if hasattr(dataclass_instance, key):
                setattr(dataclass_instance, key, value)
    
    def _dataclass_to_dict(self, dataclass_instance) -> dict:
        """Konwertuj dataclass do dictionary"""
        result = {}
        for field_name in dataclass_instance.__dataclass_fields__:
            value = getattr(dataclass_instance, field_name)
            result[field_name] = value
        return result
    
    def validate_config(self) -> bool:
        """Waliduj konfigurację"""
        errors = []
        
        # Sprawdź API keys
        if not self.api.anthropic_api_key:
            errors.append("Brak Anthropic API Key")
        if not self.api.slack_bot_token:
            errors.append("Brak Slack Bot Token")
        
        # Sprawdź limity ekonomiczne
        if self.economic.daily_budget_limit <= 0:
            errors.append("Dzienny budżet musi być większy od 0")
        
        # Sprawdź parametry osobowości
        personality_fields = ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']
        for field in personality_fields:
            value = getattr(self.personality, field)
            if not 0.0 <= value <= 1.0:
                errors.append(f"Parametr osobowości {field} musi być między 0.0 a 1.0")
        
        if errors:
            print("❌ Błędy konfiguracji:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        print("✅ Konfiguracja jest prawidłowa")
        return True
    
    def get_current_thinking_speed(self) -> float:
        """Oblicz aktualną szybkość myślenia na podstawie nastroju i dopaminy"""
        # Podstawowa szybkość
        base_speed = 1.0
        
        # Wpływ nastroju (uproszczony)
        mood_score = (self.mood.happiness + self.mood.energy + self.mood.focus) / 3
        if mood_score > 0.8:
            mood_multiplier = self.mood.mood_thinking_multiplier["very_happy"]
        elif mood_score > 0.6:
            mood_multiplier = self.mood.mood_thinking_multiplier["happy"]
        elif mood_score > 0.4:
            mood_multiplier = self.mood.mood_thinking_multiplier["neutral"]
        elif mood_score > 0.2:
            mood_multiplier = self.mood.mood_thinking_multiplier["sad"]
        else:
            mood_multiplier = self.mood.mood_thinking_multiplier["very_sad"]
        
        # Wpływ dopaminy
        dopamine_normalized = self.dopamine.current_level / 100.0
        if dopamine_normalized > 0.8:
            dopamine_multiplier = self.dopamine.high_dopamine_multiplier
        elif dopamine_normalized < 0.3:
            dopamine_multiplier = self.dopamine.low_dopamine_multiplier
        else:
            dopamine_multiplier = 1.0
        
        return base_speed * mood_multiplier * dopamine_multiplier
    
    def is_sleep_time(self) -> bool:
        """Sprawdź czy jest pora snu"""
        now = datetime.now().time()
        
        # Deep sleep
        deep_start = time.fromisoformat(self.sleep.deep_sleep_start)
        deep_end = time.fromisoformat(self.sleep.deep_sleep_end)
        
        if deep_start > deep_end:  # Overnight sleep
            if now >= deep_start or now <= deep_end:
                return True
        else:
            if deep_start <= now <= deep_end:
                return True
        
        return False
    
    def get_activity_multiplier(self) -> float:
        """Pobierz mnożnik aktywności na podstawie pory dnia"""
        now = datetime.now().time()
        
        # Deep sleep
        deep_start = time.fromisoformat(self.sleep.deep_sleep_start)
        deep_end = time.fromisoformat(self.sleep.deep_sleep_end)
        
        # Light sleep
        light_start = time.fromisoformat(self.sleep.light_sleep_start)
        light_end = time.fromisoformat(self.sleep.light_sleep_end)
        
        # Sprawdź deep sleep
        if deep_start > deep_end:  # Overnight
            if now >= deep_start or now <= deep_end:
                return self.sleep.deep_sleep_activity_multiplier
        else:
            if deep_start <= now <= deep_end:
                return self.sleep.deep_sleep_activity_multiplier
        
        # Sprawdź light sleep
        if light_start > light_end:  # Overnight
            if now >= light_start or now <= light_end:
                return self.sleep.light_sleep_activity_multiplier
        else:
            if light_start <= now <= light_end:
                return self.sleep.light_sleep_activity_multiplier
        
        return 1.0  # Pełna aktywność
    
    def update_dopamine(self, trigger: str):
        """Aktualizuj poziom dopaminy na podstawie wyzwalacza"""
        if trigger in self.dopamine.triggers:
            change = self.dopamine.triggers[trigger]
            self.dopamine.current_level = max(
                self.dopamine.min_level,
                min(self.dopamine.max_level, self.dopamine.current_level + change)
            )
            print(f"🧠 Dopamina: {trigger} → {change:+.1f} (teraz: {self.dopamine.current_level:.1f})")
    
    def should_limit_activity(self) -> tuple[bool, str]:
        """Sprawdź czy należy ograniczyć aktywność (budżet, sen, itp.)"""
        # Sprawdź sen
        if self.is_sleep_time():
            return True, "sleep_time"
        
        # Sprawdź budżet (tu byłaby logika sprawdzania rzeczywistych kosztów)
        # To byłoby zintegrowane z systemem śledzenia kosztów
        
        # Sprawdź niską energię
        if self.mood.energy < self.sleep.auto_sleep_energy_threshold:
            return True, "low_energy"
        
        return False, ""

# Globalna instancja konfiguracji
config = EdenConfig()

def get_config() -> EdenConfig:
    """Pobierz globalną konfigurację"""
    return config

def reload_config():
    """Przeładuj konfigurację"""
    global config
    config = EdenConfig()
    return config 