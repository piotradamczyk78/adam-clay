from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
from typing import Generator
import logging

from config import config
from models import Base

logger = logging.getLogger(__name__)

# Konfiguracja bazy danych
DATABASE_URL = f"mysql+pymysql://{config.database.username}:{config.database.password}@{config.database.host}:{config.database.port}/{config.database.database}"

# Tworzenie silnika bazy danych
engine = create_engine(
    DATABASE_URL,
    echo=config.debug,  # Logowanie zapytań SQL w trybie debug
    pool_pre_ping=True,  # Sprawdzanie połączeń przed użyciem
    pool_recycle=3600,  # Odnawianie połączeń co godzinę
    pool_size=10,  # Maksymalna liczba połączeń w puli
    max_overflow=20,  # Maksymalna liczba dodatkowych połączeń
    connect_args={
        "charset": "utf8mb4",
        "init_command": "SET sql_mode='STRICT_TRANS_TABLES'"
    }
)

# Tworzenie sesji
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def init_db():
    """Inicjalizuje bazę danych - tworzy tabele"""
    try:
        logger.info("🗄️  Inicjalizacja bazy danych...")
        
        # Sprawdzenie połączenia
        with engine.connect() as connection:
            logger.info("✅ Połączenie z bazą danych nawiązane")
        
        # Tworzenie tabel
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tabele bazy danych utworzone/zaktualizowane")
        
        # Sprawdzenie czy są jakieś agenci
        with get_db() as db:
            from models import SubconsciousAgent
            agents_count = db.query(SubconsciousAgent).count()
            logger.info(f"📊 Liczba agentów w bazie: {agents_count}")
            
    except Exception as e:
        logger.error(f"❌ Błąd podczas inicjalizacji bazy danych: {str(e)}")
        raise

@contextmanager
def get_db() -> Generator[Session, None, None]:
    """Generuje sesję bazy danych z automatycznym zamknięciem"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def get_db_dependency() -> Generator[Session, None, None]:
    """Dependency injection dla FastAPI"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database dependency error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

# Test połączenia z bazą danych
def test_database_connection():
    """Testuje połączenie z bazą danych"""
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
            logger.info("✅ Test połączenia z bazą danych zakończony sukcesem")
            return True
    except Exception as e:
        logger.error(f"❌ Test połączenia z bazą danych nieudany: {str(e)}")
        return False

# Funkcje pomocnicze dla zarządzania bazą danych
def reset_database():
    """Resetuje bazę danych - usuwa wszystkie tabele i tworzy je ponownie"""
    logger.warning("🔄 Resetowanie bazy danych...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Baza danych zresetowana")

def get_database_stats():
    """Pobiera statystyki bazy danych"""
    try:
        with get_db() as db:
            from models import SubconsciousAgent, AgentConversation, SystemEvent, AgentMemory
            
            stats = {
                "agents": db.query(SubconsciousAgent).count(),
                "conversations": db.query(AgentConversation).count(),
                "events": db.query(SystemEvent).count(),
                "memories": db.query(AgentMemory).count()
            }
            
            return stats
    except Exception as e:
        logger.error(f"Error getting database stats: {str(e)}")
        return None 