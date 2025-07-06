from pydantic import BaseModel, Field, validator
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from enum import Enum

from models import AgentStatus, AgentType

# === SCHEMATY BAZOWE ===

class AgentBase(BaseModel):
    """Bazowy schemat agenta"""
    name: str = Field(..., min_length=1, max_length=100)
    agent_type: AgentType
    description: Optional[str] = None
    personality_traits: Optional[Dict[str, Any]] = None
    skills: Optional[Dict[str, Any]] = None
    responsibilities: Optional[Dict[str, Any]] = None
    system_prompt: Optional[str] = None
    llm_config: Optional[Dict[str, Any]] = None
    activation_threshold: Optional[float] = Field(0.5, ge=0.0, le=1.0)
    priority_level: Optional[int] = Field(1, ge=1, le=10)
    consciousness_integration: Optional[Dict[str, Any]] = None

class AgentCreate(AgentBase):
    """Schemat tworzenia agenta"""
    pass

class AgentUpdate(BaseModel):
    """Schemat aktualizacji agenta"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    agent_type: Optional[AgentType] = None
    description: Optional[str] = None
    personality_traits: Optional[Dict[str, Any]] = None
    skills: Optional[Dict[str, Any]] = None
    responsibilities: Optional[Dict[str, Any]] = None
    system_prompt: Optional[str] = None
    llm_config: Optional[Dict[str, Any]] = None
    activation_threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    priority_level: Optional[int] = Field(None, ge=1, le=10)
    consciousness_integration: Optional[Dict[str, Any]] = None

class AgentResponse(AgentBase):
    """Schemat odpowiedzi z danymi agenta"""
    id: int
    status: AgentStatus
    current_activity_level: float
    created_at: datetime
    updated_at: datetime
    last_active_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class AgentListResponse(BaseModel):
    """Schemat listy agentów"""
    agents: List[AgentResponse]
    total: int
    active: int
    inactive: int

# === SCHEMATY KONWERSACJI ===

class ConversationBase(BaseModel):
    """Bazowy schemat konwersacji"""
    trigger_event: str = Field(..., min_length=1, max_length=200)
    context: Optional[Dict[str, Any]] = None

class ConversationCreate(ConversationBase):
    """Schemat tworzenia konwersacji"""
    agent_id: int

class ConversationUpdate(BaseModel):
    """Schemat aktualizacji konwersacji"""
    messages: Optional[List[Dict[str, Any]]] = None
    summary: Optional[str] = None
    insights: Optional[Dict[str, Any]] = None
    recommendations: Optional[Dict[str, Any]] = None
    emotional_state: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)

class ConversationResponse(ConversationBase):
    """Schemat odpowiedzi z danymi konwersacji"""
    id: int
    agent_id: int
    messages: List[Dict[str, Any]]
    summary: Optional[str] = None
    insights: Optional[Dict[str, Any]] = None
    recommendations: Optional[Dict[str, Any]] = None
    emotional_state: Optional[Dict[str, Any]] = None
    status: str
    confidence_score: Optional[float] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    
    class Config:
        from_attributes = True

# === SCHEMATY WYDARZEŃ SYSTEMOWYCH ===

class SystemEventBase(BaseModel):
    """Bazowy schemat wydarzenia systemowego"""
    event_type: str = Field(..., min_length=1, max_length=100)
    content: Dict[str, Any]
    source: str = Field(..., min_length=1, max_length=200)
    priority: Optional[int] = Field(1, ge=1, le=10)

class SystemEventCreate(SystemEventBase):
    """Schemat tworzenia wydarzenia systemowego"""
    pass

class SystemEventResponse(SystemEventBase):
    """Schemat odpowiedzi z danymi wydarzenia"""
    id: int
    processed_by_agents: Optional[Dict[str, Any]] = None
    responses: Optional[Dict[str, Any]] = None
    status: str
    created_at: datetime
    processed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# === SCHEMATY PAMIĘCI AGENTÓW ===

class AgentMemoryBase(BaseModel):
    """Bazowy schemat pamięci agenta"""
    memory_type: str = Field(..., min_length=1, max_length=100)
    content: str
    metadata: Optional[Dict[str, Any]] = None
    importance_score: Optional[float] = Field(0.5, ge=0.0, le=1.0)
    emotional_weight: Optional[float] = Field(0.5, ge=0.0, le=1.0)
    tags: Optional[List[str]] = None
    related_memories: Optional[List[int]] = None
    consciousness_link: Optional[str] = None

class AgentMemoryCreate(AgentMemoryBase):
    """Schemat tworzenia pamięci agenta"""
    agent_id: int

class AgentMemoryResponse(AgentMemoryBase):
    """Schemat odpowiedzi z danymi pamięci"""
    id: int
    agent_id: int
    created_at: datetime
    accessed_at: Optional[datetime] = None
    access_count: int
    
    class Config:
        from_attributes = True

# === SCHEMATY INTERAKCJI MIĘDZY AGENTAMI ===

class AgentInteractionBase(BaseModel):
    """Bazowy schemat interakcji między agentami"""
    interaction_type: str = Field(..., min_length=1, max_length=100)
    content: Dict[str, Any]
    outcome: Optional[Dict[str, Any]] = None
    effectiveness_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    harmony_score: Optional[float] = Field(None, ge=0.0, le=1.0)

class AgentInteractionCreate(AgentInteractionBase):
    """Schemat tworzenia interakcji"""
    agent_id: int
    target_agent_id: int

class AgentInteractionResponse(AgentInteractionBase):
    """Schemat odpowiedzi z danymi interakcji"""
    id: int
    agent_id: int
    target_agent_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# === SCHEMATY STATYSTYK ===

class AgentStatisticsResponse(BaseModel):
    """Schemat statystyk agenta"""
    agent_id: int
    period_start: datetime
    period_end: datetime
    total_interactions: int
    successful_interactions: int
    success_rate: float
    average_response_time: Optional[float] = None
    average_confidence: Optional[float] = None
    user_satisfaction: Optional[float] = None
    knowledge_growth: Optional[float] = None
    adaptation_rate: Optional[float] = None
    
    class Config:
        from_attributes = True

class SystemStatisticsResponse(BaseModel):
    """Schemat statystyk systemu"""
    total_agents: int
    active_agents: int
    inactive_agents: int
    total_conversations: int
    total_events: int
    total_memories: int
    average_system_load: float
    uptime_seconds: int
    
# === SCHEMATY KOMUNIKACJI Z SYSTEMEM GŁÓWNYM ===

class ConsciousnessEventBase(BaseModel):
    """Bazowy schemat wydarzenia ze świadomości"""
    event_type: str
    thought_id: Optional[int] = None
    content: str
    emotional_state: Optional[Dict[str, Any]] = None
    priority: Optional[int] = Field(1, ge=1, le=10)
    requires_response: bool = False

class ConsciousnessEventCreate(ConsciousnessEventBase):
    """Schemat tworzenia wydarzenia ze świadomości"""
    pass

class ConsciousnessResponse(BaseModel):
    """Schemat odpowiedzi do systemu świadomości"""
    source_agent_id: int
    response_type: str
    content: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    emotional_tone: Optional[str] = None
    recommendations: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

# === SCHEMATY KONFIGURACJI ===

class AgentConfigUpdate(BaseModel):
    """Schemat aktualizacji konfiguracji agenta"""
    llm_config: Optional[Dict[str, Any]] = None
    activation_threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    priority_level: Optional[int] = Field(None, ge=1, le=10)
    consciousness_integration: Optional[Dict[str, Any]] = None

class ServiceStatusResponse(BaseModel):
    """Schemat statusu serwisu"""
    service_name: str
    version: str
    status: str
    uptime: int
    database_connected: bool
    agents_count: int
    active_agents_count: int
    consciousness_connected: bool
    last_sync: Optional[datetime] = None
    
# === WALIDATORY ===

class AgentCreateValidator(AgentCreate):
    """Walidator tworzenia agenta z dodatkowymi sprawdzeniami"""
    
    @validator('personality_traits')
    def validate_personality_traits(cls, v):
        if v is not None and not isinstance(v, dict):
            raise ValueError('personality_traits must be a dictionary')
        return v
    
    @validator('skills')
    def validate_skills(cls, v):
        if v is not None and not isinstance(v, dict):
            raise ValueError('skills must be a dictionary')
        return v
    
    @validator('llm_config')
    def validate_llm_config(cls, v):
        if v is not None:
            if not isinstance(v, dict):
                raise ValueError('model_config must be a dictionary')
            
            # Sprawdzenie wymaganych kluczy
            required_keys = ['temperature', 'max_tokens', 'model']
            for key in required_keys:
                if key not in v:
                    raise ValueError(f'model_config must contain {key}')
        return v

# === SCHEMATY POMOCNICZE ===

class PaginationParams(BaseModel):
    """Schemat parametrów paginacji"""
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)
    
class FilterParams(BaseModel):
    """Schemat parametrów filtrowania"""
    agent_type: Optional[AgentType] = None
    status: Optional[AgentStatus] = None
    priority_min: Optional[int] = Field(None, ge=1, le=10)
    priority_max: Optional[int] = Field(None, ge=1, le=10)
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None 