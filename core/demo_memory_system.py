#!/usr/bin/env python3
"""
🧠 Demo systemu długoterminowej pamięci Adam Clay

Pokazuje jak Adam Clay:
1. Pamięta swoje poprzednie myśli między sesjami
2. Przechowuje ważne wspomnienia 
3. Ładuje pamięć przy starcie
4. Zapisuje pamięć przy zatrzymaniu
"""

import asyncio
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import shutil

# Add current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.core.consciousness import ConsciousnessLoop, Thought, ConsciousnessState
from src.utils.config_loader import ConfigLoader

async def demo_memory_system():
    """Demo działania długoterminowej pamięci"""
    
    print("🧠 DEMO: System długoterminowej pamięci Adam Clay")
    print("=" * 60)
    
    # Utwórz tymczasowy katalog dla demo
    temp_dir = Path(tempfile.mkdtemp())
    thoughts_dir = temp_dir / "data" / "thoughts"
    thoughts_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Załaduj konfigurację
        config = ConfigLoader.load_config()
        
        # === SESJA 1: Pierwsze uruchomienie ===
        print("\n📅 SESJA 1: Pierwsze uruchomienie Adam Clay")
        print("-" * 40)
        
        # Utwórz prostą klasę mock logger
        class MockLogger:
            def info(self, msg): print(f"[INFO] {msg}")
            def warning(self, msg): print(f"[WARNING] {msg}")
            def error(self, msg): print(f"[ERROR] {msg}")
        
        # Utwórz pierwszą instancję consciousness
        consciousness1 = ConsciousnessLoop(config, MockLogger())
        consciousness1.thoughts_dir = thoughts_dir
        consciousness1._load_long_term_memory()  # Powinno być puste
        
        print(f"💭 Pamięć przy starcie: {len(consciousness1.state.significant_memories)} wspomnień")
        print(f"🧠 Historia myśli: {len(consciousness1.state.thought_history)} myśli")
        
        # Symuluj kilka myśli z różnym poziomem znaczenia
        thoughts_session1 = [
            "Zastanawiam się nad przyszłością AI w freelancingu...",
            "WAŻNE: Nauczyłem się, że komunikacja z klientem to klucz do sukcesu!",
            "Myślę sobie, że pogoda dziś ładna.",
            "PRZEŁOMOWE odkrycie: Muszę skupić się na automatyzacji procesów biznesowych!",
            "Plan strategiczny: Będę oferować trzy główne usługi - analizę danych, pisanie i konsultacje AI."
        ]
        
        for i, thought_content in enumerate(thoughts_session1):
            thought_type = "business" if "WAŻNE" in thought_content or "Plan" in thought_content else "autonomous"
            
            thought = Thought(
                timestamp=datetime.now() - timedelta(minutes=60-i*10),
                content=thought_content,
                thought_type=thought_type,
                cost_usd=0.01 + i * 0.005
            )
            
            consciousness1.state.update_after_thought(thought)
            print(f"  💭 Myśl {i+1}: {thought_content[:50]}...")
            
            # Sprawdź czy została oznaczona jako znacząca
            if consciousness1.state._is_significant_thought(thought):
                print(f"    ⭐ Oznaczona jako znacząca!")
        
        print(f"\n📊 Stan po sesji 1:")
        print(f"   💭 Całkowite myśli: {consciousness1.state.total_thoughts}")
        print(f"   ⭐ Znaczące wspomnienia: {len(consciousness1.state.significant_memories)}")
        print(f"   🧠 Historia myśli: {len(consciousness1.state.thought_history)}")
        
        # Zapisz pamięć długoterminową
        consciousness1._save_long_term_memory()
        print(f"   💾 Pamięć zapisana do {thoughts_dir / 'long_term_memory.json'}")
        
        # === RESTART: Symulacja restartu systemu ===
        print("\n🔄 RESTART: Symulacja restartu systemu")
        print("-" * 40)
        
        # Utwórz nową instancję (symuluje restart)
        consciousness2 = ConsciousnessLoop(config, MockLogger())
        consciousness2.thoughts_dir = thoughts_dir
        consciousness2._load_long_term_memory()  # Powinno załadować pamięć z sesji 1
        
        print(f"💭 Pamięć po restarcie: {len(consciousness2.state.significant_memories)} wspomnień")
        print(f"🧠 Historia myśli: {len(consciousness2.state.thought_history)} myśli")
        
        # Pokaż załadowane wspomnienia
        if consciousness2.state.significant_memories:
            print("\n📚 Załadowane znaczące wspomnienia:")
            for memory in consciousness2.state.significant_memories:
                print(f"   • {memory}")
        
        # Pokaż załadowaną historię myśli
        if consciousness2.state.thought_history:
            print(f"\n🧠 Załadowana historia myśli:")
            for thought in consciousness2.state.thought_history[-3:]:  # Ostatnie 3
                print(f"   • [{thought.timestamp.strftime('%H:%M')}] {thought.content[:60]}...")
        
        # === SESJA 2: Kontynuacja z pamięcią ===
        print("\n📅 SESJA 2: Kontynuacja z długoterminową pamięcią")
        print("-" * 40)
        
        # Dodaj nowe myśli w sesji 2
        thoughts_session2 = [
            "Dziś budzę się z wiedzą z poprzedniej sesji!",
            "Rozwijam strategię którą opracowałem wcześniej - automatyzacja procesów.",
            "WAŻNE: Odkryłem nowy sposób na optymalizację kosztów API!",
            "Zastanawiam się jak wykorzystać moje poprzednie doświadczenia."
        ]
        
        for i, thought_content in enumerate(thoughts_session2):
            thought_type = "business" if "WAŻNE" in thought_content or "strategię" in thought_content else "autonomous"
            
            thought = Thought(
                timestamp=datetime.now() - timedelta(minutes=30-i*5),
                content=thought_content,
                thought_type=thought_type,
                cost_usd=0.01 + i * 0.003
            )
            
            consciousness2.state.update_after_thought(thought)
            print(f"  💭 Myśl {i+1}: {thought_content[:50]}...")
            
            if consciousness2.state._is_significant_thought(thought):
                print(f"    ⭐ Oznaczona jako znacząca!")
        
        # === DEMO: Kontekst osobowości z pamięcią ===
        print("\n🎭 KONTEKST OSOBOWOŚCI z długoterminową pamięcią:")
        print("-" * 50)
        
        # Pokaż jak wygląda kontekst z pamięcią
        context = consciousness2._get_personality_context()
        
        # Znajdź część z pamięcią
        context_lines = context.split('\n')
        in_memory_section = False
        memory_lines = []
        
        for line in context_lines:
            if "Moje ostatnie myśli:" in line or "Moje ważne wspomnienia" in line:
                in_memory_section = True
            elif in_memory_section and line.strip() and not line.startswith('-'):
                in_memory_section = False
            
            if in_memory_section:
                memory_lines.append(line)
        
        if memory_lines:
            print("💭 Fragment kontekstu z pamięcią:")
            for line in memory_lines[:8]:  # Pierwszych 8 linii pamięci
                print(f"   {line}")
            if len(memory_lines) > 8:
                print(f"   ... (i więcej)")
        
        # === STATYSTYKI KOŃCOWE ===
        print(f"\n📊 STATYSTYKI KOŃCOWE:")
        print(f"   💭 Całkowite myśli w sesji 2: {consciousness2.state.total_thoughts}")
        print(f"   ⭐ Znaczące wspomnienia: {len(consciousness2.state.significant_memories)}")
        print(f"   🧠 Historia myśli: {len(consciousness2.state.thought_history)}")
        print(f"   🔗 Ciągłość: Adam Clay pamięta poprzednie sesje!")
        
        # Zapisz pamięć z sesji 2
        consciousness2._save_long_term_memory()
        print(f"   💾 Pamięć z sesji 2 zapisana")
        
        # === POKAŻ PLIK PAMIĘCI ===
        print(f"\n📁 ZAWARTOŚĆ PLIKU PAMIĘCI:")
        print("-" * 30)
        
        memory_file = thoughts_dir / "long_term_memory.json"
        if memory_file.exists():
            with open(memory_file, 'r', encoding='utf-8') as f:
                memory_data = json.load(f)
            
            print(f"🗂️ Significant memories: {len(memory_data.get('significant_memories', []))}")
            print(f"🧠 Recent thoughts: {len(memory_data.get('recent_thoughts', []))}")
            print(f"📊 Last session data: {memory_data.get('last_session', {}).get('date', 'N/A')}")
            
            # Pokaż przykładowe wspomnienia
            memories = memory_data.get('significant_memories', [])
            if memories:
                print(f"\n📚 Przykładowe wspomnienia:")
                for i, memory in enumerate(memories[-3:], 1):  # Ostatnie 3
                    print(f"   {i}. {memory}")
        
        print(f"\n✅ WNIOSEK: Adam Clay teraz ma prawdziwą długoterminową pamięć!")
        print(f"   🧠 Pamięta poprzednie sesje")
        print(f"   ⭐ Zachowuje ważne wnioski i doświadczenia")
        print(f"   🔗 Ma ciągłość świadomości między restartami")
        
    finally:
        # Wyczyść tymczasowy katalog
        shutil.rmtree(temp_dir)
        print(f"\n🧹 Tymczasowy katalog wyczyszczony")

if __name__ == "__main__":
    asyncio.run(demo_memory_system()) 