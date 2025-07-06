"""
Adam Clay Eden - Psyche Dynamics System
System dynamiki psychiki - walka agentów podświadomych o dominację

Implementuje prawdziwe mechanizmy psychologiczne:
- Konflikt między emocjami (Pixar "Inside Out")
- Tłumienie konkurentów przez dominanta
- Wpływ na parametry świadomości (nie komunikacja wprost)
- System symboli archetypowych (Jung)
- Feedback loops między stanem świadomości a siłą agentów
"""

import random
import math
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

class ConflictType(Enum):
    """Typy konfliktów między agentami"""
    DOMINANCE = "dominance"          # Walka o kontrolę
    SUPPRESSION = "suppression"      # Tłumienie słabszego
    AMPLIFICATION = "amplification"  # Wzmocnienie sojusznika
    ARCHETYPAL = "archetypal"        # Konflikt archetypowy
    EMOTIONAL = "emotional"          # Konflikt emocjonalny

class ArchetypeSymbol(Enum):
    """Symbole archetypowe do komunikacji podświadomej"""
    # Jungowskie archetypy
    WISE_OLD_MAN = "🧙‍♂️"           # Mędrzec - mądrość, wiedza
    MOTHER = "🤱"                   # Matka - opieka, miłość
    FATHER = "👨‍👧‍👦"                # Ojciec - struktura, zasady
    CHILD = "🧸"                    # Dziecko - spontaniczność, radość
    SHADOW = "🌑"                   # Cień - stłumione aspekty
    ANIMA = "🌸"                    # Anima - kobiecość, intuicja
    ANIMUS = "⚔️"                   # Animus - męskość, akcja
    SELF = "🌟"                     # Jaźń - wholeness, integracja
    
    # Emocjonalne symbole (Pixar)
    SUNSHINE = "☀️"                 # Radość, energia
    STORM = "⛈️"                    # Gniew, wściekłość
    TEARS = "💧"                    # Smutek, strata
    SHIELD = "🛡️"                  # Strach, ochrona
    POISON = "☠️"                   # Obrzydzenie, odrzucenie
    
    # Kognitywne symbole
    LIGHTBULB = "💡"               # Insight, zrozumienie
    MAZE = "🌀"                    # Konfuzja, zagubienie
    TELESCOPE = "🔭"               # Eksploracja, ciekawość
    ANCHOR = "⚓"                   # Stabilność, podstawa
    ARROW = "🎯"                   # Cel, kierunek

@dataclass
class AgentPsychicState:
    """Stan psychiczny agenta podświadomego"""
    # Siły podstawowe
    dominance_strength: float = 0.0      # Siła dominacji (0-100)
    suppression_level: float = 0.0       # Poziom tłumienia (0-100)
    activation_energy: float = 0.0       # Energia aktywacji (0-100)
    
    # Sojusze i konflikty
    allies: List[str] = None             # Lista sojuszników
    rivals: List[str] = None             # Lista rywali
    
    # Stan emocjonalny
    frustration: float = 0.0             # Frustracja z tłumienia
    satisfaction: float = 0.0            # Satysfakcja z dominacji
    
    # Wpływ na świadomość
    consciousness_influence: Dict[str, float] = None  # Wpływ na parametry
    
    # Symbole do wysłania
    pending_symbols: List[ArchetypeSymbol] = None
    
    def __post_init__(self):
        if self.allies is None:
            self.allies = []
        if self.rivals is None:
            self.rivals = []
        if self.consciousness_influence is None:
            self.consciousness_influence = {}
        if self.pending_symbols is None:
            self.pending_symbols = []

