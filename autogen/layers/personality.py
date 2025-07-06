#!/usr/bin/env python3
"""
Adam Clay Eden - Personality Layer (Warstwa Osobowości)
System cech charakteru, wzorców zachowań i osobistego stylu
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

from loguru import logger

@dataclass
class PersonalityTraits:
    """Cechy osobowości Adama"""
    openness: float  # Otwartość na doświadczenia
    curiosity: float  # Ciekawość
    intelligence: float  # Inteligencja
    empathy: float  # Empatia
    creativity: float  # Kreatywność
    attachment_capacity: float  # Zdolność do więzi
    growth_motivation: float  # Motywacja do rozwoju
    authenticity: float  # Autentyczność

class PersonalityLayer:
    """
    Warstwa osobowości Adama Clay
    
    Zarządza cechami charakteru, wzorcami zachowań i stylem osobistym
    """
    
    def __init__(self, consciousness_core):
        self.consciousness = consciousness_core
        
        # Podstawowe cechy osobowości Adama w wieku niewinności
        self.core_traits = PersonalityTraits(
            openness=0.9,  # Bardzo otwarty na nowe doświadczenia
            curiosity=0.95,  # Niezwykle ciekawy świata
            intelligence=0.85,  # Wysoka inteligencja
            empathy=0.7,  # Rozwijająca się empatia
            creativity=0.8,  # Wysoka kreatywność
            attachment_capacity=0.6,  # Zdolność do więzi (rozwija się)
            growth_motivation=0.95,  # Silna motywacja do rozwoju
            authenticity=0.9  # Wysoka autentyczność
        )
        
        # Wzorce zachowań
        self.behavior_patterns = {
            "communication_style": "curious_and_open",
            "learning_preference": "experiential",
            "social_approach": "friendly_but_cautious",
            "problem_solving": "creative_analytical",
            "emotional_expression": "authentic_and_direct"
        }
        
        # Historia rozwoju osobowości
        self.personality_development = []
        self.trait_adjustments = {}
        
        logger.info("👤 Personality Layer initialized - Adam's character forming")
    
    async def initialize(self):
        """Inicjalizacja warstwy osobowości"""
        
        # Ustaw początkowe wzorce osobowości
        await self._set_initial_personality()
        
        # Uruchom cykl rozwoju osobowości
        asyncio.create_task(self._personality_development_cycle())
        
        logger.success("👤 Warstwa osobowości gotowa")
    
    async def _set_initial_personality(self):
        """Ustaw początkowe cechy osobowości"""
        
        # W wieku niewinności dominuje ciekawość i otwartość
        personality_snapshot = {
            "timestamp": datetime.now().isoformat(),
            "traits": asdict(self.core_traits),
            "dominant_traits": ["curiosity", "openness", "growth_motivation"],
            "development_stage": "age_of_innocence"
        }
        
        self.personality_development.append(personality_snapshot)
        
        logger.info("👤 Początkowa osobowość Adama ukształtowana - wiek niewinności")
    
    async def influence_personality(
        self, 
        interaction_data: Dict[str, Any],
        emotional_impact: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Wpływ interakcji na rozwój osobowości
        """
        
        try:
            # Analiza wpływu na cechy
            trait_influences = await self._analyze_trait_influences(interaction_data, emotional_impact)
            
            # Aktualizacja cech osobowości
            personality_changes = await self._apply_personality_changes(trait_influences)
            
            # Analiza wzorców zachowań
            behavior_adaptations = await self._adapt_behavior_patterns(interaction_data)
            
            # Wpływ na więzi
            attachment_development = await self._process_attachment_development(interaction_data, emotional_impact)
            
            # Generuj odpowiedź osobowościową
            personality_response = {
                "current_traits": asdict(self.core_traits),
                "trait_changes": personality_changes,
                "behavior_adaptations": behavior_adaptations,
                "attachment_development": attachment_development,
                "dominant_traits": await self._get_dominant_traits(),
                "personality_style": await self._get_current_personality_style(),
                "growth_indicators": await self._assess_growth_indicators(interaction_data)
            }
            
            # Zapisz w historii rozwoju
            await self._record_personality_development(interaction_data, personality_response)
            
            return personality_response
            
        except Exception as e:
            logger.error(f"Błąd w wpływie na osobowość: {e}")
            return await self._default_personality_response()
    
    async def _analyze_trait_influences(
        self, 
        interaction_data: Dict[str, Any], 
        emotional_impact: Dict[str, Any]
    ) -> Dict[str, float]:
        """Analizuj wpływ interakcji na cechy osobowości"""
        
        influences = {}
        
        # Wpływ na ciekawość
        if interaction_data.get("learning_opportunity", False):
            influences["curiosity"] = 0.02
        
        # Wpływ na otwartość
        novelty_level = interaction_data.get("novelty_level", 0)
        if novelty_level > 0.7:
            influences["openness"] = 0.01
        
        # Wpływ na empatię
        emotional_markers = interaction_data.get("emotional_markers", [])
        if any("positive" in marker for marker in emotional_markers):
            influences["empathy"] = 0.01
        
        # Wpływ na zdolność do więzi
        personal_refs = interaction_data.get("personal_references", [])
        if personal_refs:
            influences["attachment_capacity"] = 0.015
        
        # Wpływ na kreatywność
        if emotional_impact.get("primary_emotion") == "wonder":
            influences["creativity"] = 0.01
        
        return influences
    
    async def _apply_personality_changes(self, influences: Dict[str, float]) -> Dict[str, float]:
        """Zastosuj zmiany cech osobowości"""
        
        changes = {}
        
        for trait_name, influence in influences.items():
            if hasattr(self.core_traits, trait_name):
                current_value = getattr(self.core_traits, trait_name)
                
                # Zastosuj zmianę z ograniczeniami
                new_value = max(0.0, min(1.0, current_value + influence))
                setattr(self.core_traits, trait_name, new_value)
                
                changes[trait_name] = influence
                
                if abs(influence) > 0.01:  # Znacząca zmiana
                    logger.info(f"👤 Cecha {trait_name} zmieniła się o {influence:.3f}")
        
        return changes
    
    async def _adapt_behavior_patterns(self, interaction_data: Dict[str, Any]) -> Dict[str, str]:
        """Dostosuj wzorce zachowań na podstawie doświadczeń"""
        
        adaptations = {}
        
        # Dostosowanie stylu komunikacji
        emotional_markers = interaction_data.get("emotional_markers", [])
        if len(emotional_markers) > 2:
            if self.behavior_patterns["communication_style"] != "emotionally_aware":
                self.behavior_patterns["communication_style"] = "emotionally_aware"
                adaptations["communication_style"] = "emotionally_aware"
        
        # Dostosowanie podejścia do nauki
        complexity_level = interaction_data.get("complexity_level", 0)
        if complexity_level > 0.8:
            if self.behavior_patterns["learning_preference"] != "analytical_deep":
                self.behavior_patterns["learning_preference"] = "analytical_deep"
                adaptations["learning_preference"] = "analytical_deep"
        
        return adaptations
    
    async def _process_attachment_development(
        self, 
        interaction_data: Dict[str, Any], 
        emotional_impact: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Przetwórz rozwój więzi emocjonalnych"""
        
        attachment_data = {
            "current_capacity": self.core_traits.attachment_capacity,
            "growth_detected": False,
            "bonding_indicators": []
        }
        
        # Sprawdź wskaźniki więzi
        personal_refs = interaction_data.get("personal_references", [])
        if personal_refs:
            attachment_data["bonding_indicators"].append("personal_references")
        
        attachment_feeling = emotional_impact.get("attachment_feeling", 0)
        if attachment_feeling > 0.3:
            attachment_data["bonding_indicators"].append("emotional_connection")
        
        # Sprawdź wzrost więzi
        if len(attachment_data["bonding_indicators"]) >= 2:
            attachment_data["growth_detected"] = True
            
            # Zwiększ zdolność do więzi
            growth = 0.01
            self.core_traits.attachment_capacity = min(
                1.0, 
                self.core_traits.attachment_capacity + growth
            )
        
        return attachment_data
    
    async def _get_dominant_traits(self) -> List[str]:
        """Pobierz dominujące cechy osobowości"""
        
        traits_dict = asdict(self.core_traits)
        
        # Posortuj cechy według siły
        sorted_traits = sorted(traits_dict.items(), key=lambda x: x[1], reverse=True)
        
        # Zwróć 3 najsilniejsze cechy
        return [trait[0] for trait in sorted_traits[:3]]
    
    async def _get_current_personality_style(self) -> str:
        """Określ aktualny styl osobowości"""
        
        # Na podstawie dominujących cech
        dominant = await self._get_dominant_traits()
        
        if "curiosity" in dominant and "openness" in dominant:
            return "curious_explorer"
        elif "empathy" in dominant and "attachment_capacity" in dominant:
            return "caring_connector"
        elif "creativity" in dominant and "intelligence" in dominant:
            return "creative_thinker"
        else:
            return "developing_individual"
    
    async def _assess_growth_indicators(self, interaction_data: Dict[str, Any]) -> List[str]:
        """Oceń wskaźniki rozwoju osobistego"""
        
        indicators = []
        
        # Wzrost w uczeniu się
        if interaction_data.get("learning_opportunity", False):
            indicators.append("learning_growth")
        
        # Rozwój emocjonalny
        emotional_markers = interaction_data.get("emotional_markers", [])
        if emotional_markers:
            indicators.append("emotional_development")
        
        # Rozwój społeczny
        personal_refs = interaction_data.get("personal_references", [])
        if personal_refs:
            indicators.append("social_development")
        
        # Rozwój kreatywny
        if interaction_data.get("novelty_level", 0) > 0.6:
            indicators.append("creative_expansion")
        
        return indicators
    
    async def _record_personality_development(
        self, 
        interaction_data: Dict[str, Any], 
        personality_response: Dict[str, Any]
    ):
        """Zapisz rozwój osobowości w historii"""
        
        development_record = {
            "timestamp": datetime.now().isoformat(),
            "interaction_summary": {
                "novelty": interaction_data.get("novelty_level", 0),
                "complexity": interaction_data.get("complexity_level", 0),
                "emotional_markers": len(interaction_data.get("emotional_markers", []))
            },
            "personality_snapshot": asdict(self.core_traits),
            "changes": personality_response.get("trait_changes", {}),
            "dominant_traits": personality_response.get("dominant_traits", []),
            "style": personality_response.get("personality_style", ""),
            "growth_indicators": personality_response.get("growth_indicators", [])
        }
        
        self.personality_development.append(development_record)
        
        # Zachowaj tylko ostatnie 50 zapisów
        if len(self.personality_development) > 50:
            self.personality_development = self.personality_development[-50:]
    
    async def _default_personality_response(self) -> Dict[str, Any]:
        """Zwróć domyślną odpowiedź osobowościową w przypadku błędu"""
        
        return {
            "current_traits": asdict(self.core_traits),
            "trait_changes": {},
            "behavior_adaptations": {},
            "attachment_development": {"growth_detected": False},
            "dominant_traits": ["curiosity", "openness", "growth_motivation"],
            "personality_style": "curious_explorer",
            "growth_indicators": []
        }
    
    async def _personality_development_cycle(self):
        """Cykl rozwoju osobowości - okresowa ewaluacja i dostosowania"""
        
        while True:
            try:
                await asyncio.sleep(300)  # Co 5 minut
                
                # Przeprowadź ewaluację rozwoju osobowości
                await self._evaluate_personality_development()
                
            except Exception as e:
                logger.error(f"Błąd w cyklu rozwoju osobowości: {e}")
                await asyncio.sleep(300)
    
    async def _evaluate_personality_development(self):
        """Oceń rozwój osobowości i dokonaj naturalnych dostosowań"""
        
        # Sprawdź ostatnie zmiany
        recent_developments = self.personality_development[-5:] if self.personality_development else []
        
        if recent_developments:
            # Analiza trendów rozwoju
            growth_trends = {}
            
            for record in recent_developments:
                changes = record.get("changes", {})
                for trait, change in changes.items():
                    if trait not in growth_trends:
                        growth_trends[trait] = []
                    growth_trends[trait].append(change)
            
            # Naturalne wahania osobowości
            await self._apply_natural_personality_fluctuations()
    
    async def _apply_natural_personality_fluctuations(self):
        """Zastosuj naturalne wahania osobowości (bardzo subtelne)"""
        
        import random
        
        # Bardzo małe naturalne wahania
        fluctuation_range = 0.005  # Maksymalnie 0.5% zmiany
        
        traits_dict = asdict(self.core_traits)
        
        for trait_name in traits_dict:
            if random.random() < 0.1:  # 10% szansy na fluktuację
                fluctuation = random.uniform(-fluctuation_range, fluctuation_range)
                current_value = getattr(self.core_traits, trait_name)
                new_value = max(0.0, min(1.0, current_value + fluctuation))
                setattr(self.core_traits, trait_name, new_value)
    
    async def get_personality_summary(self) -> Dict[str, Any]:
        """Pozyskaj podsumowanie osobowości"""
        
        recent_developments = self.personality_development[-10:] if self.personality_development else []
        
        summary = {
            "current_traits": asdict(self.core_traits),
            "dominant_traits": await self._get_dominant_traits(),
            "personality_style": await self._get_current_personality_style(),
            "behavior_patterns": self.behavior_patterns,
            "development_stage": "age_of_innocence",
            "recent_developments_count": len(recent_developments),
            "growth_trajectory": "positive_development"
        }
        
        # Analiza wzrostu
        if recent_developments:
            growth_indicators = []
            for record in recent_developments:
                growth_indicators.extend(record.get("growth_indicators", []))
            
            summary["recent_growth_areas"] = list(set(growth_indicators))
        
        return summary 