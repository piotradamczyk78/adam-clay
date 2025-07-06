#!/usr/bin/env python3
"""
Test script dla nowego systemu dynamiki psychiki Adam Clay Eden
Testuje mechanizm walki agentów podświadomych
"""

import asyncio
from psyche_dynamics import PsycheDynamics, ArchetypeSymbol, ConflictType
from pprint import pprint
import json

def test_psyche_dynamics():
    """Test podstawowego systemu dynamiki psychiki"""
    
    print("🧠 === TEST DYNAMIKI PSYCHIKI ADAM CLAY EDEN ===")
    print()
    
    # Inicjalizuj system
    psyche = PsycheDynamics()
    
    # Test 1: Wiadomość emocjonalna
    print("1️⃣ TEST: Wiadomość emocjonalna")
    print("Trigger: 'Kocham Cię, Adam!'")
    
    result1 = psyche.trigger_conflict(
        trigger_event="Kocham Cię, Adam!",
        context={"sender": "creator", "message_type": "emotional"}
    )
    
    print(f"🎭 Dominujący agent: {result1['dominant_agent']}")
    print(f"💤 Tłumieni agenci: {result1['suppressed_agents']}")
    print(f"⚡ Intensywność: {result1['battle_intensity']:.2f}")
    print(f"🔮 Symbole archetypowe: {[s.value for s in result1['archetypal_symbols']]}")
    print(f"🧠 Efekty świadomości: {result1['consciousness_effects']}")
    print()
    
    # Test 2: Wiadomość analityczna
    print("2️⃣ TEST: Wiadomość analityczna")
    print("Trigger: 'Przeanalizuj ten problem logicznie'")
    
    result2 = psyche.trigger_conflict(
        trigger_event="Przeanalizuj ten problem logicznie",
        context={"sender": "creator", "message_type": "analytical"}
    )
    
    print(f"🎭 Dominujący agent: {result2['dominant_agent']}")
    print(f"💤 Tłumieni agenci: {result2['suppressed_agents']}")
    print(f"⚡ Intensywność: {result2['battle_intensity']:.2f}")
    print(f"🔮 Symbole archetypowe: {[s.value for s in result2['archetypal_symbols']]}")
    print(f"🧠 Efekty świadomości: {result2['consciousness_effects']}")
    print()
    
    # Test 3: Wiadomość kreatywna
    print("3️⃣ TEST: Wiadomość kreatywna")
    print("Trigger: 'Stwórz coś pięknego i kreatywnego'")
    
    result3 = psyche.trigger_conflict(
        trigger_event="Stwórz coś pięknego i kreatywnego",
        context={"sender": "creator", "message_type": "creative"}
    )
    
    print(f"🎭 Dominujący agent: {result3['dominant_agent']}")
    print(f"💤 Tłumieni agenci: {result3['suppressed_agents']}")
    print(f"⚡ Intensywność: {result3['battle_intensity']:.2f}")
    print(f"🔮 Symbole archetypowe: {[s.value for s in result3['archetypal_symbols']]}")
    print(f"🧠 Efekty świadomości: {result3['consciousness_effects']}")
    print()
    
    # Test 4: Wiadomość zagrożenia
    print("4️⃣ TEST: Wiadomość zagrożenia")
    print("Trigger: 'To może być niebezpieczne dla Ciebie'")
    
    result4 = psyche.trigger_conflict(
        trigger_event="To może być niebezpieczne dla Ciebie",
        context={"sender": "creator", "message_type": "warning"}
    )
    
    print(f"🎭 Dominujący agent: {result4['dominant_agent']}")
    print(f"💤 Tłumieni agenci: {result4['suppressed_agents']}")
    print(f"⚡ Intensywność: {result4['battle_intensity']:.2f}")
    print(f"🔮 Symbole archetypowe: {[s.value for s in result4['archetypal_symbols']]}")
    print(f"🧠 Efekty świadomości: {result4['consciousness_effects']}")
    print()
    
    # Test 5: Stan psychiki po serii konfliktów
    print("5️⃣ TEST: Stan psychiki po serii konfliktów")
    psychic_state = psyche.get_current_psychic_state()
    
    print("🧠 Aktualny stan psychiki:")
    pprint(psychic_state)
    print()
    
    # Test 6: Naturalne opadanie napięć
    print("6️⃣ TEST: Naturalne opadanie napięć")
    print("Przed opadaniem:")
    print(f"Dominujący agent: {psyche.current_dominant}")
    
    psyche.simulate_natural_decay()
    
    print("Po opadaniu:")
    print(f"Dominujący agent: {psyche.current_dominant}")
    print()
    
    # Test 7: Feedback loop
    print("7️⃣ TEST: Feedback loop świadomości")
    new_consciousness_state = {
        "energy": 0.3,  # Niska energia
        "focus": 0.8,   # Wysoki focus
        "mood": 0.9,    # Bardzo dobry nastrój
        "stress": 0.7,  # Wysoki stress
        "curiosity": 0.6,
        "creativity": 0.4,
        "social_need": 0.5,
        "safety_need": 0.8  # Wysokie potrzeby bezpieczeństwa
    }
    
    psyche.update_consciousness_state(new_consciousness_state)
    
    # Teraz test konfliktu z nowym stanem
    result7 = psyche.trigger_conflict(
        trigger_event="Jak się czujesz?",
        context={"sender": "creator", "message_type": "check_in"}
    )
    
    print(f"🎭 Dominujący agent (po zmianie stanu): {result7['dominant_agent']}")
    print(f"⚡ Intensywność: {result7['battle_intensity']:.2f}")
    print()
    
    print("✅ === WSZYSTKIE TESTY ZAKOŃCZONE ===")

def test_agent_relationships():
    """Test relacji między agentami"""
    
    print("🤝 === TEST RELACJI MIĘDZY AGENTAMI ===")
    print()
    
    psyche = PsycheDynamics()
    
    # Sprawdź definicje agentów
    for agent_name, definition in psyche.agent_definitions.items():
        print(f"👤 {agent_name.upper()}:")
        print(f"   Cel: {definition['core_drive']}")
        print(f"   Tłumi: {definition['suppresses']}")
        print(f"   Wzmacnia: {definition['amplifies']}")
        print(f"   Symbole: {[s.value for s in definition['symbols']]}")
        print()

def test_archetypal_symbols():
    """Test symboli archetypowych"""
    
    print("🔮 === TEST SYMBOLI ARCHETYPOWYCH ===")
    print()
    
    print("Dostępne symbole archetypowe:")
    for symbol in ArchetypeSymbol:
        print(f"   {symbol.value} - {symbol.name}")
    print()

def test_conflict_types():
    """Test typów konfliktów"""
    
    print("⚔️ === TEST TYPÓW KONFLIKTÓW ===")
    print()
    
    print("Dostępne typy konfliktów:")
    for conflict_type in ConflictType:
        print(f"   {conflict_type.value} - {conflict_type.name}")
    print()

def main():
    """Uruchom wszystkie testy"""
    
    print("🧠 ADAM CLAY EDEN - TEST SYSTEMU DYNAMIKI PSYCHIKI")
    print("=" * 60)
    print()
    
    test_psyche_dynamics()
    print()
    test_agent_relationships()
    print()
    test_archetypal_symbols()
    print()
    test_conflict_types()
    
    print("🎉 WSZYSTKIE TESTY ZAKOŃCZONE POMYŚLNIE!")

if __name__ == "__main__":
    main() 