from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum as PyEnum
import json

Base = declarative_base()

class AgentStatus(PyEnum):
    """Status agenta podświadomego"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    LEARNING = "learning"
    PROCESSING = "processing"

class AgentType(PyEnum):
    """
    Typ agenta podświadomego
    
    Inspirowane psychologią Junga, teorią wielokrotnej inteligencji Gardnera,
    modelem Big Five oraz filmem Pixara "W głowie się nie mieści".
    
    Każdy typ reprezentuje inny aspekt ludzkiej psychiki i specjalizuje się
    w określonych funkcjach poznawczych i emocjonalnych.
    """
    
    # ❤️ Agent emocjonalny - "Radość" i "Smutek" z filmu Pixara
    # Psychologia: Inteligencja interpersonalna/intrapersonalna (Gardner)
    # Big Five: Wysoka ugodowość, funkcja "Odczuwanie" (Jung)
    EMOTIONAL = "emotional"
    
    # 🔍 Agent analityczny - "Obrzydzenie" z filmu Pixara (filtruje złe pomysły)
    # Psychologia: Inteligencja logiczno-matematyczna (Gardner)
    # Big Five: Wysoka sumienność, funkcja "Myślenie" (Jung)
    ANALYTICAL = "analytical"
    
    # 🎨 Agent kreatywny - Archetyp "Twórcy" (Jung)
    # Psychologia: Inteligencja przestrzenna/muzyczna (Gardner)
    # Big Five: Wysoka otwartość na doświadczenia
    CREATIVE = "creative"
    
    # 👥 Agent społeczny - Archetyp "Niewinnego" (Jung)
    # Psychologia: Inteligencja interpersonalna (Gardner)
    # Big Five: Wysoka ekstrawersja
    SOCIAL = "social"
    
    # 🛡️ Agent strażnik - "Gniew" i "Strach" z filmu Pixara
    # Psychologia: Instynkt samozachowawczy, funkcja ochronna (IFS)
    # Big Five: Neurotyzm jako mechanizm kontroli
    GUARDIAN = "guardian"
    
    # 📚 Agent pamięci - Archetyp "Maga" (Jung)
    # Psychologia: Funkcja organizacyjna umysłu
    # Big Five: Wysoka sumienność, funkcja "Percepcja" (Jung)
    MEMORY = "memory"
    
    # 🎯 Agent strategiczny - Archetyp "Władcy" (Jung)
    # Psychologia: Myślenie długoterminowe, planowanie strategiczne
    # Funkcje wykonawcze mózgu
    STRATEGIC = "strategic"
    
    # 🔮 Agent intuicyjny - "Ja prawdziwe" w IFS, funkcja "Intuicja" (Jung)
    # Psychologia: Archetyp "Odkrywcy", mądrość podświadoma
    # Holistyczne przetwarzanie informacji
    INTUITIVE = "intuitive"

class SubconsciousAgent(Base):
    """
    Model agenta podświadomego Adam Clay
    
    🧠 PSYCHOLOGICZNE PODSTAWY:
    
    Każdy agent reprezentuje wyspecjalizowany aspekt ludzkiej psychiki,
    inspirowany następującymi teoriami:
    
    📚 TEORIA WIELOKROTNEJ INTELIGENCJI (Howard Gardner):
    - Różne typy inteligencji działają niezależnie
    - Każdy agent specjalizuje się w innym typie inteligencji
    
    🎭 JUNGOWSKA PSYCHOLOGIA ANALITYCZNA:
    - Archetypy: Mędrzec, Twórca, Opiekun, Władca, Odkrywca...
    - Funkcje psychiczne: Myślenie, Odczuwanie, Intuicja, Percepcja
    
    🌊 MODEL BIG FIVE (OCEAN):
    - Otwartość, Sumienność, Ekstrawersja, Ugodowość, Neurotyzm
    - Każdy agent ma unikalny profil osobowości
    
    🎬 "W GŁOWIE SIĘ NIE MIEŚCI" (Pixar):
    - Radość, Smutek, Gniew, Strach, Obrzydzenie
    - Każda emocja ma swoją funkcję i mądrość
    
    🔄 TEORIA SYSTEMÓW WEWNĘTRZNYCH (IFS):
    - Różne "części" osobowości współpracują
    - Każda część ma pozytywną intencję
    
    🤖 PRAKTYKA AI:
    - Multi-agent systems przewyższają pojedyncze modele
    - Specjalizacja + współpraca = lepsza wydajność
    - Konflikty między agentami prowadzą do lepszych rozwiązań
    
    💡 DLACZEGO TO DZIAŁA:
    - Mózg ma różne obszary odpowiedzialne za różne funkcje
    - Umysł jest "społecznością umysłów" (Marvin Minsky)
    - Różnorodność perspektyw prowadzi do mądrzejszych decyzji
    """
    __tablename__ = "subconscious_agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    agent_type = Column(Enum(AgentType), nullable=False)
    status = Column(Enum(AgentStatus), default=AgentStatus.ACTIVE)
    
    # Charakterystyka agenta
    description = Column(Text)
    personality_traits = Column(JSON)  # JSON z cechami osobowości
    skills = Column(JSON)  # JSON z umiejętnościami
    responsibilities = Column(JSON)  # JSON z odpowiedzialnościami
    
    # Konfiguracja AI
    system_prompt = Column(Text)
    model_config = Column(JSON)  # Temperatura, max_tokens, itp.
    
    # Parametry aktywności
    activation_threshold = Column(Float, default=0.5)  # Próg aktywacji
    current_activity_level = Column(Float, default=0.0)  # Obecny poziom aktywności
    priority_level = Column(Integer, default=1)  # Priorytet 1-10
    
    # Integracja z Adam Clay
    consciousness_integration = Column(JSON)  # Ustawienia integracji
    
    # Metadane
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_active_at = Column(DateTime)
    
    # Relacje
    conversations = relationship("AgentConversation", back_populates="agent")
    interactions = relationship("AgentInteraction", back_populates="agent", foreign_keys="AgentInteraction.agent_id")
    target_interactions = relationship("AgentInteraction", foreign_keys="AgentInteraction.target_agent_id")
    memories = relationship("AgentMemory", back_populates="agent")

class AgentConversation(Base):
    """Konwersacje agentów z systemem głównym"""
    __tablename__ = "agent_conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("subconscious_agents.id"))
    
    # Kontekst konwersacji
    trigger_event = Column(String(200))  # Co wywołało konwersację
    context = Column(JSON)  # Kontekst sytuacyjny
    
    # Treść konwersacji
    messages = Column(JSON)  # Historia wiadomości
    summary = Column(Text)  # Podsumowanie konwersacji
    
    # Wyniki
    insights = Column(JSON)  # Wnioski z konwersacji
    recommendations = Column(JSON)  # Rekomendacje
    emotional_state = Column(JSON)  # Stan emocjonalny
    
    # Status
    status = Column(String(50), default="active")
    confidence_score = Column(Float)  # Pewność siebie agenta
    
    # Metadane
    started_at = Column(DateTime, default=func.now())
    ended_at = Column(DateTime)
    duration_seconds = Column(Integer)
    
    # Relacje
    agent = relationship("SubconsciousAgent", back_populates="conversations")

class AgentInteraction(Base):
    """Interakcje między agentami"""
    __tablename__ = "agent_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("subconscious_agents.id"))
    target_agent_id = Column(Integer, ForeignKey("subconscious_agents.id"))
    
    # Typ interakcji
    interaction_type = Column(String(100))  # collaboration, conflict, consultation, etc.
    
    # Treść
    content = Column(JSON)  # Treść interakcji
    outcome = Column(JSON)  # Wynik interakcji
    
    # Ocena
    effectiveness_score = Column(Float)  # Skuteczność interakcji
    harmony_score = Column(Float)  # Harmonia między agentami
    
    # Metadane
    created_at = Column(DateTime, default=func.now())
    
    # Relacje
    agent = relationship("SubconsciousAgent", back_populates="interactions", foreign_keys=[agent_id])
    target_agent = relationship("SubconsciousAgent", foreign_keys=[target_agent_id])

class AgentMemory(Base):
    """Pamięć agentów podświadomych"""
    __tablename__ = "agent_memory"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("subconscious_agents.id"))
    
    # Typ pamięci
    memory_type = Column(String(100))  # episodic, semantic, procedural
    
    # Treść
    content = Column(Text)
    agent_metadata = Column(JSON)  # Dodatkowe metadane
    
    # Klasyfikacja
    importance_score = Column(Float)  # Ważność pamięci
    emotional_weight = Column(Float)  # Waga emocjonalna
    tags = Column(JSON)  # Tagi do wyszukiwania
    
    # Powiązania
    related_memories = Column(JSON)  # Powiązane wspomnienia
    consciousness_link = Column(String(200))  # Link do głównej świadomości
    
    # Metadane
    created_at = Column(DateTime, default=func.now())
    accessed_at = Column(DateTime)
    access_count = Column(Integer, default=0)
    
    # Relacje
    agent = relationship("SubconsciousAgent", back_populates="memories")

class SystemEvent(Base):
    """Wydarzenia systemowe i triggery"""
    __tablename__ = "system_events"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Typ wydarzenia
    event_type = Column(String(100))  # consciousness_thought, email_received, etc.
    
    # Treść
    content = Column(JSON)
    source = Column(String(200))  # Skąd pochodzi wydarzenie
    
    # Przetwarzanie
    processed_by_agents = Column(JSON)  # Którzy agenci przetworzyli
    responses = Column(JSON)  # Odpowiedzi agentów
    
    # Status
    status = Column(String(50), default="pending")
    priority = Column(Integer, default=1)
    
    # Metadane
    created_at = Column(DateTime, default=func.now())
    processed_at = Column(DateTime)
    
class AgentStatistics(Base):
    """Statystyki działania agentów"""
    __tablename__ = "agent_statistics"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("subconscious_agents.id"))
    
    # Okres statystyk
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    
    # Metryki aktywności
    total_interactions = Column(Integer, default=0)
    successful_interactions = Column(Integer, default=0)
    average_response_time = Column(Float)
    
    # Metryki jakości
    average_confidence = Column(Float)
    user_satisfaction = Column(Float)
    
    # Metryki uczenia się
    knowledge_growth = Column(Float)
    adaptation_rate = Column(Float)
    
    # Metadane
    created_at = Column(DateTime, default=func.now())

# Funkcje pomocnicze
def get_agent_by_name(db: Session, name: str) -> Optional[SubconsciousAgent]:
    """Pobiera agenta po nazwie"""
    return db.query(SubconsciousAgent).filter(SubconsciousAgent.name == name).first()

def get_active_agents(db: Session) -> List[SubconsciousAgent]:
    """Pobiera wszystkich aktywnych agentów"""
    return db.query(SubconsciousAgent).filter(SubconsciousAgent.status == AgentStatus.ACTIVE).all()

def create_agent_conversation(db: Session, agent_id: int, trigger_event: str, context: Dict[str, Any]) -> AgentConversation:
    """Tworzy nową konwersację agenta"""
    conversation = AgentConversation(
        agent_id=agent_id,
        trigger_event=trigger_event,
        context=context,
        messages=[],
        status="active"
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation 