import asyncio
import json
import aiohttp
import websockets
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass

from config import config
from database import get_db
from models import SystemEvent, SubconsciousAgent, AgentStatus
from logger import setup_logger, log_consciousness_integration
from schemas import ConsciousnessEventCreate, ConsciousnessResponse

logger = setup_logger("consciousness_integration")

@dataclass
class ConsciousnessEvent:
    """Struktura wydarzenia ze świadomości"""
    event_type: str
    content: Dict[str, Any]
    timestamp: datetime
    source: str
    priority: int = 1
    requires_response: bool = False

class ConsciousnessIntegration:
    """Klasa integrująca system podświadomych agentów z głównym systemem świadomości"""
    
    def __init__(self):
        self.is_connected = False
        self.websocket_connection = None
        self.last_sync = None
        self.session = None
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 10
        self.reconnect_delay = 5  # seconds
        
    async def start(self):
        """Rozpoczyna integrację z systemem świadomości"""
        try:
            logger.info("🧠 Rozpoczynanie integracji z systemem świadomości Adam Clay")
            
            # Tworzenie sesji HTTP
            self.session = aiohttp.ClientSession()
            
            # Próba nawiązania połączenia
            await self._connect_to_consciousness()
            
            # Uruchomienie nasłuchu w tle
            asyncio.create_task(self._listen_to_consciousness())
            
            logger.info("✅ Integracja z systemem świadomości uruchomiona")
            
        except Exception as e:
            logger.error(f"❌ Błąd uruchamiania integracji: {str(e)}")
            log_consciousness_integration("START", False, {"error": str(e)})
    
    async def _connect_to_consciousness(self):
        """Nawiązuje połączenie z głównym systemem świadomości"""
        try:
            # Test połączenia REST API
            api_url = f"{config.adam_clay.consciousness_api_url}/health"
            
            async with self.session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"✅ Połączono z API świadomości: {data.get('status', 'unknown')}")
                    self.is_connected = True
                    self.last_sync = datetime.now()
                    log_consciousness_integration("CONNECT_REST", True, {"status": data.get('status')})
                else:
                    logger.warning(f"⚠️ Problemy z API świadomości: {response.status}")
                    log_consciousness_integration("CONNECT_REST", False, {"status_code": response.status})
            
            # Próba połączenia WebSocket
            await self._connect_websocket()
            
        except Exception as e:
            logger.error(f"❌ Błąd połączenia z systemem świadomości: {str(e)}")
            log_consciousness_integration("CONNECT", False, {"error": str(e)})
            self.is_connected = False
    
    async def _connect_websocket(self):
        """Nawiązuje połączenie WebSocket"""
        try:
            ws_url = config.adam_clay.websocket_url
            
            # Próba połączenia (z timeoutem)
            try:
                self.websocket_connection = await asyncio.wait_for(
                    websockets.connect(ws_url), 
                    timeout=10.0
                )
                logger.info("✅ Połączono przez WebSocket")
                log_consciousness_integration("CONNECT_WS", True)
                
            except asyncio.TimeoutError:
                logger.warning("⚠️ WebSocket timeout - kontynuuję bez WebSocket")
                log_consciousness_integration("CONNECT_WS", False, {"reason": "timeout"})
                
        except Exception as e:
            logger.warning(f"⚠️ Nie udało się połączyć przez WebSocket: {str(e)}")
            log_consciousness_integration("CONNECT_WS", False, {"error": str(e)})
    
    async def _listen_to_consciousness(self):
        """Nasłuchuje wydarzeń z systemu świadomości"""
        while True:
            try:
                if self.websocket_connection:
                    await self._listen_websocket()
                else:
                    # Fallback na polling REST API
                    await self._poll_rest_api()
                
                await asyncio.sleep(1)  # Krótka pauza
                
            except Exception as e:
                logger.error(f"❌ Błąd nasłuchiwania: {str(e)}")
                await self._handle_connection_error()
                await asyncio.sleep(self.reconnect_delay)
    
    async def _listen_websocket(self):
        """Nasłuchuje przez WebSocket"""
        try:
            message = await asyncio.wait_for(
                self.websocket_connection.recv(), 
                timeout=30.0
            )
            
            # Parsowanie wiadomości
            data = json.loads(message)
            event = ConsciousnessEvent(
                event_type=data.get("event_type", "unknown"),
                content=data.get("content", {}),
                timestamp=datetime.now(),
                source="consciousness_websocket",
                priority=data.get("priority", 1),
                requires_response=data.get("requires_response", False)
            )
            
            await self._process_consciousness_event(event)
            
        except asyncio.TimeoutError:
            # Ping-pong dla utrzymania połączenia
            await self.websocket_connection.ping()
            
        except websockets.exceptions.ConnectionClosed:
            logger.warning("🔌 Połączenie WebSocket zostało zamknięte")
            self.websocket_connection = None
            await self._handle_connection_error()
    
    async def _poll_rest_api(self):
        """Pobiera wydarzenia przez REST API (fallback)"""
        try:
            # Pobieranie najnowszych wydarzeń
            since = self.last_sync.isoformat() if self.last_sync else None
            url = f"{config.adam_clay.consciousness_api_url}/events"
            
            params = {}
            if since:
                params['since'] = since
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    events_data = await response.json()
                    
                    for event_data in events_data.get('events', []):
                        event = ConsciousnessEvent(
                            event_type=event_data.get("event_type", "unknown"),
                            content=event_data.get("content", {}),
                            timestamp=datetime.fromisoformat(event_data.get("timestamp", datetime.now().isoformat())),
                            source="consciousness_rest",
                            priority=event_data.get("priority", 1),
                            requires_response=event_data.get("requires_response", False)
                        )
                        
                        await self._process_consciousness_event(event)
                    
                    self.last_sync = datetime.now()
                    
        except Exception as e:
            logger.debug(f"Polling REST API: {str(e)}")
            await asyncio.sleep(5)  # Longer delay on error
    
    async def _process_consciousness_event(self, event: ConsciousnessEvent):
        """Przetwarza wydarzenie ze świadomości"""
        try:
            logger.info(f"📥 Otrzymano wydarzenie ze świadomości: {event.event_type}")
            
            # Stworzenie wydarzenia systemowego
            with get_db() as db:
                system_event = SystemEvent(
                    event_type=event.event_type,
                    content=event.content,
                    source=event.source,
                    priority=event.priority,
                    status="pending"
                )
                
                db.add(system_event)
                db.commit()
                db.refresh(system_event)
                
                # Przekazanie do agent managera poprzez importowanie lokalnie
                # (unikanie circular imports)
                from main import agent_manager
                
                if agent_manager:
                    await agent_manager.process_event(system_event)
                    
                log_consciousness_integration(
                    "PROCESS_EVENT", 
                    True, 
                    {"event_type": event.event_type}
                )
                
        except Exception as e:
            logger.error(f"❌ Błąd przetwarzania wydarzenia: {str(e)}")
            log_consciousness_integration(
                "PROCESS_EVENT", 
                False, 
                {"event_type": event.event_type, "error": str(e)}
            )
    
    async def send_response_to_consciousness(self, response: ConsciousnessResponse):
        """Wysyła odpowiedź do systemu świadomości"""
        try:
            url = f"{config.adam_clay.consciousness_api_url}/subconscious/response"
            
            data = {
                "source_agent_id": response.source_agent_id,
                "response_type": response.response_type,
                "content": response.content,
                "confidence": response.confidence,
                "emotional_tone": response.emotional_tone,
                "recommendations": response.recommendations,
                "metadata": response.metadata,
                "timestamp": datetime.now().isoformat()
            }
            
            async with self.session.post(url, json=data) as response_obj:
                if response_obj.status == 200:
                    logger.info(f"✅ Wysłano odpowiedź do świadomości od agenta {response.source_agent_id}")
                    log_consciousness_integration("SEND_RESPONSE", True, {"agent_id": response.source_agent_id})
                else:
                    logger.warning(f"⚠️ Problemy z wysłaniem odpowiedzi: {response_obj.status}")
                    log_consciousness_integration("SEND_RESPONSE", False, {"status_code": response_obj.status})
                    
        except Exception as e:
            logger.error(f"❌ Błąd wysyłania odpowiedzi: {str(e)}")
            log_consciousness_integration("SEND_RESPONSE", False, {"error": str(e)})
    
    async def sync_agent_states(self):
        """Synchronizuje stany agentów z systemem świadomości"""
        try:
            url = f"{config.adam_clay.consciousness_api_url}/subconscious/agents"
            
            # Pobieranie wszystkich agentów
            with get_db() as db:
                agents = db.query(SubconsciousAgent).all()
                
                agent_states = []
                for agent in agents:
                    agent_states.append({
                        "id": agent.id,
                        "name": agent.name,
                        "type": agent.agent_type.value,
                        "status": agent.status.value,
                        "activity_level": agent.current_activity_level,
                        "last_active": agent.last_active_at.isoformat() if agent.last_active_at else None
                    })
                
                data = {
                    "agents": agent_states,
                    "timestamp": datetime.now().isoformat()
                }
                
                async with self.session.post(url, json=data) as response:
                    if response.status == 200:
                        logger.info(f"✅ Zsynchronizowano stany {len(agent_states)} agentów")
                        log_consciousness_integration("SYNC_AGENTS", True, {"count": len(agent_states)})
                    else:
                        logger.warning(f"⚠️ Problemy z synchronizacją: {response.status}")
                        log_consciousness_integration("SYNC_AGENTS", False, {"status_code": response.status})
                        
        except Exception as e:
            logger.error(f"❌ Błąd synchronizacji stanów agentów: {str(e)}")
            log_consciousness_integration("SYNC_AGENTS", False, {"error": str(e)})
    
    async def send_thought_analysis(self, thought_id: int, analysis: Dict[str, Any]):
        """Wysyła analizę myśli do systemu świadomości"""
        try:
            url = f"{config.adam_clay.consciousness_api_url}/thoughts/{thought_id}/analysis"
            
            data = {
                "analysis": analysis,
                "timestamp": datetime.now().isoformat(),
                "source": "subconscious_agents"
            }
            
            async with self.session.post(url, json=data) as response:
                if response.status == 200:
                    logger.info(f"✅ Wysłano analizę myśli {thought_id}")
                    log_consciousness_integration("SEND_ANALYSIS", True, {"thought_id": thought_id})
                else:
                    logger.warning(f"⚠️ Problemy z wysłaniem analizy: {response.status}")
                    log_consciousness_integration("SEND_ANALYSIS", False, {"status_code": response.status})
                    
        except Exception as e:
            logger.error(f"❌ Błąd wysyłania analizy myśli: {str(e)}")
            log_consciousness_integration("SEND_ANALYSIS", False, {"error": str(e)})
    
    async def _handle_connection_error(self):
        """Obsługuje błędy połączenia"""
        self.is_connected = False
        self.reconnect_attempts += 1
        
        if self.reconnect_attempts < self.max_reconnect_attempts:
            logger.warning(f"🔄 Próba ponownego połączenia ({self.reconnect_attempts}/{self.max_reconnect_attempts})")
            await asyncio.sleep(self.reconnect_delay)
            
            try:
                await self._connect_to_consciousness()
                self.reconnect_attempts = 0  # Reset on successful connection
            except Exception as e:
                logger.error(f"❌ Nie udało się ponownie połączyć: {str(e)}")
        else:
            logger.error(f"❌ Maksymalna liczba prób połączenia przekroczona")
            log_consciousness_integration("RECONNECT_FAILED", False, {"attempts": self.reconnect_attempts})
    
    async def sync(self):
        """Wykonuje pełną synchronizację z systemem świadomości"""
        try:
            logger.info("🔄 Rozpoczynanie synchronizacji z systemem świadomości")
            
            # Synchronizacja stanów agentów
            await self.sync_agent_states()
            
            # Sprawdzenie połączenia
            if not self.is_connected:
                await self._connect_to_consciousness()
            
            self.last_sync = datetime.now()
            logger.info("✅ Synchronizacja zakończona pomyślnie")
            log_consciousness_integration("FULL_SYNC", True)
            
        except Exception as e:
            logger.error(f"❌ Błąd synchronizacji: {str(e)}")
            log_consciousness_integration("FULL_SYNC", False, {"error": str(e)})
    
    async def periodic_sync(self):
        """Wykonuje okresową synchronizację"""
        try:
            current_time = datetime.now()
            
            # Synchronizacja co 5 minut
            if self.last_sync is None or current_time - self.last_sync > timedelta(minutes=5):
                await self.sync()
                
        except Exception as e:
            logger.error(f"❌ Błąd okresowej synchronizacji: {str(e)}")
    
    def is_connected(self) -> bool:
        """Sprawdza czy połączenie jest aktywne"""
        return self.is_connected and (self.websocket_connection is not None or self.session is not None)
    
    async def stop(self):
        """Zatrzymuje integrację z systemem świadomości"""
        try:
            logger.info("🛑 Zatrzymywanie integracji z systemem świadomości")
            
            # Zamknięcie połączenia WebSocket
            if self.websocket_connection:
                await self.websocket_connection.close()
                self.websocket_connection = None
            
            # Zamknięcie sesji HTTP
            if self.session:
                await self.session.close()
                self.session = None
            
            self.is_connected = False
            logger.info("✅ Integracja zatrzymana")
            log_consciousness_integration("STOP", True)
            
        except Exception as e:
            logger.error(f"❌ Błąd zatrzymywania integracji: {str(e)}")
            log_consciousness_integration("STOP", False, {"error": str(e)})
    
    async def get_consciousness_status(self) -> Dict[str, Any]:
        """Pobiera status systemu świadomości"""
        try:
            url = f"{config.adam_clay.consciousness_api_url}/status"
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    status = await response.json()
                    return status
                else:
                    return {"error": f"HTTP {response.status}"}
                    
        except Exception as e:
            logger.error(f"❌ Błąd pobierania statusu świadomości: {str(e)}")
            return {"error": str(e)}
    
    async def report_system_health(self):
        """Raportuje stan zdrowia systemu podświadomości"""
        try:
            url = f"{config.adam_clay.consciousness_api_url}/subconscious/health"
            
            # Przygotowanie raportu
            with get_db() as db:
                total_agents = db.query(SubconsciousAgent).count()
                active_agents = db.query(SubconsciousAgent).filter(
                    SubconsciousAgent.status == AgentStatus.ACTIVE
                ).count()
            
            health_report = {
                "timestamp": datetime.now().isoformat(),
                "status": "healthy" if self.is_connected else "degraded",
                "total_agents": total_agents,
                "active_agents": active_agents,
                "connection_status": "connected" if self.is_connected else "disconnected",
                "last_sync": self.last_sync.isoformat() if self.last_sync else None
            }
            
            async with self.session.post(url, json=health_report) as response:
                if response.status == 200:
                    logger.debug("✅ Raport zdrowia wysłany")
                    log_consciousness_integration("HEALTH_REPORT", True)
                else:
                    logger.warning(f"⚠️ Problemy z wysłaniem raportu: {response.status}")
                    log_consciousness_integration("HEALTH_REPORT", False, {"status_code": response.status})
                    
        except Exception as e:
            logger.error(f"❌ Błąd raportowania zdrowia: {str(e)}")
            log_consciousness_integration("HEALTH_REPORT", False, {"error": str(e)}) 