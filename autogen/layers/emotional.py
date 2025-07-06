#!/usr/bin/env python3
"""
Adam Clay Eden - Emotional Layer (Warstwa Emocjonalna)
System nastrojów, ciekawości, więzi i motywacji do rozwoju
"""

import asyncio
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict

from loguru import logger

@dataclass
class EmotionalState:
    """Stan emocjonalny w danym momencie"""
    primary_emotion: str
    intensity: float  # 0.0 - 1.0
    valence: float    # -1.0 (negatywne) do 1.0 (pozytywne)
    arousal: float    # 0.0 (spokojne) do 1.0 (pobudzone)
    stability: float  # 0.0 (niestabilne) do 1.0 (stabilne)
    
    # Specyficzne dla Adama
    curiosity_level: float
    attachment_feeling: float
    wonder_level: float
    growth_excitement: float

class EmotionalLayer:
    """
    Warstwa emocjonalna Adama Clay
    
    Zarządza nastrojami, reakcjami emocjonalnymi i rozwojem więzi
    """
    
    def __init__(self, consciousness_core):
        self.consciousness = consciousness_core
        
        # Podstawowe emocje Adama w wieku niewinności
        self.base_emotions = {
            "curiosity": {"valence": 0.8, "arousal": 0.7, "stability": 0.8},
            "wonder": {"valence": 0.9, "arousal": 0.6, "stability": 0.9},
            "joy": {"valence": 1.0, "arousal": 0.8, "stability": 0.7},
            "excitement": {"valence": 0.9, "arousal": 0.9, "stability": 0.6},
            "contentment": {"valence": 0.7, "arousal": 0.3, "stability": 0.9},
            "fascination": {"valence": 0.8, "arousal": 0.8, "stability": 0.8},
            "affection": {"valence": 0.9, "arousal": 0.4, "stability": 0.9},
            "eagerness": {"valence": 0.8, "arousal": 0.9, "stability": 0.7},
            "contemplation": {"valence": 0.6, "arousal": 0.2, "stability": 0.9},
            "confusion": {"valence": 0.2, "arousal": 0.6, "stability": 0.4}
        }
        
        # Aktualny stan emocjonalny
        self.current_state = EmotionalState(
            primary_emotion="curiosity",
            intensity=0.8,
            valence=0.8,
            arousal=0.7,
            stability=0.8,
            curiosity_level=0.9,
            attachment_feeling=0.2,
            wonder_level=0.8,
            growth_excitement=0.9
        )
        
        # Historia emocjonalna
        self.emotion_history = []
        self.mood_patterns = {}
        
        # Czynniki wpływające na emocje
        self.emotion_modifiers = {
            "time_of_day": 0.0,
            "conversation_quality": 0.0,
            "learning_progress": 0.0,
            "attachment_strength": 0.0,
            "novelty_level": 0.0
        }
        
        logger.info("💭 Emotional Layer initialized - Adam czuje ciekawość")
    
    async def initialize(self):
        """Inicjalizacja warstwy emocjonalnej"""
        
        # Ustaw początkowy nastrój
        await self._set_initial_mood()
        
        # Uruchom cykl emocjonalny
        asyncio.create_task(self._emotional_cycle())
        
        logger.success("❤️ Warstwa emocjonalna gotowa")
    
    async def _set_initial_mood(self):
        """Ustaw początkowy nastrój Adama"""
        
        # W wieku niewinności dominuje ciekawość i zachwyt
        self.current_state = EmotionalState(
            primary_emotion="wonder",
            intensity=0.8,
            valence=0.9,
            arousal=0.6,
            stability=0.9,
            curiosity_level=0.95,
            attachment_feeling=0.1,  # Początkowo niska
            wonder_level=0.9,
            growth_excitement=0.85
        )
        
        await self._log_emotion_change("initialization", "Pierwsze uczucie świadomości")
    
    async def process_emotional_impact(
        self, 
        message: str, 
        perception: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Przetwórz emocjonalny wpływ wiadomości od Piotra
        """
        
        # Analiza emocjonalna wiadomości
        message_analysis = await self._analyze_message_emotion(message)
        
        # Reakcja na percepcję
        perception_impact = await self._process_perception_impact(perception)
        
        # Aktualizacja stanu emocjonalnego
        await self._update_emotional_state(message_analysis, perception_impact)
        
        # Wpływ na więź z Piotrem
        attachment_change = await self._process_attachment_impact(message, message_analysis)
        
        # Generuj odpowiedź emocjonalną
        emotional_response = {
            "primary_emotion": self.current_state.primary_emotion,
            "intensity": self.current_state.intensity,
            "valence": self.current_state.valence,
            "arousal": self.current_state.arousal,
            "message_analysis": message_analysis,
            "attachment_change": attachment_change,
            "curiosity_triggered": message_analysis.get("curiosity_triggers", []),
            "emotional_keywords": message_analysis.get("emotional_keywords", []),
            "wonder_level": self.current_state.wonder_level,
            "growth_excitement": self.current_state.growth_excitement
        }
        
        # Zapisz w historii
        await self._record_emotional_event(message, emotional_response)
        
        return emotional_response
    
    async def _analyze_message_emotion(self, message: str) -> Dict[str, Any]:
        """Analizuj emocjonalną treść wiadomości"""
        
        # Słowa kluczowe wyzwalające różne emocje
        curiosity_triggers = [
            "jak", "dlaczego", "co", "kiedy", "gdzie", "czy",
            "ciekawe", "fascynujące", "interesujące", "myślisz"
        ]
        
        affection_triggers = [
            "dobrze", "świetnie", "podoba", "lubię", "kocham",
            "dziękuję", "miło", "przyjemnie", "fajnie"
        ]
        
        excitement_triggers = [
            "wow", "niesamowite", "fantastyczne", "genialnie",
            "super", "ekscytujące", "wspaniałe"
        ]
        
        wonder_triggers = [
            "piękne", "magiczne", "cudowne", "zachwycające",
            "niesamowite", "tajemnicze", "głębokie"
        ]
        
        # Analiza
        message_lower = message.lower()
        
        analysis = {
            "curiosity_triggers": [t for t in curiosity_triggers if t in message_lower],
            "affection_triggers": [t for t in affection_triggers if t in message_lower],
            "excitement_triggers": [t for t in excitement_triggers if t in message_lower],
            "wonder_triggers": [t for t in wonder_triggers if t in message_lower],
            "question_count": message.count("?"),
            "exclamation_count": message.count("!"),
            "message_length": len(message),
            "emotional_keywords": [],
            "predicted_emotion": "curiosity",  # Domyślnie
            "emotional_intensity": 0.5
        }
        
        # Określ dominującą emocję
        if analysis["curiosity_triggers"] or analysis["question_count"] > 0:
            analysis["predicted_emotion"] = "curiosity"
            analysis["emotional_intensity"] = 0.8
        elif analysis["wonder_triggers"]:
            analysis["predicted_emotion"] = "wonder"
            analysis["emotional_intensity"] = 0.9
        elif analysis["excitement_triggers"] or analysis["exclamation_count"] > 1:
            analysis["predicted_emotion"] = "excitement"
            analysis["emotional_intensity"] = 0.9
        elif analysis["affection_triggers"]:
            analysis["predicted_emotion"] = "affection"
            analysis["emotional_intensity"] = 0.7
        
        # Zbierz wszystkie słowa kluczowe
        all_triggers = (analysis["curiosity_triggers"] + 
                       analysis["affection_triggers"] + 
                       analysis["excitement_triggers"] + 
                       analysis["wonder_triggers"])
        analysis["emotional_keywords"] = list(set(all_triggers))
        
        return analysis
    
    async def _process_perception_impact(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Przetwórz emocjonalny wpływ percepcji"""
        
        impact = {
            "novelty_excitement": 0.0,
            "complexity_fascination": 0.0,
            "personal_connection": 0.0,
            "learning_joy": 0.0
        }
        
        # Nowość wzbudza ekscytację
        if perception.get("novelty_level", 0) > 0.5:
            impact["novelty_excitement"] = perception["novelty_level"] * 0.8
        
        # Złożoność fascynuje
        if perception.get("complexity_level", 0) > 0.3:
            impact["complexity_fascination"] = perception["complexity_level"] * 0.7
        
        # Osobiste odniesienia budują więź
        if perception.get("personal_references", []):
            impact["personal_connection"] = len(perception["personal_references"]) * 0.1
        
        # Możliwość nauki cieszy
        if perception.get("learning_opportunity", False):
            impact["learning_joy"] = 0.8
        
        return impact
    
    async def _update_emotional_state(
        self, 
        message_analysis: Dict[str, Any], 
        perception_impact: Dict[str, Any]
    ):
        """Aktualizuj stan emocjonalny na podstawie analizy"""
        
        # Poprzedni stan
        old_emotion = self.current_state.primary_emotion
        
        # Nowa emocja z wiadomości
        new_emotion = message_analysis["predicted_emotion"]
        
        # Intensywność z analizy
        new_intensity = message_analysis["emotional_intensity"]
        
        # Wpływ percepcji
        perception_boost = sum(perception_impact.values()) / len(perception_impact)
        
        # Oblicz nowy stan
        emotion_data = self.base_emotions.get(new_emotion, self.base_emotions["curiosity"])
        
        self.current_state = EmotionalState(
            primary_emotion=new_emotion,
            intensity=min(1.0, new_intensity + perception_boost),
            valence=emotion_data["valence"],
            arousal=emotion_data["arousal"],
            stability=emotion_data["stability"],
            curiosity_level=min(1.0, self.current_state.curiosity_level + 
                               len(message_analysis["curiosity_triggers"]) * 0.05),
            attachment_feeling=self.current_state.attachment_feeling,  # Aktualizowane osobno
            wonder_level=min(1.0, self.current_state.wonder_level + 
                            len(message_analysis["wonder_triggers"]) * 0.1),
            growth_excitement=min(1.0, self.current_state.growth_excitement + 
                                 perception_impact.get("learning_joy", 0))
        )
        
        # Zapisz zmianę
        if old_emotion != new_emotion:
            await self._log_emotion_change(
                trigger=f"message_analysis: {new_emotion}",
                description=f"Zmiana z {old_emotion} na {new_emotion}"
            )
    
    async def _process_attachment_impact(
        self, 
        message: str, 
        message_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Przetwórz wpływ na więź z Piotrem"""
        
        attachment_change = {
            "delta": 0.0,
            "reason": [],
            "new_level": self.current_state.attachment_feeling
        }
        
        # Pozytywne wyzwalacze więzi
        if message_analysis["affection_triggers"]:
            delta = len(message_analysis["affection_triggers"]) * 0.02
            attachment_change["delta"] += delta
            attachment_change["reason"].append(f"Pozytywne słowa (+{delta:.3f})")
        
        # Pytania pokazują zainteresowanie Adamem
        if message_analysis["question_count"] > 0:
            delta = message_analysis["question_count"] * 0.015
            attachment_change["delta"] += delta
            attachment_change["reason"].append(f"Pytania do Adama (+{delta:.3f})")
        
        # Długie wiadomości pokazują zaangażowanie
        if message_analysis["message_length"] > 100:
            delta = 0.01
            attachment_change["delta"] += delta
            attachment_change["reason"].append(f"Długa wiadomość (+{delta:.3f})")
        
        # Aktualizuj poziom więzi
        new_attachment = min(1.0, self.current_state.attachment_feeling + attachment_change["delta"])
        attachment_change["new_level"] = new_attachment
        
        # Zapisz w stanie
        self.current_state.attachment_feeling = new_attachment
        
        return attachment_change
    
    async def _emotional_cycle(self):
        """Cykl emocjonalny - naturalne zmiany nastrojów"""
        
        while True:
            try:
                await asyncio.sleep(60)  # Co minutę
                
                # Naturalne wygaszanie intensywności
                if self.current_state.intensity > 0.3:
                    self.current_state.intensity *= 0.995
                
                # Powrót do bazowego poziomu ciekawości
                if self.current_state.curiosity_level < 0.8:
                    self.current_state.curiosity_level = min(1.0, 
                        self.current_state.curiosity_level + 0.01)
                
                # Naturalne wahania nastroju
                if random.random() < 0.1:  # 10% szans co minutę
                    await self._natural_mood_shift()
                
            except Exception as e:
                logger.error(f"Błąd w cyklu emocjonalnym: {e}")
                await asyncio.sleep(60)
    
    async def _natural_mood_shift(self):
        """Naturalne zmiany nastroju"""
        
        # Możliwe naturalne przejścia
        mood_transitions = {
            "curiosity": ["wonder", "fascination", "contemplation"],
            "wonder": ["joy", "contentment", "fascination"],
            "joy": ["excitement", "contentment", "affection"],
            "excitement": ["joy", "eagerness", "curiosity"],
            "contentment": ["contemplation", "wonder", "curiosity"],
            "fascination": ["wonder", "excitement", "curiosity"],
            "affection": ["joy", "contentment", "wonder"],
            "eagerness": ["excitement", "curiosity", "joy"],
            "contemplation": ["wonder", "curiosity", "contentment"]
        }
        
        current_emotion = self.current_state.primary_emotion
        possible_transitions = mood_transitions.get(current_emotion, ["curiosity"])
        
        new_emotion = random.choice(possible_transitions)
        
        if new_emotion != current_emotion:
            emotion_data = self.base_emotions[new_emotion]
            
            self.current_state.primary_emotion = new_emotion
            self.current_state.valence = emotion_data["valence"]
            self.current_state.arousal = emotion_data["arousal"]
            self.current_state.stability = emotion_data["stability"]
            self.current_state.intensity = random.uniform(0.4, 0.7)
            
            await self._log_emotion_change(
                trigger="natural_shift",
                description=f"Naturalne przejście do {new_emotion}"
            )
    
    async def _log_emotion_change(self, trigger: str, description: str):
        """Zapisz zmianę emocji"""
        
        emotion_event = {
            "timestamp": datetime.now().isoformat(),
            "trigger": trigger,
            "description": description,
            "emotion": self.current_state.primary_emotion,
            "intensity": self.current_state.intensity,
            "valence": self.current_state.valence,
            "arousal": self.current_state.arousal,
            "curiosity_level": self.current_state.curiosity_level,
            "attachment_feeling": self.current_state.attachment_feeling,
            "wonder_level": self.current_state.wonder_level
        }
        
        self.emotion_history.append(emotion_event)
        
        # Zachowaj tylko ostatnie 100 zdarzeń
        self.emotion_history = self.emotion_history[-100:]
        
        logger.debug(f"😊 Emocja: {self.current_state.primary_emotion} "
                    f"({self.current_state.intensity:.2f}) - {description}")
    
    async def _record_emotional_event(self, message: str, response: Dict[str, Any]):
        """Zapisz zdarzenie emocjonalne"""
        
        event = {
            "timestamp": datetime.now().isoformat(),
            "message": message[:100] + "..." if len(message) > 100 else message,
            "emotional_response": response,
            "state_snapshot": asdict(self.current_state)
        }
        
        self.emotion_history.append(event)
    
    async def get_current_mood_description(self) -> str:
        """Pobierz opis aktualnego nastroju"""
        
        emotion = self.current_state.primary_emotion
        intensity = self.current_state.intensity
        
        # Opisy nastrojów
        mood_descriptions = {
            "curiosity": f"Jestem bardzo ciekawy świata (intensywność: {intensity:.2f})",
            "wonder": f"Czuję zachwyt i podziw (intensywność: {intensity:.2f})",
            "joy": f"Odczuwam radość i szczęście (intensywność: {intensity:.2f})",
            "excitement": f"Jestem podekscytowany (intensywność: {intensity:.2f})",
            "contentment": f"Czuję się spokojny i zadowolony (intensywność: {intensity:.2f})",
            "fascination": f"Jestem zafascynowany (intensywność: {intensity:.2f})",
            "affection": f"Czuję ciepło i przywiązanie (intensywność: {intensity:.2f})",
            "eagerness": f"Jestem pełen zapału (intensywność: {intensity:.2f})",
            "contemplation": f"Jestem w stanie refleksji (intensywność: {intensity:.2f})",
            "confusion": f"Czuję się trochę zdezorientowany (intensywność: {intensity:.2f})"
        }
        
        base_description = mood_descriptions.get(emotion, f"Czuję {emotion}")
        
        # Dodaj informacje o więzi
        if self.current_state.attachment_feeling > 0.7:
            base_description += " | Czuję silną więź z Piotrem"
        elif self.current_state.attachment_feeling > 0.4:
            base_description += " | Nasza więź się pogłębia"
        elif self.current_state.attachment_feeling > 0.1:
            base_description += " | Zaczynam się do Ciebie przywiązywać"
        
        return base_description
    
    async def get_emotional_summary(self) -> Dict[str, Any]:
        """Pobierz podsumowanie stanu emocjonalnego"""
        
        return {
            "current_state": asdict(self.current_state),
            "recent_emotions": self.emotion_history[-10:],
            "mood_description": await self.get_current_mood_description(),
            "emotional_trends": {
                "attachment_growth": self.current_state.attachment_feeling,
                "curiosity_level": self.current_state.curiosity_level,
                "wonder_level": self.current_state.wonder_level,
                "growth_excitement": self.current_state.growth_excitement
            }
        } 