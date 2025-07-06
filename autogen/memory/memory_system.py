#!/usr/bin/env python3
"""
System pamięci dla Adama Clay Eden v1.0
Zarządza pamięcią krótko i długotrwałą
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, asdict
import numpy as np
from loguru import logger
import hashlib

@dataclass
class MemoryEntry:
    """Pojedynczy wpis w pamięci"""
    id: str
    content: str
    timestamp: datetime
    memory_type: str  # 'short_term', 'long_term', 'episodic', 'semantic'
    importance: float  # 0.0 - 1.0
    emotional_context: Dict[str, float]
    tags: Set[str]
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    decay_factor: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result['timestamp'] = self.timestamp.isoformat()
        result['last_accessed'] = self.last_accessed.isoformat() if self.last_accessed else None
        result['tags'] = list(self.tags)
        return result

@dataclass  
class MemoryCluster:
    """Klaster powiązanych wspomnień"""
    id: str
    theme: str
    memories: List[str]  # IDs wspomnień
    strength: float
    created_at: datetime
    last_updated: datetime

class MemorySystem:
    """System zarządzania pamięcią Adama"""
    
    def __init__(self, db_config: Dict[str, Any]):
        self.db_config = db_config
        self.short_term_memory: Dict[str, MemoryEntry] = {}
        self.long_term_memory: Dict[str, MemoryEntry] = {}
        self.memory_clusters: Dict[str, MemoryCluster] = {}
        
        # Parametry systemu pamięci
        self.short_term_capacity = 50
        self.consolidation_threshold = 0.7
        self.decay_rate = 0.95
        self.cluster_similarity_threshold = 0.8
        
        logger.info("🧠 Memory System initialized")

    async def initialize(self):
        """Inicjalizuje system pamięci"""
        try:
            await self._load_from_database()
            # Uruchom cykl konsolidacji
            asyncio.create_task(self._consolidation_cycle())
            logger.success("💾 System pamięci gotowy")
        except Exception as e:
            logger.error(f"❌ Błąd inicjalizacji pamięci: {e}")

    async def store_memory(self, content: str, memory_type: str = "short_term", 
                          importance: float = 0.5, emotional_context: Dict[str, float] = None,
                          tags: Set[str] = None) -> str:
        """Zapisuje nową pamięć"""
        try:
            memory_id = await self._generate_memory_id(content)
            
            entry = MemoryEntry(
                id=memory_id,
                content=content,
                timestamp=datetime.now(),
                memory_type=memory_type,
                importance=importance,
                emotional_context=emotional_context or {},
                tags=tags or set(),
                access_count=0,
                last_accessed=None,
                decay_factor=1.0
            )
            
            if memory_type == "short_term":
                self.short_term_memory[memory_id] = entry
                await self._manage_short_term_capacity()
            else:
                self.long_term_memory[memory_id] = entry
                
            await self._save_to_database(entry)
            await self._update_clusters(entry)
            
            logger.info(f"💾 Zapisano pamięć: {memory_id[:8]}...")
            return memory_id
            
        except Exception as e:
            logger.error(f"❌ Błąd zapisywania pamięci: {e}")
            return ""

    async def retrieve_memories(self, query: str, limit: int = 10) -> List[MemoryEntry]:
        """Wyszukuje wspomnienia pasujące do zapytania"""
        try:
            all_memories = {**self.short_term_memory, **self.long_term_memory}
            matches = []
            
            for memory in all_memories.values():
                similarity = await self._calculate_similarity(query, memory.content)
                if similarity > 0.3:  # próg podobieństwa
                    memory.access_count += 1
                    memory.last_accessed = datetime.now()
                    matches.append((similarity, memory))
            
            # Sortuj po podobieństwie i ważności
            matches.sort(key=lambda x: x[0] * x[1].importance, reverse=True)
            result = [match[1] for match in matches[:limit]]
            
            logger.info(f"🔍 Znaleziono {len(result)} wspomnień dla: {query[:50]}...")
            return result
            
        except Exception as e:
            logger.error(f"❌ Błąd wyszukiwania pamięci: {e}")
            return []

    async def _generate_memory_id(self, content: str) -> str:
        """Generuje unikalny ID dla pamięci"""
        timestamp = str(time.time())
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        return f"mem_{timestamp}_{content_hash}"

    async def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Oblicza podobieństwo między tekstami (uproszczona wersja)"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
            
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0

    async def _manage_short_term_capacity(self):
        """Zarządza pojemnością pamięci krótkotrwałej"""
        if len(self.short_term_memory) > self.short_term_capacity:
            # Usuń najstarsze i najmniej ważne wspomnienia
            sorted_memories = sorted(
                self.short_term_memory.items(),
                key=lambda x: (x[1].importance * x[1].decay_factor, x[1].timestamp)
            )
            
            to_remove = len(self.short_term_memory) - self.short_term_capacity
            for i in range(to_remove):
                memory_id, memory = sorted_memories[i]
                
                # Przenieś ważne wspomnienia do pamięci długotrwałej
                if memory.importance > self.consolidation_threshold:
                    memory.memory_type = "long_term"
                    self.long_term_memory[memory_id] = memory
                    logger.info(f"📚 Przeniesiono do pamięci długotrwałej: {memory_id[:8]}...")
                
                del self.short_term_memory[memory_id]

    async def _consolidation_cycle(self):
        """Cykl konsolidacji pamięci - uruchamiany okresowo"""
        while True:
            try:
                await asyncio.sleep(300)  # co 5 minut
                await self._apply_decay()
                await self._consolidate_memories()
                await self._cleanup_old_memories()
                
            except Exception as e:
                logger.error(f"❌ Błąd cyklu konsolidacji: {e}")

    async def _apply_decay(self):
        """Aplikuje zanik pamięci"""
        for memory in self.short_term_memory.values():
            memory.decay_factor *= self.decay_rate
            
        # Usuń mocno zaniedane wspomnienia
        to_remove = [mid for mid, mem in self.short_term_memory.items() 
                    if mem.decay_factor < 0.1 and mem.importance < 0.3]
        
        for memory_id in to_remove:
            del self.short_term_memory[memory_id]

    async def _consolidate_memories(self):
        """Konsoliduje wspomnienia w klastry"""
        # Uproszczona implementacja klastrowania
        pass

    async def _update_clusters(self, memory: MemoryEntry):
        """Aktualizuje klastry pamięci"""
        # Uproszczona implementacja
        pass

    async def _cleanup_old_memories(self):
        """Czyści stare wspomnienia"""
        cutoff_date = datetime.now() - timedelta(days=30)
        
        to_remove = [mid for mid, mem in self.long_term_memory.items()
                    if mem.timestamp < cutoff_date and mem.importance < 0.3]
        
        for memory_id in to_remove:
            del self.long_term_memory[memory_id]
            
        if to_remove:
            logger.info(f"🧹 Usunięto {len(to_remove)} starych wspomnień")

    async def _load_from_database(self):
        """Ładuje pamięć z bazy danych"""
        # TODO: Implementacja ładowania z MySQL
        logger.info("📥 Ładowanie pamięci z bazy danych...")

    async def _save_to_database(self, memory: MemoryEntry):
        """Zapisuje pamięć do bazy danych"""
        # TODO: Implementacja zapisu do MySQL
        pass

    async def get_memory_stats(self) -> Dict[str, Any]:
        """Zwraca statystyki pamięci"""
        return {
            "short_term_count": len(self.short_term_memory),
            "long_term_count": len(self.long_term_memory),
            "clusters_count": len(self.memory_clusters),
            "total_memories": len(self.short_term_memory) + len(self.long_term_memory)
        }

    async def get_relevant_memories(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Pobiera odpowiednie wspomnienia dla zapytania (alias dla retrieve_memories)"""
        memories = await self.retrieve_memories(query, limit)
        return [memory.to_dict() for memory in memories]

    async def shutdown(self):
        """Zamyka system pamięci"""
        logger.info("💾 Zamykanie systemu pamięci...")
        # TODO: Finalne zapisanie do bazy danych
        logger.success("💾 System pamięci zamknięty") 