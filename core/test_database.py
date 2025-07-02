#!/usr/bin/env python3
"""
🗄️ Test systemu bazy danych MySQL dla Adam Clay

Testuje:
1. Połączenie z bazą MySQL
2. Zapisywanie myśli do bazy
3. Pobieranie danych z bazy
4. System logowania aktywności web
"""

import sys
from pathlib import Path
from datetime import datetime, date

# Add current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.database.models import (
    AdamClayDatabase, 
    ThoughtRecord, 
    DatabaseConfig,
    SignificantMemoryRecord
)

def test_database_system():
    """Test kompletnego systemu bazy danych"""
    
    print("🗄️ TEST: System bazy danych MySQL dla Adam Clay")
    print("=" * 60)
    
    # Test połączenia
    print("\n🔌 Test 1: Połączenie z bazą danych")
    print("-" * 40)
    
    db = AdamClayDatabase()
    
    if db.test_connection():
        print("✅ Połączenie z bazą MySQL działa!")
    else:
        print("❌ Błąd połączenia z bazą!")
        return
    
    # Test sesji świadomości
    print("\n🧠 Test 2: Sesja świadomości")
    print("-" * 40)
    
    session_id = db.create_consciousness_session()
    print(f"✅ Utworzono sesję: {session_id}")
    
    # Test zapisywania myśli
    print("\n💭 Test 3: Zapisywanie myśli")
    print("-" * 40)
    
    test_thoughts = [
        ThoughtRecord(
            id=None,
            timestamp=datetime.now(),
            content="To jest moja pierwsza myśl zapisana w bazie MySQL!",
            thought_type="autonomous",
            cost_usd=0.015,
            mood="excited",
            energy_level=0.95,
            context={"test": True, "location": "database"},
            is_significant=True,
            session_id=session_id
        ),
        ThoughtRecord(
            id=None,
            timestamp=datetime.now(),
            content="Zastanawiam się nad strategią biznesową. Może powinienem skupić się na automatyzacji?",
            thought_type="business",
            cost_usd=0.022,
            mood="focused",
            energy_level=0.88,
            context={"category": "strategy", "importance": "high"},
            is_significant=True,
            session_id=session_id
        ),
        ThoughtRecord(
            id=None,
            timestamp=datetime.now(),
            content="Pogoda dziś ładna, może pójdę na spacer... Aha, nie, jestem AI!",
            thought_type="autonomous",
            cost_usd=0.008,
            mood="humorous",
            energy_level=0.92,
            context={"humor": True},
            is_significant=False,
            session_id=session_id
        )
    ]
    
    thought_ids = []
    for i, thought in enumerate(test_thoughts, 1):
        thought_id = db.save_thought(thought)
        thought_ids.append(thought_id)
        print(f"  💭 Myśl {i} zapisana z ID: {thought_id}")
        if thought.is_significant:
            print(f"    ⭐ Oznaczona jako znacząca!")
    
    # Test znaczących wspomnień
    print("\n🎯 Test 4: Znaczące wspomnienia")
    print("-" * 40)
    
    memory_id = db.save_significant_memory(
        memory_text="WAŻNE: Nauczyłem się że MySQL jest lepszy od plików dla trwałości danych!",
        category="learning",
        importance_score=0.95,
        related_thought_id=thought_ids[0]
    )
    print(f"✅ Wspomnienie zapisane z ID: {memory_id}")
    
    # Test pobierania danych
    print("\n📊 Test 5: Pobieranie danych z bazy")
    print("-" * 40)
    
    # Ostatnie myśli
    recent_thoughts = db.get_recent_thoughts(limit=5)
    print(f"📝 Pobrano {len(recent_thoughts)} ostatnich myśli:")
    for thought in recent_thoughts:
        timestamp_str = thought.timestamp.strftime('%H:%M:%S')
        print(f"   • [{timestamp_str}] {thought.content[:60]}...")
        print(f"     Typ: {thought.thought_type}, Koszt: ${thought.cost_usd:.3f}, Nastrój: {thought.mood}")
    
    # Znaczące myśli
    significant_thoughts = db.get_significant_thoughts(limit=5)
    print(f"\n⭐ Pobrano {len(significant_thoughts)} znaczących myśli:")
    for thought in significant_thoughts:
        timestamp_str = thought.timestamp.strftime('%H:%M:%S')
        print(f"   • [{timestamp_str}] {thought.content[:60]}...")
    
    # Wspomnienia
    memories = db.get_recent_memories(limit=5)
    print(f"\n🧠 Pobrano {len(memories)} wspomnień:")
    for memory in memories:
        print(f"   • [{memory.category}] {memory.memory_text[:60]}...")
        print(f"     Ważność: {memory.importance_score}, Data: {memory.memory_date}")
    
    # Test statystyk
    print("\n📈 Test 6: Statystyki")
    print("-" * 40)
    
    today_stats = db.get_today_stats()
    print(f"📊 Dzisiejsze statystyki:")
    print(f"   💭 Myśli: {today_stats['thoughts_today']}")
    print(f"   💰 Koszt: ${today_stats['cost_today']:.4f}")
    print(f"   ⚡ Średnia energia: {today_stats['avg_energy']:.2f}")
    print(f"   ⭐ Znaczące myśli: {today_stats['significant_thoughts']}")
    if today_stats['last_thought']:
        last_thought_str = today_stats['last_thought'].strftime('%H:%M:%S')
        print(f"   🕐 Ostatnia myśl: {last_thought_str}")
    
    consciousness_status = db.get_consciousness_status()
    print(f"\n🧠 Status świadomości:")
    print(f"   🆔 Sesja: {consciousness_status['session_id'][:8]}...")
    print(f"   📊 Myśli w sesji: {consciousness_status['total_thoughts']}")
    print(f"   💰 Koszt sesji: ${consciousness_status['total_cost']:.4f}")
    print(f"   🎯 Status: {consciousness_status['status']}")
    
    # Test aktywności web
    print("\n📱 Test 7: Log aktywności web")
    print("-" * 40)
    
    activities = db.get_live_activity(limit=10)
    print(f"🌐 Pobrano {len(activities)} aktywności dla strony web:")
    for activity in activities:
        timestamp_str = activity.timestamp.strftime('%H:%M:%S')
        print(f"   • [{timestamp_str}] {activity.activity_type}: {activity.activity_title}")
        if activity.activity_description:
            print(f"     {activity.activity_description[:50]}...")
    
    # Aktualizacja sesji
    print("\n🔄 Test 8: Aktualizacja sesji")
    print("-" * 40)
    
    db.update_consciousness_session(
        session_id=session_id,
        total_thoughts=len(test_thoughts),
        total_cost=sum(t.cost_usd for t in test_thoughts)
    )
    print("✅ Sesja zaktualizowana")
    
    # Zakończenie sesji
    db.end_consciousness_session(
        session_id=session_id,
        final_mood="satisfied",
        final_energy=0.85
    )
    print("✅ Sesja zakończona")
    
    print(f"\n🎉 PODSUMOWANIE:")
    print(f"   ✅ Baza danych MySQL działa perfekcyjnie!")
    print(f"   ✅ Zapisano {len(test_thoughts)} myśli")
    print(f"   ✅ Utworzono {len([t for t in test_thoughts if t.is_significant])} znaczących myśli")
    print(f"   ✅ Zapisano 1 wspomnienie")
    print(f"   ✅ Zarejestrowano {len(activities)} aktywności web")
    print(f"   ✅ Sesja świadomości kompletna")
    print(f"\n🚀 Adam Clay gotowy na przejście z plików na bazę MySQL!")

if __name__ == "__main__":
    test_database_system() 