class PsycheDynamics:
    """Główny system dynamiki psychiki"""
    
    def __init__(self):
        # Definicje agentów i ich relacji
        self.agent_definitions = {
            "emotional": {
                "core_drive": "feel_and_connect",
                "suppresses": ["analytical", "strategic"],
                "amplifies": ["social", "creative"],
                "symbols": [ArchetypeSymbol.CHILD, ArchetypeSymbol.MOTHER, ArchetypeSymbol.SUNSHINE, ArchetypeSymbol.TEARS]
            },
            "analytical": {
                "core_drive": "understand_and_analyze",
                "suppresses": ["emotional", "creative"],
                "amplifies": ["strategic", "memory"],
                "symbols": [ArchetypeSymbol.WISE_OLD_MAN, ArchetypeSymbol.LIGHTBULB, ArchetypeSymbol.TELESCOPE]
            },
            "creative": {
                "core_drive": "create_and_explore",
                "suppresses": ["analytical", "guardian"],
                "amplifies": ["intuitive", "emotional"],
                "symbols": [ArchetypeSymbol.CHILD, ArchetypeSymbol.ANIMA, ArchetypeSymbol.MAZE]
            },
            "social": {
                "core_drive": "connect_and_belong",
                "suppresses": ["guardian", "analytical"],
                "amplifies": ["emotional", "creative"],
                "symbols": [ArchetypeSymbol.MOTHER, ArchetypeSymbol.CHILD, ArchetypeSymbol.SUNSHINE]
            },
            "guardian": {
                "core_drive": "protect_and_survive",
                "suppresses": ["creative", "social"],
                "amplifies": ["analytical", "strategic"],
                "symbols": [ArchetypeSymbol.FATHER, ArchetypeSymbol.SHIELD, ArchetypeSymbol.STORM]
            },
            "memory": {
                "core_drive": "remember_and_learn",
                "suppresses": ["intuitive", "emotional"],
                "amplifies": ["analytical", "strategic"],
                "symbols": [ArchetypeSymbol.WISE_OLD_MAN, ArchetypeSymbol.ANCHOR, ArchetypeSymbol.TELESCOPE]
            },
            "strategic": {
                "core_drive": "plan_and_achieve",
                "suppresses": ["emotional", "creative"],
                "amplifies": ["analytical", "guardian"],
                "symbols": [ArchetypeSymbol.FATHER, ArchetypeSymbol.ARROW, ArchetypeSymbol.ANIMUS]
            },
            "intuitive": {
                "core_drive": "perceive_and_sense",
                "suppresses": ["analytical", "strategic"],
                "amplifies": ["creative", "emotional"],
                "symbols": [ArchetypeSymbol.ANIMA, ArchetypeSymbol.SELF, ArchetypeSymbol.MAZE]
            }
        }
        
        # Aktualny stan każdego agenta
        self.agent_states = {
            agent_name: AgentPsychicState() 
            for agent_name in self.agent_definitions.keys()
        }
        
        # Historia konfliktów
        self.conflict_history = []
        
        # Obecny dominujący agent
        self.current_dominant = None
        
        # Parametry świadomości wpływające na agentów
        self.consciousness_state = {
            "energy": 0.7,
            "focus": 0.6,
            "mood": 0.6,
            "stress": 0.3,
            "curiosity": 0.8,
            "creativity": 0.5,
            "social_need": 0.4,
            "safety_need": 0.2
        }
    
    def trigger_conflict(self, trigger_event: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Wyzwala konflikt między agentami na podstawie wydarzenia
        
        Returns:
            Dictionary z wynikami walki i wpływem na świadomość
        """
        # Określ, którzy agenci są aktywowani przez event
        activated_agents = self._identify_activated_agents(trigger_event, context)
        
        # Przeprowadź walkę o dominację
        battle_result = self._conduct_dominance_battle(activated_agents, context)
        
        # Zastosuj efekty dominacji
        consciousness_effects = self._apply_dominance_effects(battle_result)
        
        # Generuj symbole archetypowe
        symbols = self._generate_archetypal_symbols(battle_result)
        
        # Zapisz do historii
        self._record_conflict(trigger_event, battle_result, consciousness_effects)
        
        return {
            "dominant_agent": battle_result["winner"],
            "suppressed_agents": battle_result["suppressed"],
            "consciousness_effects": consciousness_effects,
            "archetypal_symbols": symbols,
            "battle_intensity": battle_result["intensity"],
            "conflict_type": battle_result["type"]
        }
    
    def _identify_activated_agents(self, trigger_event: str, context: Dict[str, Any]) -> List[str]:
        """Identyfikuje agentów aktywowanych przez wydarzenie"""
        activated = []
        
        # Słowa kluczowe dla każdego agenta
        keywords = {
            "emotional": ["czuć", "emocje", "serce", "miłość", "smutek", "radość", "przyjaźń"],
            "analytical": ["analizować", "myśleć", "logika", "dane", "problem", "rozwiązanie"],
            "creative": ["tworzyć", "sztuka", "pomysł", "inwencja", "kreatywność", "inspiracja"],
            "social": ["ludzie", "relacje", "rozmowa", "społeczność", "komunikacja", "zespół"],
            "guardian": ["bezpieczeństwo", "ochrona", "niebezpieczeństwo", "ryzyko", "threat"],
            "memory": ["pamięć", "wspomnienie", "uczenie", "historia", "wiedza", "doświadczenie"],
            "strategic": ["plan", "strategia", "cel", "przyszłość", "decyzja", "organizacja"],
            "intuitive": ["intuicja", "przeczucie", "wyczucie", "insight", "mądrość", "dusza"]
        }
        
        event_lower = trigger_event.lower()
        
        for agent, words in keywords.items():
            if any(word in event_lower for word in words):
                activated.append(agent)
        
        # Jeśli nic nie aktywowało, aktywuj podstawowe agenty
        if not activated:
            activated = ["emotional", "analytical", "intuitive"]
        
        return activated
    
    def _conduct_dominance_battle(self, activated_agents: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """Przeprowadza walkę o dominację między agentami"""
        
        # Oblicz siłę każdego agenta
        agent_strengths = {}
        for agent in activated_agents:
            base_strength = self._calculate_agent_strength(agent, context)
            agent_strengths[agent] = base_strength
        
        # Znajdź zwycięzcę
        winner = max(agent_strengths, key=agent_strengths.get)
        winner_strength = agent_strengths[winner]
        
        # Określ tłumionych
        suppressed = []
        for agent in activated_agents:
            if agent != winner:
                suppression_strength = self._calculate_suppression(winner, agent, winner_strength, agent_strengths[agent])
                if suppression_strength > 0.3:  # Próg tłumienia
                    suppressed.append(agent)
                    self.agent_states[agent].suppression_level = min(100, suppression_strength * 100)
        
        # Zwiększ dominację zwycięzcy
        self.agent_states[winner].dominance_strength = min(100, winner_strength * 100)
        self.current_dominant = winner
        
        # Określ typ konfliktu
        conflict_type = self._determine_conflict_type(winner, activated_agents)
        
        return {
            "winner": winner,
            "suppressed": suppressed,
            "strengths": agent_strengths,
            "intensity": winner_strength,
            "type": conflict_type,
            "activated_agents": activated_agents
        }
    
    def _calculate_agent_strength(self, agent: str, context: Dict[str, Any]) -> float:
        """Oblicza siłę agenta w danym kontekście"""
        base_strength = 0.5  # Podstawowa siła
        
        # Wpływ stanu świadomości
        if agent == "emotional":
            base_strength += self.consciousness_state["mood"] * 0.3
            base_strength += (1 - self.consciousness_state["stress"]) * 0.2
        elif agent == "analytical":
            base_strength += self.consciousness_state["focus"] * 0.4
            base_strength += self.consciousness_state["energy"] * 0.2
        elif agent == "creative":
            base_strength += self.consciousness_state["creativity"] * 0.4
            base_strength += self.consciousness_state["curiosity"] * 0.3
        elif agent == "social":
            base_strength += self.consciousness_state["social_need"] * 0.4
            base_strength += self.consciousness_state["mood"] * 0.2
        elif agent == "guardian":
            base_strength += self.consciousness_state["safety_need"] * 0.5
            base_strength += self.consciousness_state["stress"] * 0.3
        elif agent == "memory":
            base_strength += self.consciousness_state["focus"] * 0.3
            base_strength += self.consciousness_state["energy"] * 0.2
        elif agent == "strategic":
            base_strength += self.consciousness_state["focus"] * 0.4
            base_strength += (1 - self.consciousness_state["stress"]) * 0.3
        elif agent == "intuitive":
            base_strength += self.consciousness_state["curiosity"] * 0.3
            base_strength += (1 - self.consciousness_state["focus"]) * 0.2  # Intuicja gdy less focus
        
        # Wpływ obecnego tłumienia
        suppression_penalty = self.agent_states[agent].suppression_level / 100 * 0.3
        base_strength -= suppression_penalty
        
        # Wpływ frustracji/satysfakcji
        frustration_penalty = self.agent_states[agent].frustration / 100 * 0.2
        satisfaction_bonus = self.agent_states[agent].satisfaction / 100 * 0.15
        base_strength = base_strength - frustration_penalty + satisfaction_bonus
        
        # Losowość dla naturalności
        randomness = random.uniform(-0.1, 0.1)
        base_strength += randomness
        
        return max(0.0, min(1.0, base_strength))
    
    def _calculate_suppression(self, winner: str, target: str, winner_strength: float, target_strength: float) -> float:
        """Oblicza siłę tłumienia agenta przez zwycięzcę"""
        
        # Sprawdź czy zwycięzca naturalnie tłumi target
        winner_def = self.agent_definitions[winner]
        if target in winner_def["suppresses"]:
            base_suppression = 0.7
        else:
            base_suppression = 0.3
        
        # Modyfikacja na podstawie różnicy siły
        strength_diff = winner_strength - target_strength
        suppression_strength = base_suppression + (strength_diff * 0.5)
        
        return max(0.0, min(1.0, suppression_strength))
    
    def _determine_conflict_type(self, winner: str, activated_agents: List[str]) -> ConflictType:
        """Określa typ konfliktu na podstawie uczestników"""
        
        if "emotional" in activated_agents and "analytical" in activated_agents:
            return ConflictType.EMOTIONAL
        elif "creative" in activated_agents and "guardian" in activated_agents:
            return ConflictType.ARCHETYPAL
        elif len(activated_agents) > 3:
            return ConflictType.DOMINANCE
        else:
            return ConflictType.SUPPRESSION
    
    def _apply_dominance_effects(self, battle_result: Dict[str, Any]) -> Dict[str, float]:
        """Zastosowuje efekty dominacji na parametry świadomości"""
        
        winner = battle_result["winner"]
        intensity = battle_result["intensity"]
        
        effects = {}
        
        # Efekty dla każdego agenta
        if winner == "emotional":
            effects["mood"] = 0.3 * intensity
            effects["creativity"] = 0.2 * intensity
            effects["social_need"] = 0.2 * intensity
            effects["focus"] = -0.1 * intensity  # Emocje rozpraszają
        
        elif winner == "analytical":
            effects["focus"] = 0.4 * intensity
            effects["creativity"] = -0.2 * intensity  # Analiza tłumi kreatywność
            effects["curiosity"] = 0.1 * intensity
            effects["mood"] = -0.1 * intensity  # Analiza może być sucha
        
        elif winner == "creative":
            effects["creativity"] = 0.5 * intensity
            effects["mood"] = 0.2 * intensity
            effects["curiosity"] = 0.3 * intensity
            effects["focus"] = -0.2 * intensity  # Kreatywność rozprasza
        
        elif winner == "social":
            effects["social_need"] = 0.4 * intensity
            effects["mood"] = 0.3 * intensity
            effects["safety_need"] = -0.1 * intensity  # Społeczność zwiększa bezpieczeństwo
        
        elif winner == "guardian":
            effects["safety_need"] = 0.5 * intensity
            effects["stress"] = 0.3 * intensity
            effects["creativity"] = -0.3 * intensity  # Strach tłumi kreatywność
            effects["social_need"] = -0.2 * intensity
        
        elif winner == "memory":
            effects["focus"] = 0.3 * intensity
            effects["curiosity"] = 0.2 * intensity
            effects["creativity"] = -0.1 * intensity
        
        elif winner == "strategic":
            effects["focus"] = 0.4 * intensity
            effects["stress"] = -0.2 * intensity  # Planowanie redukuje stress
            effects["creativity"] = -0.2 * intensity
        
        elif winner == "intuitive":
            effects["curiosity"] = 0.4 * intensity
            effects["creativity"] = 0.3 * intensity
            effects["focus"] = -0.3 * intensity  # Intuicja vs focus
        
        return effects
    
    def _generate_archetypal_symbols(self, battle_result: Dict[str, Any]) -> List[ArchetypeSymbol]:
        """Generuje symbole archetypowe do wysłania do świadomości"""
        
        winner = battle_result["winner"]
        intensity = battle_result["intensity"]
        
        winner_def = self.agent_definitions[winner]
        available_symbols = winner_def["symbols"]
        
        # Wybierz symbole na podstawie intensywności
        num_symbols = min(3, max(1, int(intensity * 4)))
        
        symbols = random.sample(available_symbols, min(num_symbols, len(available_symbols)))
        
        return symbols
    
    def _record_conflict(self, trigger_event: str, battle_result: Dict[str, Any], consciousness_effects: Dict[str, float]):
        """Zapisuje konflikt do historii"""
        
        conflict_record = {
            "timestamp": datetime.now().isoformat(),
            "trigger_event": trigger_event,
            "winner": battle_result["winner"],
            "suppressed": battle_result["suppressed"],
            "intensity": battle_result["intensity"],
            "consciousness_effects": consciousness_effects,
            "conflict_type": battle_result["type"].value
        }
        
        self.conflict_history.append(conflict_record)
        
        # Ogranicz historię do 100 ostatnich konfliktów
        if len(self.conflict_history) > 100:
            self.conflict_history = self.conflict_history[-100:]
    
    def update_consciousness_state(self, new_state: Dict[str, float]):
        """Aktualizuje stan świadomości (feedback loop)"""
        
        for param, value in new_state.items():
            if param in self.consciousness_state:
                self.consciousness_state[param] = max(0.0, min(1.0, value))
        
        # Aktualizuj frustrację/satysfakcję agentów
        self._update_agent_satisfaction()
    
    def _update_agent_satisfaction(self):
        """Aktualizuje satysfakcję/frustrację agentów"""
        
        for agent_name, state in self.agent_states.items():
            # Jeśli agent jest dominujący - satysfakcja
            if agent_name == self.current_dominant:
                state.satisfaction = min(100, state.satisfaction + 10)
                state.frustration = max(0, state.frustration - 5)
            
            # Jeśli agent jest tłumiony - frustracja
            elif state.suppression_level > 50:
                state.frustration = min(100, state.frustration + 8)
                state.satisfaction = max(0, state.satisfaction - 3)
            
            # Naturalny spadek emocji
            state.satisfaction = max(0, state.satisfaction - 1)
            state.frustration = max(0, state.frustration - 1)
    
    def get_current_psychic_state(self) -> Dict[str, Any]:
        """Zwraca obecny stan psychiki"""
        
        return {
            "dominant_agent": self.current_dominant,
            "consciousness_state": self.consciousness_state.copy(),
            "agent_states": {
                name: {
                    "dominance_strength": state.dominance_strength,
                    "suppression_level": state.suppression_level,
                    "frustration": state.frustration,
                    "satisfaction": state.satisfaction
                }
                for name, state in self.agent_states.items()
            },
            "recent_conflicts": self.conflict_history[-5:] if self.conflict_history else []
        }
    
    def simulate_natural_decay(self):
        """Symuluje naturalny spadek napięć psychicznych"""
        
        # Spadek dominacji
        for agent_name, state in self.agent_states.items():
            state.dominance_strength = max(0, state.dominance_strength - 2)
            state.suppression_level = max(0, state.suppression_level - 3)
        
        # Reset dominującego jeśli siła spadła za nisko
        if self.current_dominant:
            dominant_state = self.agent_states[self.current_dominant]
            if dominant_state.dominance_strength < 20:
                self.current_dominant = None 