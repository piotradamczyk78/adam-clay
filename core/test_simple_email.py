#!/usr/bin/env python3
"""
Test prostego systemu email bez 2FA
"""

import json
import asyncio
from pathlib import Path
from src.communication.email_system import EmailQuestionSystem, QuestionPriority
from src.utils.logger import setup_logger


async def test_email_system():
    print("🧪 TEST PROSTEGO SYSTEMU EMAIL")
    print("=" * 40)
    
    # Wczytaj konfigurację
    config_path = Path("config.json")
    if not config_path.exists():
        print("❌ Brak config.json")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    email_config = config.get("communication", {}).get("email", {})
    
    if not email_config.get("enabled"):
        print("❌ System email wyłączony")
        print("💡 Uruchom: python setup_simple_email.py")
        return
    
    print("📧 Konfiguracja:")
    print(f"  From: {email_config['from_email']}")
    print(f"  To: {email_config['to_email']}")
    print(f"  Server: {email_config['smtp_server']}")
    print(f"  Username: {email_config.get('smtp_username', email_config['from_email'])}")
    
    # Setup logger
    class SimpleLogger:
        def info(self, msg): print(f"ℹ️ {msg}")
        def error(self, msg): print(f"❌ {msg}")
    
    logger = SimpleLogger()
    
    # Test email system
    try:
        email_system = EmailQuestionSystem(email_config, logger)
        
        print("\n🧪 Testowanie połączenia...")
        
        # Test sending email
        await email_system._send_email(
            subject="🧪 Test Adam Clay - Prosta konfiguracja",
            content=f"""🤖 Test komunikacji Adam Clay

To jest testowy email z prostego systemu (bez 2FA).

✅ Konfiguracja działa!
🕐 Czas: {__import__('datetime').datetime.now()}
📧 Serwer: {email_config['smtp_server']}

🚀 System pytań gotowy:
- CRITICAL_QUESTION (blokuje myślenie)
- IMPORTANT_QUESTION (priorytetowe)
- INFO_QUESTION (informacyjne)  
- OPTIMIZATION_QUESTION (raport dzienny)

💬 Aby odpowiedzieć na pytanie, użyj formatu:
ANSWER:ID_PYTANIA treść odpowiedzi
            """,
            priority="NORMAL"
        )
        
        print("✅ Email wysłany pomyślnie!")
        print(f"📧 Sprawdź skrzynkę: {email_config['to_email']}")
        
        # Test pytania informacyjnego
        print("\n🔄 Test pytania informacyjnego...")
        await email_system.ask_question(
            "Czy system komunikacji email działa poprawnie?",
            QuestionPriority.INFORMATIVE,
            {"test": True, "setup": "simple_email"}
        )
        
        print("✅ Pytanie informacyjne wysłane!")
        
        # Info o odpowiadaniu
        print("\n📋 Jak odpowiadać na pytania:")
        print("1. Odpowiedz na email od Adam Clay")
        print("2. Użyj formatu: ANSWER:ID_PYTANIA treść")
        print("3. Przykład: ANSWER:q_123456789_informative Tak, działa!")
        
        print("\n🎉 Test zakończony pomyślnie!")
        print("🚀 Adam Clay jest gotowy do komunikacji!")
        
    except Exception as e:
        print(f"❌ Błąd: {e}")
        print("\n💡 Możliwe przyczyny:")
        print("  - Nieprawidłowe dane logowania")
        print("  - Blokada dostawcy email")
        print("  - Problemy z połączeniem internetowym")
        print("  - Nieaktywne konto email")


if __name__ == "__main__":
    try:
        asyncio.run(test_email_system())
    except KeyboardInterrupt:
        print("\n👋 Test przerwany")
    except Exception as e:
        print(f"\n❌ Błąd testu: {e}") 