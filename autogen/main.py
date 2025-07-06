from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import uvicorn
import asyncio
from contextlib import asynccontextmanager

# Lokalne importy
from config import config
from models import (
    SubconsciousAgent, AgentConversation, AgentInteraction, 
    AgentMemory, SystemEvent, AgentStatistics,
    AgentStatus, AgentType, Base
)
from database import get_db_dependency, get_db, engine, init_db
from agent_manager import AgentManager
from consciousness_integration import ConsciousnessIntegration
from schemas import (
    AgentCreate, AgentResponse, ConversationCreate, 
    SystemEventCreate, AgentListResponse
)
from logger import setup_logger

# Inicjalizacja loggera
logger = setup_logger("autogen_main")

# Globalne instancje
agent_manager = None
consciousness_integration = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Zarządzanie cyklem życia aplikacji"""
    # Startup
    logger.info("🚀 Uruchamianie Adam Clay AutoGen Subconscious Service")
    
    # Inicjalizacja bazy danych
    init_db()
    
    # Inicjalizacja globalnych instancji
    global agent_manager, consciousness_integration
    agent_manager = AgentManager()
    consciousness_integration = ConsciousnessIntegration()
    
    # Ładowanie agentów
    await agent_manager.load_agents()
    
    # Uruchomienie integracji z głównym systemem
    await consciousness_integration.start()
    
    # Uruchomienie zadań w tle
    asyncio.create_task(background_tasks())
    
    logger.info("✅ Serwis AutoGen uruchomiony pomyślnie")
    
    yield
    
    # Shutdown
    logger.info("🛑 Zamykanie serwisu AutoGen")
    
    if consciousness_integration:
        await consciousness_integration.stop()
    
    if agent_manager:
        await agent_manager.shutdown()
    
    logger.info("✅ Serwis AutoGen zamknięty pomyślnie")

# Inicjalizacja aplikacji FastAPI
app = FastAPI(
    title=config.service_name,
    version=config.version,
    description="Serwis podświadomych agentów dla Adam Clay - system wielu agentów AI",
    lifespan=lifespan
)

# Konfiguracja CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === ENDPOINTS API ===

@app.get("/")
async def root():
    """Endpoint główny"""
    return {
        "service": config.service_name,
        "version": config.version,
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Sprawdzenie stanu serwisu"""
    try:
        # Sprawdzenie bazy danych
        with get_db() as db:
            agents_count = db.query(SubconsciousAgent).count()
        
        # Sprawdzenie agentów
        active_agents = len(agent_manager.get_active_agents()) if agent_manager else 0
        
        return {
            "status": "healthy",
            "database": "connected",
            "agents": {
                "total": agents_count,
                "active": active_agents
            },
            "consciousness_integration": consciousness_integration.is_connected() if consciousness_integration else False,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )

@app.get("/agents", response_model=List[AgentResponse])
async def get_agents(db: Session = Depends(get_db_dependency)):
    """Pobiera wszystkich agentów"""
    try:
        agents = db.query(SubconsciousAgent).all()
        return agents
    except Exception as e:
        logger.error(f"Error getting agents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agents", response_model=AgentResponse)
