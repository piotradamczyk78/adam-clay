import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import openai
import autogen
from autogen.agentchat import ConversableAgent, UserProxyAgent, GroupChat, GroupChatManager

from database import get_db
from models import (
    SubconsciousAgent, AgentConversation, SystemEvent, AgentMemory,
    AgentStatus, AgentType, AgentInteraction, AgentStatistics
)
from config import config
from logger import setup_logger, log_agent_activity, log_performance
from schemas import AgentStatisticsResponse

logger = setup_logger("agent_manager")

class AutoGenAgent:
    """Wrapper dla agentów AutoGen zintegrowanych z bazą danych"""
    
    def __init__(self, db_agent: SubconsciousAgent):
        self.db_agent = db_agent
        self.autogen_agent = None
        self.conversation_history = []
        self.is_active = False
        self.last_activity = datetime.now()
        self.setup_autogen_agent()
    
    def setup_autogen_agent(self):
        """Konfiguruje agenta AutoGen na podstawie danych z bazy"""
        try:
            # Przygotowanie konfiguracji modelu
            model_config = self.db_agent.model_config or {
                "model": "gpt-4-turbo-preview",
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            # Tworzenie agenta AutoGen
            self.autogen_agent = ConversableAgent(
                name=self.db_agent.name,
                system_message=self._build_system_message(),
                llm_config={
                    "config_list": [{
                        "model": model_config.get("model", "gpt-4-turbo-preview"),
                        "api_key": config.openai_api_key,
                        "temperature": model_config.get("temperature", 0.7),
                        "max_tokens": model_config.get("max_tokens", 1000)
                    }]
                },
                human_input_mode="NEVER",
                max_consecutive_auto_reply=3,
                is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE")
            )
            
            logger.info(f"Skonfigurowano agenta AutoGen: {self.db_agent.name}")
            
        except Exception as e:
            logger.error(f"Błąd konfiguracji agenta {self.db_agent.name}: {str(e)}")
    
    def _build_system_message(self) -> str:
        """Buduje system message dla agenta na podstawie jego charakterystyki"""
        base_message = f"""
Jesteś {self.db_agent.name}, podświadomy agent w systemie psychiki Adam Clay.

TWOJA ROLA: {self.db_agent.agent_type.value}
OPIS: {self.db_agent.description or "Brak opisu"}

CECHY OSOBOWOŚCI:
{json.dumps(self.db_agent.personality_traits or {}, indent=2)}

UMIEJĘTNOŚCI:
{json.dumps(self.db_agent.skills or {}, indent=2)}

ODPOWIEDZIALNOŚCI:
{json.dumps(self.db_agent.responsibilities or {}, indent=2)}

INSTRUKCJE SYSTEMOWE:
{self.db_agent.system_prompt or "Działaj zgodnie ze swoją rolą i charakterystyką."}

ZASADY KOMUNIKACJI:
1. Odpowiadaj w języku polskim
2. Bądź autentyczny dla swojej roli
3. Uwzględniaj kontekst psychiki Adam Clay
4. Kończ odpowiedź słowem "TERMINATE" gdy zadanie jest zakończone
5. Współpracuj z innymi agentami gdy jest to potrzebne

STAN AKTYWNOŚCI: {self.db_agent.current_activity_level}
PRIORYTET: {self.db_agent.priority_level}/10
"""
        
        return base_message.strip()
    
    async def activate(self):
        """Aktywuje agenta"""
        self.is_active = True
        self.last_activity = datetime.now()
        log_agent_activity(self.db_agent.id, self.db_agent.name, "AKTIVATED")
    
    async def deactivate(self):
        """Deaktywuje agenta"""
        self.is_active = False
        log_agent_activity(self.db_agent.id, self.db_agent.name, "DEACTIVATED")
    
    async def process_event(self, event: SystemEvent) -> Optional[str]:
        """Przetwarza wydarzenie systemowe"""
        if not self.is_active:
            return None
        
        try:
            # Sprawdzenie czy agent powinien reagować na to wydarzenie
            if not self._should_respond_to_event(event):
                return None
            
            # Przygotowanie kontekstu
            context = self._prepare_context(event)
            
            # Generowanie odpowiedzi
            response = await self._generate_response(context)
            
            # Zapisanie do historii
            self.conversation_history.append({
                "event_id": event.id,
                "timestamp": datetime.now(),
                "context": context,
                "response": response
            })
            
            # Aktualizacja aktywności
            self.last_activity = datetime.now()
            
            log_agent_activity(
                self.db_agent.id, 
                self.db_agent.name, 
                "PROCESSED_EVENT",
                {"event_type": event.event_type, "response_length": len(response) if response else 0}
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Błąd przetwarzania wydarzenia przez agenta {self.db_agent.name}: {str(e)}")
            return None
    
    def _should_respond_to_event(self, event: SystemEvent) -> bool:
        """Sprawdza czy agent powinien reagować na wydarzenie"""
        # Sprawdzenie priorytetu
        if event.priority > self.db_agent.priority_level:
            return False
        
        # Sprawdzenie typu agenta i wydarzenia
        event_type = event.event_type.lower()
        agent_type = self.db_agent.agent_type.value.lower()
        
        # Mapowanie typów wydarzeń do typów agentów
        event_agent_mapping = {
            "consciousness_thought": ["analytical", "creative", "intuitive"],
            "email_received": ["social", "analytical", "guardian"],
            "system_error": ["guardian", "analytical"],
            "emotional_state_change": ["emotional", "intuitive"],
            "memory_significant": ["memory", "analytical"],
            "creative_inspiration": ["creative", "intuitive"],
            "social_interaction": ["social", "emotional"]
        }
        
        relevant_agents = event_agent_mapping.get(event_type, [])
        
        return agent_type in relevant_agents or self.db_agent.priority_level >= 8
    
    def _prepare_context(self, event: SystemEvent) -> str:
        """Przygotowuje kontekst dla agenta"""
        context = f"""
WYDARZENIE: {event.event_type}
ŹRÓDŁO: {event.source}
TREŚĆ: {json.dumps(event.content, indent=2)}
PRIORYTET: {event.priority}/10
CZAS: {event.created_at}

TWÓJ KONTEKST:
- Typ agenta: {self.db_agent.agent_type.value}
- Poziom aktywności: {self.db_agent.current_activity_level}
- Ostatnie działania: {len(self.conversation_history)} w historii

Przeanalizuj to wydarzenie z perspektywy swojej roli i zaproponuj odpowiedź lub działanie.
"""
        return context.strip()
    
    async def _generate_response(self, context: str) -> str:
        """Generuje odpowiedź używając AutoGen"""
        try:
            # Tworzenie proxy agenta dla interakcji
            user_proxy = UserProxyAgent(
                name="system_proxy",
                human_input_mode="NEVER",
                max_consecutive_auto_reply=0,
                is_termination_msg=lambda x: True
            )
            
            # Inicjalizacja czatu
            user_proxy.initiate_chat(
                self.autogen_agent,
                message=context,
                max_turns=1
            )
            
            # Pobranie ostatniej odpowiedzi
            if self.autogen_agent.last_message():
                response = self.autogen_agent.last_message().get("content", "")
                return response.replace("TERMINATE", "").strip()
            
            return ""
            
        except Exception as e:
            logger.error(f"Błąd generowania odpowiedzi: {str(e)}")
            return ""

class AgentManager:
    """Główny manager agentów podświadomych"""
    
    def __init__(self):
        self.agents: Dict[int, AutoGenAgent] = {}
        self.group_chat_manager = None
        self.statistics = {}
        self.start_time = datetime.now()
        
    async def load_agents(self):
        """Ładuje agentów z bazy danych"""
        try:
            with get_db() as db:
                db_agents = db.query(SubconsciousAgent).all()
                
                for db_agent in db_agents:
                    agent = AutoGenAgent(db_agent)
                    self.agents[db_agent.id] = agent
                    
                    # Aktywacja agenta jeśli ma status aktywny
                    if db_agent.status == AgentStatus.ACTIVE:
                        await agent.activate()
                
                logger.info(f"Załadowano {len(self.agents)} agentów")
                
                # Inicjalizacja group chat jeśli są aktywni agenci
                await self._setup_group_chat()
                
        except Exception as e:
            logger.error(f"Błąd ładowania agentów: {str(e)}")
    
    async def _setup_group_chat(self):
        """Konfiguruje group chat dla współpracy agentów"""
        try:
            active_agents = [agent for agent in self.agents.values() if agent.is_active]
            
            if len(active_agents) < 2:
                logger.info("Zbyt mało aktywnych agentów do utworzenia group chat")
                return
            
            # Tworzenie group chat
            autogen_agents = [agent.autogen_agent for agent in active_agents]
            
            groupchat = GroupChat(
                agents=autogen_agents,
                messages=[],
                max_round=10,
                speaker_selection_method="round_robin"
            )
            
            self.group_chat_manager = GroupChatManager(
                groupchat=groupchat,
                llm_config={
                    "config_list": [{
                        "model": "gpt-4-turbo-preview",
                        "api_key": config.openai_api_key,
                        "temperature": 0.3,
                        "max_tokens": 500
                    }]
                }
            )
            
            logger.info(f"Skonfigurowano group chat z {len(active_agents)} agentami")
            
        except Exception as e:
            logger.error(f"Błąd konfiguracji group chat: {str(e)}")
    
    async def add_agent(self, db_agent: SubconsciousAgent):
        """Dodaje nowego agenta"""
        try:
            agent = AutoGenAgent(db_agent)
            self.agents[db_agent.id] = agent
            
            if db_agent.status == AgentStatus.ACTIVE:
                await agent.activate()
            
            # Rekonfiguracja group chat
            await self._setup_group_chat()
            
            logger.info(f"Dodano agenta: {db_agent.name}")
            
        except Exception as e:
            logger.error(f"Błąd dodawania agenta: {str(e)}")
    
    async def activate_agent(self, agent_id: int):
        """Aktywuje agenta"""
        if agent_id in self.agents:
            await self.agents[agent_id].activate()
            
            # Aktualizacja w bazie danych
            with get_db() as db:
                db_agent = db.query(SubconsciousAgent).filter(SubconsciousAgent.id == agent_id).first()
                if db_agent:
                    db_agent.status = AgentStatus.ACTIVE
                    db_agent.last_active_at = datetime.now()
                    db.commit()
            
            await self._setup_group_chat()
    
    async def deactivate_agent(self, agent_id: int):
        """Deaktywuje agenta"""
        if agent_id in self.agents:
            await self.agents[agent_id].deactivate()
            
            # Aktualizacja w bazie danych
            with get_db() as db:
                db_agent = db.query(SubconsciousAgent).filter(SubconsciousAgent.id == agent_id).first()
                if db_agent:
                    db_agent.status = AgentStatus.INACTIVE
                    db.commit()
            
            await self._setup_group_chat()
    
    async def update_agent_status(self, agent_id: int, status: AgentStatus):
        """Aktualizuje status agenta"""
        if status == AgentStatus.ACTIVE:
            await self.activate_agent(agent_id)
        elif status == AgentStatus.INACTIVE:
            await self.deactivate_agent(agent_id)
    
    async def process_event(self, event: SystemEvent):
        """Przetwarza wydarzenie przez wszystkich aktywnych agentów"""
        start_time = datetime.now()
        
        try:
            responses = {}
            
            # Przetwarzanie przez poszczególnych agentów
            for agent_id, agent in self.agents.items():
                if agent.is_active:
                    response = await agent.process_event(event)
                    if response:
                        responses[agent_id] = response
            
            # Zapisanie odpowiedzi w bazie danych
            with get_db() as db:
                event_from_db = db.query(SystemEvent).filter(SystemEvent.id == event.id).first()
                if event_from_db:
                    event_from_db.processed_by_agents = list(responses.keys())
                    event_from_db.responses = responses
                    event_from_db.processed_at = datetime.now()
                    event_from_db.status = "processed"
                    db.commit()
            
            # Logowanie wydajności
            duration = (datetime.now() - start_time).total_seconds()
            log_performance(
                "process_event",
                duration,
                {"event_type": event.event_type, "agents_responded": len(responses)}
            )
            
            logger.info(f"Przetworzono wydarzenie {event.event_type} przez {len(responses)} agentów")
            
        except Exception as e:
            logger.error(f"Błąd przetwarzania wydarzenia: {str(e)}")
    
    async def facilitate_agent_interaction(self, agent_ids: List[int], topic: str):
        """Ułatwia interakcję między agentami"""
        try:
            if len(agent_ids) < 2:
                logger.warning("Potrzeba co najmniej 2 agentów do interakcji")
                return
            
            # Pobieranie agentów
            participating_agents = [self.agents[aid] for aid in agent_ids if aid in self.agents and self.agents[aid].is_active]
            
            if len(participating_agents) < 2:
                logger.warning("Niewystarczająca liczba aktywnych agentów")
                return
            
            # Tworzenie group chat dla interakcji
            autogen_agents = [agent.autogen_agent for agent in participating_agents]
            
            groupchat = GroupChat(
                agents=autogen_agents,
                messages=[],
                max_round=6,
                speaker_selection_method="auto"
            )
            
            manager = GroupChatManager(
                groupchat=groupchat,
                llm_config={
                    "config_list": [{
                        "model": "gpt-4-turbo-preview",
                        "api_key": config.openai_api_key,
                        "temperature": 0.4,
                        "max_tokens": 800
                    }]
                }
            )
            
            # Inicjalizacja dyskusji
            first_agent = participating_agents[0]
            first_agent.autogen_agent.initiate_chat(
                manager,
                message=f"Temat do dyskusji: {topic}. Proszę o analizę z perspektywy waszych ról.",
                max_turns=10
            )
            
            logger.info(f"Ułatwiono interakcję między {len(participating_agents)} agentami na temat: {topic}")
            
        except Exception as e:
            logger.error(f"Błąd ułatwiania interakcji: {str(e)}")
    
    def get_active_agents(self) -> List[AutoGenAgent]:
        """Zwraca listę aktywnych agentów"""
        return [agent for agent in self.agents.values() if agent.is_active]
    
    async def get_agent_statistics(self, agent_id: int) -> Optional[AgentStatisticsResponse]:
        """Pobiera statystyki agenta"""
        try:
            if agent_id not in self.agents:
                return None
            
            agent = self.agents[agent_id]
            
            # Obliczanie statystyk
            total_interactions = len(agent.conversation_history)
            successful_interactions = sum(1 for conv in agent.conversation_history if conv.get("response"))
            success_rate = successful_interactions / total_interactions if total_interactions > 0 else 0
            
            return AgentStatisticsResponse(
                agent_id=agent_id,
                period_start=self.start_time,
                period_end=datetime.now(),
                total_interactions=total_interactions,
                successful_interactions=successful_interactions,
                success_rate=success_rate,
                average_response_time=None,  # TODO: Implementować pomiar czasu odpowiedzi
                average_confidence=None,     # TODO: Implementować ocenę pewności
                user_satisfaction=None,     # TODO: Implementować ocenę użytkowników
                knowledge_growth=None,      # TODO: Implementować pomiar wzrostu wiedzy
                adaptation_rate=None        # TODO: Implementować pomiar adaptacji
            )
            
        except Exception as e:
            logger.error(f"Błąd pobierania statystyk: {str(e)}")
            return None
    
    async def health_check(self):
        """Sprawdza stan zdrowia agentów"""
        try:
            current_time = datetime.now()
            
            for agent_id, agent in self.agents.items():
                if agent.is_active:
                    # Sprawdzenie czy agent nie jest bezczynny zbyt długo
                    if current_time - agent.last_activity > timedelta(hours=1):
                        logger.warning(f"Agent {agent.db_agent.name} jest bezczynny od {agent.last_activity}")
                        
                        # Aktualizacja poziomu aktywności
                        agent.db_agent.current_activity_level = max(0, agent.db_agent.current_activity_level - 0.1)
            
            logger.debug("Sprawdzenie stanu zdrowia agentów zakończone")
            
        except Exception as e:
            logger.error(f"Błąd sprawdzania stanu zdrowia: {str(e)}")
    
    async def shutdown(self):
        """Zamyka wszystkich agentów"""
        try:
            for agent in self.agents.values():
                await agent.deactivate()
            
            self.agents.clear()
            self.group_chat_manager = None
            
            logger.info("Wszyscy agenci zostali wyłączeni")
            
        except Exception as e:
            logger.error(f"Błąd zamykania agentów: {str(e)}") 