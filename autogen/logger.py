import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
from loguru import logger as loguru_logger

from config import config

class LoggerSetup:
    """Klasa do konfiguracji systemu logowania"""
    
    def __init__(self):
        self.log_file = config.logs_dir / config.log_file
        self.log_level = config.log_level
        self.setup_loguru()
        
    def setup_loguru(self):
        """Konfiguruje loguru jako główny system logowania"""
        # Usunięcie domyślnego handlera
        loguru_logger.remove()
        
        # Konfiguracja formatowania
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
        
        # Handler dla konsoli
        loguru_logger.add(
            sys.stderr,
            format=log_format,
            level=self.log_level,
            colorize=True,
            backtrace=True,
            diagnose=True
        )
        
        # Handler dla pliku
        loguru_logger.add(
            self.log_file,
            format=log_format,
            level=self.log_level,
            rotation="10 MB",
            retention="30 days",
            compression="zip",
            backtrace=True,
            diagnose=True
        )
        
        # Handler dla błędów krytycznych (osobny plik)
        critical_log_file = config.logs_dir / "critical.log"
        loguru_logger.add(
            critical_log_file,
            format=log_format,
            level="ERROR",
            rotation="5 MB",
            retention="90 days",
            compression="zip",
            backtrace=True,
            diagnose=True
        )
        
        loguru_logger.info(f"🔧 System logowania skonfigurowany - poziom: {self.log_level}")
        loguru_logger.info(f"📁 Logi zapisywane do: {self.log_file}")

class InterceptHandler(logging.Handler):
    """Handler łączący standardowe logowanie z loguru"""
    
    def emit(self, record):
        # Pobranie odpowiedniej ramki stosu
        try:
            level = loguru_logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        
        loguru_logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

def setup_logger(name: str) -> loguru_logger:
    """
    Konfiguruje logger dla konkretnego modułu
    
    Args:
        name: Nazwa modułu/loggera
        
    Returns:
        Skonfigurowany logger
    """
    # Inicjalizacja systemu logowania jeśli nie został jeszcze zainicjalizowany
    if not hasattr(setup_logger, '_initialized'):
        LoggerSetup()
        setup_logger._initialized = True
        
        # Przekierowanie standardowego logowania do loguru
        logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
        
        # Wyłączenie logowania SQLAlchemy w produkcji
        if not config.debug:
            logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
            logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    
    return loguru_logger.bind(name=name)

def log_performance(func_name: str, duration: float, extra_info: Optional[dict] = None):
    """
    Loguje informacje o wydajności funkcji
    
    Args:
        func_name: Nazwa funkcji
        duration: Czas wykonania w sekundach
        extra_info: Dodatkowe informacje do logowania
    """
    logger = setup_logger("performance")
    
    message = f"⏱️  {func_name} wykonano w {duration:.3f}s"
    
    if extra_info:
        message += f" | {extra_info}"
    
    if duration > 1.0:
        logger.warning(message)
    else:
        logger.info(message)

def log_agent_activity(agent_id: int, agent_name: str, activity: str, details: Optional[dict] = None):
    """
    Loguje aktywność agenta
    
    Args:
        agent_id: ID agenta
        agent_name: Nazwa agenta
        activity: Typ aktywności
        details: Szczegóły aktywności
    """
    logger = setup_logger("agent_activity")
    
    message = f"🤖 Agent {agent_name} (ID: {agent_id}) - {activity}"
    
    if details:
        message += f" | {details}"
    
    logger.info(message)

def log_consciousness_integration(event_type: str, success: bool, details: Optional[dict] = None):
    """
    Loguje integrację z systemem świadomości
    
    Args:
        event_type: Typ wydarzenia
        success: Czy operacja zakończyła się sukcesem
        details: Szczegóły operacji
    """
    logger = setup_logger("consciousness_integration")
    
    status = "✅ Sukces" if success else "❌ Błąd"
    message = f"🧠 Integracja ze świadomością - {event_type} - {status}"
    
    if details:
        message += f" | {details}"
    
    if success:
        logger.info(message)
    else:
        logger.error(message)

def log_system_event(event_type: str, message: str, level: str = "INFO"):
    """
    Loguje wydarzenie systemowe
    
    Args:
        event_type: Typ wydarzenia
        message: Treść wiadomości
        level: Poziom logowania
    """
    logger = setup_logger("system_events")
    
    formatted_message = f"🔄 {event_type} - {message}"
    
    level_map = {
        "DEBUG": logger.debug,
        "INFO": logger.info,
        "WARNING": logger.warning,
        "ERROR": logger.error,
        "CRITICAL": logger.critical
    }
    
    log_func = level_map.get(level.upper(), logger.info)
    log_func(formatted_message)

def log_database_operation(operation: str, table: str, success: bool, details: Optional[dict] = None):
    """
    Loguje operację na bazie danych
    
    Args:
        operation: Typ operacji (CREATE, READ, UPDATE, DELETE)
        table: Nazwa tabeli
        success: Czy operacja zakończyła się sukcesem
        details: Szczegóły operacji
    """
    logger = setup_logger("database")
    
    status = "✅" if success else "❌"
    message = f"🗄️  {status} {operation} - {table}"
    
    if details:
        message += f" | {details}"
    
    if success:
        logger.debug(message)
    else:
        logger.error(message)

def log_api_request(method: str, endpoint: str, status_code: int, duration: float, user_agent: Optional[str] = None):
    """
    Loguje żądanie API
    
    Args:
        method: Metoda HTTP
        endpoint: Endpoint API
        status_code: Kod statusu odpowiedzi
        duration: Czas odpowiedzi
        user_agent: User agent klienta
    """
    logger = setup_logger("api_requests")
    
    status_emoji = "✅" if status_code < 400 else "❌"
    message = f"🌐 {status_emoji} {method} {endpoint} - {status_code} ({duration:.3f}s)"
    
    if user_agent:
        message += f" | UA: {user_agent}"
    
    if status_code >= 400:
        logger.warning(message)
    else:
        logger.info(message)

class AutoGenLogger:
    """Główna klasa loggera dla AutoGen"""
    
    def __init__(self, name: str = "autogen"):
        self.logger = setup_logger(name)
        self.start_time = datetime.now()
    
    def info(self, message: str, **kwargs):
        """Loguje informację"""
        self.logger.info(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Loguje ostrzeżenie"""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Loguje błąd"""
        self.logger.error(message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Loguje błąd krytyczny"""
        self.logger.critical(message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Loguje informację debug"""
        self.logger.debug(message, **kwargs)
    
    def log_startup(self):
        """Loguje uruchomienie systemu"""
        self.logger.info("🚀 Adam Clay AutoGen Subconscious Service - Starting...")
        self.logger.info(f"📊 Konfiguracja: {config.service_name} v{config.version}")
        self.logger.info(f"🌐 API będzie dostępne na: http://{config.host}:{config.port}")
    
    def log_shutdown(self):
        """Loguje zamknięcie systemu"""
        uptime = datetime.now() - self.start_time
        self.logger.info(f"🛑 Zamykanie systemu - Uptime: {uptime}")
        self.logger.info("✅ System zamknięty pomyślnie")

# Eksport głównych funkcji
__all__ = [
    'setup_logger',
    'log_performance',
    'log_agent_activity',
    'log_consciousness_integration',
    'log_system_event',
    'log_database_operation',
    'log_api_request',
    'AutoGenLogger'
] 