async def create_agent(agent_data: AgentCreate, db: Session = Depends(get_db_dependency)):
    """Tworzy nowego agenta"""
    try:
        # Sprawdzenie czy agent o takiej nazwie już istnieje
        existing_agent = db.query(SubconsciousAgent).filter(
            SubconsciousAgent.name == agent_data.name
        ).first()
        
        if existing_agent:
            raise HTTPException(status_code=400, detail="Agent o takiej nazwie już istnieje")
        
        # Utworzenie nowego agenta
        agent = SubconsciousAgent(**agent_data.dict())
        db.add(agent)
        db.commit()
        db.refresh(agent)
        
        # Dodanie do managera agentów
        if agent_manager:
            await agent_manager.add_agent(agent)
        
        logger.info(f"Utworzono nowego agenta: {agent.name}")
        return agent
        
    except Exception as e:
        logger.error(f"Error creating agent: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: int, db: Session = Depends(get_db_dependency)):
    """Pobiera agenta po ID"""
    agent = db.query(SubconsciousAgent).filter(SubconsciousAgent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent nie znaleziony")
    return agent

@app.put("/agents/{agent_id}/status")
async def update_agent_status(agent_id: int, status: AgentStatus, db: Session = Depends(get_db_dependency)):
    """Aktualizuje status agenta"""
    try:
        agent = db.query(SubconsciousAgent).filter(SubconsciousAgent.id == agent_id).first()
        if not agent:
            raise HTTPException(status_code=404, detail="Agent nie znaleziony")
        
        old_status = agent.status
        agent.status = status
        agent.updated_at = datetime.now()
        
        db.commit()
        
        # Aktualizacja w managerze
        if agent_manager:
            await agent_manager.update_agent_status(agent_id, status)
        
        logger.info(f"Zmieniono status agenta {agent.name}: {old_status} -> {status}")
        return {"message": "Status agenta zaktualizowany", "old_status": old_status, "new_status": status}
        
    except Exception as e:
        logger.error(f"Error updating agent status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agents/{agent_id}/activate")
async def activate_agent(agent_id: int, db: Session = Depends(get_db_dependency)):
    """Aktywuje agenta"""
    try:
        agent = db.query(SubconsciousAgent).filter(SubconsciousAgent.id == agent_id).first()
        if not agent:
            raise HTTPException(status_code=404, detail="Agent nie znaleziony")
        
        if agent_manager:
            await agent_manager.activate_agent(agent_id)
        
        logger.info(f"Aktywowano agenta: {agent.name}")
        return {"message": f"Agent {agent.name} został aktywowany"}
        
    except Exception as e:
        logger.error(f"Error activating agent: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agents/{agent_id}/deactivate")
async def deactivate_agent(agent_id: int, db: Session = Depends(get_db_dependency)):
    """Deaktywuje agenta"""
    try:
        agent = db.query(SubconsciousAgent).filter(SubconsciousAgent.id == agent_id).first()
        if not agent:
            raise HTTPException(status_code=404, detail="Agent nie znaleziony")
        
        if agent_manager:
            await agent_manager.deactivate_agent(agent_id)
        
        logger.info(f"Deaktywowano agenta: {agent.name}")
        return {"message": f"Agent {agent.name} został deaktywowany"}
        
    except Exception as e:
        logger.error(f"Error deactivating agent: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/events")
async def create_system_event(event_data: SystemEventCreate, db: Session = Depends(get_db_dependency)):
    """Tworzy nowe wydarzenie systemowe"""
    try:
        event = SystemEvent(**event_data.dict())
        db.add(event)
        db.commit()
        db.refresh(event)
        
        # Przekazanie wydarzenia do managera agentów
        if agent_manager:
            await agent_manager.process_event(event)
        
        logger.info(f"Utworzono wydarzenie systemowe: {event.event_type}")
        return {"message": "Wydarzenie utworzone", "event_id": event.id}
        
    except Exception as e:
        logger.error(f"Error creating system event: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/{agent_id}/conversations")
async def get_agent_conversations(agent_id: int, limit: int = 10, db: Session = Depends(get_db_dependency)):
    """Pobiera konwersacje agenta"""
    try:
        conversations = db.query(AgentConversation).filter(
            AgentConversation.agent_id == agent_id
        ).order_by(AgentConversation.started_at.desc()).limit(limit).all()
        
        return conversations
        
    except Exception as e:
        logger.error(f"Error getting agent conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/{agent_id}/statistics")
async def get_agent_statistics(agent_id: int, db: Session = Depends(get_db_dependency)):
    """Pobiera statystyki agenta"""
    try:
        if agent_manager:
            stats = await agent_manager.get_agent_statistics(agent_id)
            return stats
        else:
            raise HTTPException(status_code=503, detail="Agent Manager nie jest dostępny")
            
    except Exception as e:
        logger.error(f"Error getting agent statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/consciousness/sync")
async def sync_with_consciousness():
    """Synchronizuje z głównym systemem świadomości"""
    try:
        if consciousness_integration:
            await consciousness_integration.sync()
            return {"message": "Synchronizacja z systemem świadomości zakończona"}
        else:
            raise HTTPException(status_code=503, detail="Integracja z systemem świadomości nie jest dostępna")
            
    except Exception as e:
        logger.error(f"Error syncing with consciousness: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# === ZADANIA W TLE ===

async def background_tasks():
    """Zadania wykonywane w tle"""
    logger.info("🔄 Uruchamianie zadań w tle")
    
    while True:
        try:
            # Sprawdzenie stanu agentów co 60 sekund
            if agent_manager:
                await agent_manager.health_check()
            
            # Synchronizacja z systemem świadomości co 5 minut
            if consciousness_integration:
                await consciousness_integration.periodic_sync()
            
            # Czyszczenie starych danych co godzinę
            await cleanup_old_data()
            
            # Oczekiwanie 60 sekund przed następnym cyklem
            await asyncio.sleep(60)
            
        except Exception as e:
            logger.error(f"Error in background tasks: {str(e)}")
            await asyncio.sleep(60)

async def cleanup_old_data():
    """Czyszczenie starych danych"""
    try:
        with get_db() as db:
            # Usuń stare konwersacje (starsze niż 30 dni)
            old_conversations = db.query(AgentConversation).filter(
                AgentConversation.started_at < datetime.now() - timedelta(days=30)
            ).delete()
            
            # Usuń stare wydarzenia (starsze niż 7 dni)
            old_events = db.query(SystemEvent).filter(
                SystemEvent.created_at < datetime.now() - timedelta(days=7)
            ).delete()
            
            db.commit()
            
            if old_conversations > 0 or old_events > 0:
                logger.info(f"Usunięto {old_conversations} starych konwersacji i {old_events} starych wydarzeń")
                
    except Exception as e:
        logger.error(f"Error cleaning up old data: {str(e)}")

# === URUCHAMIANIE APLIKACJI ===

if __name__ == "__main__":
    logger.info("🚀 Uruchamianie Adam Clay AutoGen Subconscious Service")
    
    uvicorn.run(
        "main:app",
        host=config.host,
        port=config.port,
        reload=config.debug,
        log_level=config.log_level.lower()
    ) 