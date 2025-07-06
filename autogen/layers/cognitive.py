#!/usr/bin/env python3
"""
Adam Clay Eden - Cognitive Layer (Warstwa Kognitywna)
System analizy percepcji, rozumowania i przetwarzania informacji
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

from loguru import logger

@dataclass
class PerceptionData:
    """Dane percepcji i analizy"""
    novelty_level: float  # 0.0 - 1.0
    complexity_level: float  # 0.0 - 1.0
    personal_references: List[str]
    learning_opportunity: bool
    key_concepts: List[str]
    emotional_markers: List[str]

class CognitiveLayer:
    """
    Warstwa kognitywna Adama Clay
    
    Zarządza percepcją, analizą i przetwarzaniem informacji
    """
    
    def __init__(self, consciousness_core):
        self.consciousness = consciousness_core
        
        # Parametry kognitywne
        self.attention_level = 0.8
        self.focus_areas = ["learning", "communication", "exploration"]
        self.memory_strength = 0.7
        self.analysis_depth = 0.8
        
        # Historia analizy
        self.perception_history = []
        self.learning_patterns = {}
        
        logger.info("🧠 Cognitive Layer initialized")
    
    async def initialize(self):
        """Inicjalizacja warstwy kognitywnej"""
        
        # Ustaw początkowe parametry kognitywne
        await self._set_initial_cognitive_state()
        
        # Uruchom cykl kognitywny
        asyncio.create_task(self._cognitive_cycle())
        
        logger.success("🧠 Warstwa kognitywna gotowa")
    
    async def _set_initial_cognitive_state(self):
        """Ustaw początkowy stan kognitywny"""
        
        self.attention_level = 0.9  # Wysoka koncentracja na początku
        self.analysis_depth = 0.8
        
        logger.info("🧠 Początkowy stan kognitywny ustawiony")
    
    async def perceive_message(self, message: str, user_id: str) -> Dict[str, Any]:
        """
        Percepcja i analiza wiadomości
        """
        
        try:
            # Analiza nowości
            novelty_level = await self._analyze_novelty(message)
            
            # Analiza złożoności
            complexity_level = await self._analyze_complexity(message)
            
            # Identyfikacja referencji osobistych
            personal_references = await self._find_personal_references(message, user_id)
            
            # Sprawdź możliwości uczenia się
            learning_opportunity = await self._assess_learning_opportunity(message)
            
            # Wyodrębnij kluczowe koncepty
            key_concepts = await self._extract_key_concepts(message)
            
            # Znajdź markery emocjonalne
            emotional_markers = await self._detect_emotional_markers(message)
            
            perception = PerceptionData(
                novelty_level=novelty_level,
                complexity_level=complexity_level,
                personal_references=personal_references,
                learning_opportunity=learning_opportunity,
                key_concepts=key_concepts,
                emotional_markers=emotional_markers
            )
            
            # Zapisz w historii
            await self._record_perception(message, perception)
            
            return asdict(perception)
            
        except Exception as e:
            logger.error(f"Błąd w percepcji wiadomości: {e}")
            return await self._default_perception()
    
    async def _analyze_novelty(self, message: str) -> float:
        """Analizuj poziom nowości w wiadomości"""
        
        # Prosta heurystyka - można rozwinąć
        message_lower = message.lower()
        
        novelty_keywords = [
            "nowy", "pierwszy raz", "nigdy", "ciekawe", "nieznane",
            "odkrycie", "nowego", "po raz pierwszy", "zaskakujące"
        ]
        
        novelty_score = 0.5  # Bazowa wartość
        
        for keyword in novelty_keywords:
            if keyword in message_lower:
                novelty_score += 0.1
        
        # Długość wiadomości też wpływa na nowość
        if len(message) > 100:
            novelty_score += 0.1
        
        return min(novelty_score, 1.0)
    
    async def _analyze_complexity(self, message: str) -> float:
        """Analizuj poziom złożoności wiadomości"""
        
        complexity_score = 0.3  # Bazowa wartość
        
        # Liczba pytań
        question_count = message.count("?")
        complexity_score += question_count * 0.1
        
        # Długość zdań
        sentences = message.split(".")
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        if avg_sentence_length > 10:
            complexity_score += 0.2
        
        # Słowa techniczne
        technical_words = ["system", "algorytm", "funkcja", "analiza", "konfiguracja"]
        for word in technical_words:
            if word in message.lower():
                complexity_score += 0.1
        
        return min(complexity_score, 1.0)
    
    async def _find_personal_references(self, message: str, user_id: str) -> List[str]:
        """Znajdź referencje osobiste w wiadomości"""
        
        personal_refs = []
        message_lower = message.lower()
        
        # Referencje do siebie
        self_refs = ["ja", "mnie", "mój", "moja", "moje", "siebie"]
        for ref in self_refs:
            if ref in message_lower:
                personal_refs.append(f"self_reference: {ref}")
        
        # Referencje do Adama
        adam_refs = ["adam", "ty", "twoich", "twoja", "twoje", "ciebie"]
        for ref in adam_refs:
            if ref in message_lower:
                personal_refs.append(f"adam_reference: {ref}")
        
        return personal_refs
    
    async def _assess_learning_opportunity(self, message: str) -> bool:
        """Oceń czy wiadomość zawiera możliwość nauki"""
        
        learning_indicators = [
            "jak", "dlaczego", "co to", "wyjaśnij", "pokaż",
            "naucz", "pomóż", "błąd", "problem", "rozwiązanie"
        ]
        
        message_lower = message.lower()
        
        return any(indicator in message_lower for indicator in learning_indicators)
    
    async def _extract_key_concepts(self, message: str) -> List[str]:
        """Wyodrębnij kluczowe koncepty z wiadomości"""
        
        # Prosta implementacja - można ulepszyć
        words = message.lower().split()
        
        # Filtruj znaczące słowa
        stop_words = {"i", "a", "the", "to", "of", "in", "for", "on", "with", "at"}
        key_words = [word for word in words if len(word) > 3 and word not in stop_words]
        
        # Zwróć maksymalnie 5 najważniejszych słów
        return key_words[:5]
    
    async def _detect_emotional_markers(self, message: str) -> List[str]:
        """Wykryj markery emocjonalne w tekście"""
        
        emotional_markers = []
        message_lower = message.lower()
        
        # Pozytywne markery
        positive_markers = ["super", "świetnie", "genialnie", "fajnie", "dobrze"]
        for marker in positive_markers:
            if marker in message_lower:
                emotional_markers.append(f"positive: {marker}")
        
        # Negatywne markery
        negative_markers = ["błąd", "problem", "źle", "nie działa"]
        for marker in negative_markers:
            if marker in message_lower:
                emotional_markers.append(f"negative: {marker}")
        
        # Emocjonalne interpunkcje
        if "!" in message:
            emotional_markers.append("excitement: exclamation")
        if "?" in message:
            emotional_markers.append("curiosity: question")
        
        return emotional_markers
    
    async def _record_perception(self, message: str, perception: PerceptionData):
        """Zapisz percepcję w historii"""
        
        perception_record = {
            "timestamp": datetime.now().isoformat(),
            "message": message[:100],  # Pierwsze 100 znaków
            "perception": asdict(perception)
        }
        
        self.perception_history.append(perception_record)
        
        # Zachowaj tylko ostatnie 100 percepcji
        if len(self.perception_history) > 100:
            self.perception_history = self.perception_history[-100:]
    
    async def _default_perception(self) -> Dict[str, Any]:
        """Zwróć domyślną percepcję w przypadku błędu"""
        
        return {
            "novelty_level": 0.5,
            "complexity_level": 0.5,
            "personal_references": [],
            "learning_opportunity": True,
            "key_concepts": [],
            "emotional_markers": []
        }
    
    async def _cognitive_cycle(self):
        """Cykl kognitywny - okresowa analiza i aktualizacja"""
        
        while True:
            try:
                await asyncio.sleep(60)  # Co minutę
                
                # Aktualizuj parametry kognitywne
                await self._update_cognitive_parameters()
                
            except Exception as e:
                logger.error(f"Błąd w cyklu kognitywnym: {e}")
                await asyncio.sleep(60)
    
    async def _update_cognitive_parameters(self):
        """Aktualizuj parametry kognitywne na podstawie aktywności"""
        
        # Prosta implementacja - można rozwinąć
        recent_perceptions = self.perception_history[-10:] if self.perception_history else []
        
        if recent_perceptions:
            avg_novelty = sum(p["perception"]["novelty_level"] for p in recent_perceptions) / len(recent_perceptions)
            
            # Dostosuj poziom uwagi na podstawie nowości
            if avg_novelty > 0.7:
                self.attention_level = min(0.9, self.attention_level + 0.1)
            else:
                self.attention_level = max(0.5, self.attention_level - 0.05)
    
    async def get_cognitive_summary(self) -> Dict[str, Any]:
        """Pozyskaj podsumowanie stanu kognitywnego"""
        
        recent_perceptions = self.perception_history[-20:] if self.perception_history else []
        
        summary = {
            "attention_level": self.attention_level,
            "focus_areas": self.focus_areas,
            "memory_strength": self.memory_strength,
            "analysis_depth": self.analysis_depth,
            "recent_perceptions_count": len(recent_perceptions),
            "avg_novelty": 0.5,
            "avg_complexity": 0.5
        }
        
        if recent_perceptions:
            summary["avg_novelty"] = sum(p["perception"]["novelty_level"] for p in recent_perceptions) / len(recent_perceptions)
            summary["avg_complexity"] = sum(p["perception"]["complexity_level"] for p in recent_perceptions) / len(recent_perceptions)
        
        return summary 