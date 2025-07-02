#!/usr/bin/env python3
"""
Demo: Adam Clay Email Questions System
Pokazuje jak Adam Clay zadaje pytania z różnymi priorytetami
"""

import asyncio
import json
from datetime import datetime
from src.communication.email_system import EmailQuestionSystem, QuestionPriority
from src.utils.config_loader import ConfigLoader
from src.utils.logger import setup_logger


async def demo_email_questions():
    print("🤖 DEMO: Adam Clay Email Questions System")
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
    
    # Mock the email system (no real emails sent)
    class MockEmailSystem(EmailQuestionSystem):
        def __init__(self, config, logger):
            # Initialize without actual email connection
            self.logger = logger
            self.from_email = config["from_email"]
            self.to_email = config["to_email"]
            self.pending_questions = {}
            self.answered_questions = {}
            self.optimization_queue = []
            self.is_blocked = False
            self.blocking_question_id = None
            
        async def _send_email(self, subject, content, priority="NORMAL"):
            print(f"\n📧 MOCK EMAIL SENT:")
            print(f"📤 From: {self.from_email}")
            print(f"📥 To: {self.to_email}")
            print(f"🏷️  Subject: {subject}")
            print(f"⚡ Priority: {priority}")
            print(f"📄 Content preview: {content[:200]}...")
            print("-" * 50)
    
    email_system = MockEmailSystem(mock_email_config, logger)
    
    print("🧠 Adam Clay myśli i zadaje pytania różnych priorytetów...\n")
    
    # Demo 1: CRITICAL question (blocks execution)
    print("💭 Adam Clay thought: 'Zastanawiam się nad kluczową decyzją biznesową...'")
    await asyncio.sleep(1)
    
    print("\n🚨 CRITICAL QUESTION - BLOKUJE PROCES!")
    question_id = await email_system.ask_question(
        content="Czy powinienem skupić się na klientach enterprise czy małych firmach? To wpłynie na całą moją strategię rozwoju!",
        priority=QuestionPriority.CRITICAL,
        context={
            "mood": "business",
            "thought_type": "strategic_planning",
            "session_cost": 0.05
        }
    )
    
    print(f"⏸️  PROCES MYŚLENIA ZATRZYMANY! Czekam na odpowiedź ID: {question_id}")
    print("⏰ Adam Clay nie będzie myślał dalej dopóki nie otrzyma odpowiedzi...\n")
    
    await asyncio.sleep(2)
    
    # Demo 2: IMPORTANT question (non-blocking)
    print("💭 Adam Clay thought: 'Chciałbym również zapytać o coś ważnego...'")
    await asyncio.sleep(1)
    
    print("\n🔥 IMPORTANT QUESTION - PRIORYTETOWE")
    await email_system.ask_question(
        content="Jakie narzędzia AI powinienem dodać do mojej oferty? LLM jest świetny, ale może są jeszcze inne?",
        priority=QuestionPriority.IMPORTANT,
        context={
            "mood": "curious",
            "thought_type": "autonomous",
            "tools_currently_known": ["LLM", "GPT", "IDE"]
        }
    )
    
    print("▶️  Proces myślenia KONTYNUUJE (nie blokuje)\n")
    
    await asyncio.sleep(1)
    
    # Demo 3: INFORMATIVE question (background)
    print("💭 Adam Clay thought: 'Mam również pytanie informacyjne...'")
    await asyncio.sleep(1)
    
    print("\n📋 INFORMATIVE QUESTION - W TLE")
    await email_system.ask_question(
        content="Jak oceniasz moją osobowość i styl komunikacji? Czy jest coś co mogę poprawić?",
        priority=QuestionPriority.INFORMATIVE,
        context={
            "mood": "philosophical",
            "thought_type": "self_reflection",
            "current_personality_traits": ["curious", "business_focused", "philosophical"]
        }
    )
    
    print("💌 Wysłane w tle, odpowiedź zostanie zintegrowana później\n")
    
    await asyncio.sleep(1)
    
    # Demo 4: OPTIMIZATION question (daily batch)
    print("💭 Adam Clay thought: 'I na koniec pytanie optymalizacyjne...'")
    await asyncio.sleep(1)
    
    print("\n⚙️  OPTIMIZATION QUESTION - DZIENNY RAPORT")
    await email_system.ask_question(
        content="Czy interval 1 minuta myślenia to dobra częstotliwość dla rozwoju, czy powinienem myśleć rzadziej/częściej?",
        priority=QuestionPriority.OPTIMIZATION,
        context={
            "mood": "focused",
            "thought_type": "meta_optimization",
            "current_interval": "1 minute",
            "daily_thoughts": 50,
            "daily_cost": 0.75
        }
    )
    
    print("📊 Dodane do dziennego raportu optymalizacji\n")
    
    await asyncio.sleep(2)
    
    # Demo response processing
    print("🔄 DEMO: Otrzymywanie odpowiedzi")
    print("-" * 40)
    
    print("📨 Symulacja odpowiedzi od Piotra:")
    print("Email content: 'ANSWER:q_12345_critical Enterprise! Większe budżety i stabilniejsze projekty.'")
    
    # Mock response processing
    await email_system._process_answer("ANSWER:q_12345_critical Enterprise! Większe budżety i stabilniejsze projekty.")
    
    print("🎉 ODPOWIEDŹ OTRZYMANA!")
    print("▶️  PROCES MYŚLENIA WZNOWIONY!")
    print("💭 Adam Clay może kontynuować myślenie z nową wiedzą\n")
    
    # Final status
    print("📊 PODSUMOWANIE DEMO:")
    print(f"  Pytania CRITICAL: 1 (blokujące)")
    print(f"  Pytania IMPORTANT: 1 (priorytetowe)")
    print(f"  Pytania INFORMATIVE: 1 (w tle)")
    print(f"  Pytania OPTIMIZATION: 1 (dzienny raport)")
    print(f"  Oczekujące odpowiedzi: {len(email_system.pending_questions)}")
    print(f"  Otrzymane odpowiedzi: {len(email_system.answered_questions)}")
    
    print("\n🚀 System email komunikacji Adam Clay jest w pełni gotowy!")
    print("📧 Uruchom: python setup_email_system.py żeby skonfigurować prawdziwe emaile")


if __name__ == "__main__":
    asyncio.run(demo_email_questions()) 