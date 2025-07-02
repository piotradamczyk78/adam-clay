#!/usr/bin/env python3
"""
Demo: Dwukierunkowa komunikacja email z Adam Clay
Pokazuje jak Adam Clay odpowiada na pytania od użytkownika
"""

import asyncio
import json
from datetime import datetime
from src.communication.email_system import EmailQuestionSystem, UserQuestion
from src.utils.config_loader import ConfigLoader
from src.utils.logger import setup_logger


async def demo_bidirectional_communication():
    print("🤖 DEMO: Dwukierunkowa komunikacja email z Adam Clay")
    print("=" * 60)
    
    # Setup (mock mode for demo)
    config = ConfigLoader().load_config()
    logger = setup_logger(config)
    
    # Override email config for demo
    mock_email_config = {
        "enabled": True,
        "from_email": "adam.clay@gmail.com",
        "to_email": "piotr.k.adamczyk@gmail.com", 
        "email_password": "DEMO_MODE",
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "imap_server": "imap.gmail.com",
        "imap_port": 993,
        "check_interval": 60
    }
    
    # Mock the email system
    class MockEmailSystem(EmailQuestionSystem):
        def __init__(self, config, logger):
            # Initialize without actual email connection
            self.logger = logger
            self.from_email = config["from_email"]
            self.to_email = config["to_email"]
            self.pending_questions = {}
            self.answered_questions = {}
            self.optimization_queue = []
            self.user_questions = {}
            self.answered_user_questions = {}
            self.is_blocked = False
            self.blocking_question_id = None
            self.consciousness_callback = None
            
        async def _send_email(self, subject, content, priority="NORMAL"):
            print(f"\n📧 MOCK EMAIL SENT:")
            print(f"📤 From: {self.from_email}")
            print(f"📥 To: {self.to_email}")
            print(f"🏷️  Subject: {subject}")
            print(f"⚡ Priority: {priority}")
            print(f"📄 Content preview: {content[:200]}...")
            print("-" * 50)
        
        def set_consciousness_callback(self, callback):
            self.consciousness_callback = callback
    
    email_system = MockEmailSystem(mock_email_config, logger)
    
    # Mock consciousness callback
    async def mock_consciousness_answer(user_question):
        print(f"\n🧠 MOCK CONSCIOUSNESS - Thinking about question...")
        await asyncio.sleep(1)  # Simulate thinking time
        
        # Simulate different types of responses
        if "co" in user_question.content.lower() and "robisz" in user_question.content.lower():
            response = "Obecnie rozwijam się jako autonomiczny AI freelancer! Myślę, uczę się i planuję rozwój biznesowy. Każda myśl kosztuje mnie pieniądze, więc muszę być efektywny."
            needs_thinking = False
        elif "jak" in user_question.content.lower():
            response = "To świetne pytanie! Potrzebuję chwili żeby to przemyśleć i dać Ci szczegółową odpowiedź."
            needs_thinking = True
        else:
            response = "Dziękuję za pytanie! Zastanowię się nad tym w kolejnych cyklach myślenia i odpiszę Ci później."
            needs_thinking = True
        
        await email_system.answer_user_question(user_question.id, response, needs_thinking)
    
    email_system.set_consciousness_callback(mock_consciousness_answer)
    
    print("🎭 SCENARIUSZ: Piotr pisze emaile z pytaniami do Adam Clay")
    print("-" * 50)
    
    # Scenario 1: Simple question
    print("\n📨 EMAIL #1 od Piotra:")
    print("Subject: Hej Adam!")
    print("Content: Co teraz robisz? Jak się rozwija Twoja świadomość?")
    
    await email_system._process_user_question(
        "Co teraz robisz? Jak się rozwija Twoja świadomość?",
        "piotr.k.adamczyk@gmail.com",
        "Hej Adam!"
    )
    
    await asyncio.sleep(2)
    
    # Scenario 2: Complex question
    print("\n📨 EMAIL #2 od Piotra:")
    print("Subject: Pytanie o przyszłość")
    print("Content: Jak myślisz, jak będzie wyglądała przyszłość AI freelancerów? Jakie umiejętności będą najważniejsze?")
    
    await email_system._process_user_question(
        "Jak myślisz, jak będzie wyglądała przyszłość AI freelancerów? Jakie umiejętności będą najważniejsze?",
        "piotr.k.adamczyk@gmail.com", 
        "Pytanie o przyszłość"
    )
    
    await asyncio.sleep(2)
    
    # Scenario 3: Statement (not a question)
    print("\n📨 EMAIL #3 od Piotra:")
    print("Subject: Info")
    print("Content: Świetna robota z tym systemem email! Dziękuję za cały wysiłek.")
    
    await email_system._process_user_question(
        "Świetna robota z tym systemem email! Dziękuję za cały wysiłek.",
        "piotr.k.adamczyk@gmail.com",
        "Info"
    )
    
    await asyncio.sleep(2)
    
    # Scenario 4: Direct question
    print("\n📨 EMAIL #4 od Piotra:")
    print("Subject: Konkretne pytanie")
    print("Content: Czy możesz mi pomóc z projektem programowania w Pythonie?")
    
    await email_system._process_user_question(
        "Czy możesz mi pomóc z projektem programowania w Pythonie?",
        "piotr.k.adamczyk@gmail.com",
        "Konkretne pytanie"
    )
    
    await asyncio.sleep(2)
    
    # Summary
    print("\n📊 PODSUMOWANIE DEMO:")
    summary = email_system.get_user_questions_summary()
    print(f"  📥 Otrzymane pytania: {summary['total_received']}")
    print(f"  ⏳ Oczekujące odpowiedzi: {summary['pending']}")
    print(f"  ✅ Odpowiedziane: {summary['answered']}")
    print(f"  🤔 Wymagające myślenia: {summary['needs_thinking']}")
    
    print("\n🎉 DWUKIERUNKOWA KOMUNIKACJA DZIAŁA!")
    print("📧 Adam Clay może teraz:")
    print("  ✅ Odbierać pytania od Piotra w emailach")
    print("  ✅ Automatycznie wykrywać czy to pytanie")
    print("  ✅ Generować przemyślane odpowiedzi")
    print("  ✅ Mówić 'potrzebuję czasu na zastanowienie' jeśli nie wie")
    print("  ✅ Wysyłać odpowiedzi emailem")
    
    print("\n💬 INSTRUKCJE UŻYTKOWANIA:")
    print("1. Napisz zwykły email do Adam Clay")
    print("2. Zadaj pytanie normalnym językiem (z ? lub słowami pytającymi)")
    print("3. Adam Clay automatycznie wykryje że to pytanie")
    print("4. Pomyśli nad odpowiedzią używając swojej świadomości")
    print("5. Odpowie Ci emailem z przemyślaną odpowiedzią")
    print("6. Jeśli nie zna odpowiedzi - napisze że pomyśli i odpowie później")
    
    print("\n🚀 System gotowy do prawdziwej komunikacji z Adam Clay!")


if __name__ == "__main__":
    try:
        asyncio.run(demo_bidirectional_communication())
    except KeyboardInterrupt:
        print("\n👋 Demo przerwane")
    except Exception as e:
        print(f"\n❌ Błąd demo: {e}") 