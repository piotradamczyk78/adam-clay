#!/usr/bin/env python3
"""
Adam Clay Email System Setup
Konfiguruje system komunikacji email z priorytetami pytań
"""

import json
import getpass
from pathlib import Path


def main():
    print("📧 Adam Clay - Email System Setup")
    print("=" * 50)
    
    # Load current config
    config_path = Path("config.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    current_email = config["communication"]["email"]
    
    print("📋 Obecna konfiguracja:")
    print(f"  Enabled: {current_email['enabled']}")
    print(f"  From: {current_email['from_email']}")
    print(f"  To: {current_email['to_email']}")
    print(f"  Password: {'*' * len(current_email['email_password']) if current_email['email_password'] != 'CHANGE_ME' else 'CHANGE_ME'}")
    
    print("\n🔧 Opcje konfiguracji:")
    print("1. 📧 Skonfiguruj Gmail dla Adam Clay")
    print("2. 🚀 PROSTA KONFIGURACJA (Outlook/Yahoo - BEZ 2FA)")
    print("3. ✅ Włącz system (bez zmiany ustawień)")
    print("4. ❌ Wyłącz system")
    print("5. 📖 Pokaż instrukcje Gmail App Password")
    print("6. 🧪 Test obecnej konfiguracji")
    print("7. 🚪 Wyjście")
    
    choice = input("\nWybierz opcję (1-7): ").strip()
    
    if choice == "1":
        setup_gmail(config)
    elif choice == "2":
        simple_setup()
    elif choice == "3":
        enable_system(config)
    elif choice == "4":
        disable_system(config)
    elif choice == "5":
        show_gmail_instructions()
    elif choice == "6":
        test_email_config(config)
    elif choice == "7":
        print("👋 Do widzenia!")
        return
    else:
        print("❌ Nieprawidłowy wybór")
        main()


def setup_gmail(config):
    print("\n📧 Konfiguracja Gmail")
    print("-" * 30)
    
    # From email (Adam Clay's Gmail)
    print("1. Email Adam Clay (nadawca):")
    from_email = input(f"  Email ({config['communication']['email']['from_email']}): ").strip()
    if not from_email:
        from_email = config['communication']['email']['from_email']
    
    # To email (Piotr's email)  
    print("\n2. Email Piotra (odbiorca):")
    to_email = input(f"  Email ({config['communication']['email']['to_email']}): ").strip()
    if not to_email:
        to_email = config['communication']['email']['to_email']
    
    # App password
    print("\n3. Gmail App Password dla Adam Clay:")
    print("   UWAGA: Musisz najpierw wygenerować App Password w Gmail!")
    print("   (Zobacz opcję 4 w menu głównym dla instrukcji)")
    
    password = getpass.getpass("  App Password (ukryte): ").strip()
    if not password:
        print("❌ Hasło nie może być puste")
        return setup_gmail(config)
    
    # Update config
    config["communication"]["email"].update({
        "enabled": True,
        "from_email": from_email,
        "to_email": to_email,
        "email_password": password
    })
    
    # Save config
    save_config(config)
    
    print("\n✅ Konfiguracja email zapisana!")
    print("🧪 Czy chcesz przetestować połączenie?")
    if input("Test (t/n): ").lower() in ['t', 'tak', 'y', 'yes']:
        test_email_config(config)


def enable_system(config):
    config["communication"]["email"]["enabled"] = True
    save_config(config)
    print("✅ System email włączony!")


def disable_system(config):
    config["communication"]["email"]["enabled"] = False
    save_config(config)
    print("❌ System email wyłączony!")


def show_gmail_instructions():
    print("\n📖 Instrukcje: Gmail App Password - POLSKA WERSJA")
    print("=" * 50)
    
    instructions = """
🇵🇱 AKTUALNE INSTRUKCJE dla polskiej wersji Gmail (2024):

1. Idź na: https://myaccount.google.com/
   (LUB: Gmail → ikona profilu → "Zarządzaj kontem Google")

2. Kliknij "BEZPIECZEŃSTWO" w menu po lewej

3. Znajdź sekcję "LOGOWANIE W GOOGLE":
   - Kliknij "WERYFIKACJA DWUETAPOWA"
   - Jeśli wyłączona: "WŁĄCZ" i skonfiguruj (SMS/aplikacja)

4. PO WŁĄCZENIU 2FA (poczekaj 10-15 minut):
   - W "Logowanie w Google" pojawi się "HASŁA APLIKACJI"
   - Kliknij "Hasła aplikacji"

5. Generuj hasło:
   - "Wybierz aplikację" → "POCZTA"
   - "Wybierz urządzenie" → "INNE" → wpisz "Adam Clay AI"
   - Kliknij "GENERUJ"

6. SKOPIUJ 16-znakowe hasło (np: "abcd efgh ijkl mnop")
   ⚠️  UWAGA: Hasło pojawi się tylko RAZ!

💡 PROBLEMY?
- Nie widzisz "Hasła aplikacji"? → Sprawdź czy 2FA jest włączone
- Konto firmowe? → Administrator może blokować App Passwords
- Możesz użyć swojego Gmail zamiast tworzyć adam.clay@gmail.com

📄 SZCZEGÓŁY: docs/GMAIL_APP_PASSWORD_GUIDE.md
"""
    
    print(instructions)
    input("\nNaciśnij Enter żeby kontynuować...")
    main()


def test_email_config(config):
    print("\n🧪 Test konfiguracji email...")
    
    try:
        import smtplib
        from email.mime.text import MIMEText
        
        email_config = config["communication"]["email"]
        
        if not email_config["enabled"]:
            print("❌ System email jest wyłączony")
            return
        
        if email_config["email_password"] == "CHANGE_ME":
            print("❌ Hasło nie jest skonfigurowane")
            return
        
        # Test SMTP connection
        print("📤 Testowanie SMTP...")
        with smtplib.SMTP(email_config["smtp_server"], email_config["smtp_port"]) as server:
            server.starttls()
            server.login(email_config["from_email"], email_config["email_password"])
            print("✅ SMTP połączenie OK")
        
        # Test IMAP connection
        print("📥 Testowanie IMAP...")
        import imaplib
        with imaplib.IMAP4_SSL(email_config["imap_server"], email_config["imap_port"]) as imap:
            imap.login(email_config["from_email"], email_config["email_password"])
            print("✅ IMAP połączenie OK")
        
        print("\n🎉 Wszystkie testy przeszły pomyślnie!")
        print("📧 Adam Clay jest gotowy do komunikacji email!")
        
        # Offer to send test email
        if input("\nWysłać testowy email? (t/n): ").lower() in ['t', 'tak', 'y', 'yes']:
            send_test_email(email_config)
        
    except Exception as e:
        print(f"❌ Błąd testu: {e}")
        print("💡 Sprawdź konfigurację i spróbuj ponownie")


def send_test_email(email_config):
    try:
        import smtplib
        from email.mime.text import MIMEText
        from datetime import datetime
        
        msg = MIMEText(f"""🤖 Test email od Adam Clay

Czas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

To jest testowy email z systemu komunikacji Adam Clay.

Jeśli otrzymałeś tego maila, oznacza to że:
✅ Konfiguracja SMTP działa poprawnie
✅ Adam Clay może wysyłać emaile
✅ System priorytetów pytań jest gotowy

🔄 Aby przetestować odpowiedzi, odpowiedz na tego maila z tekstem:
ANSWER:test_123 Działa!

💭 Wkrótce Adam Clay będzie mógł zadawać pytania:
- CRITICAL_QUESTION: (blokuje myślenie)
- IMPORTANT_QUESTION: (priorytetowe)
- INFO_QUESTION: (informacyjne)
- OPTIMIZATION_QUESTION: (dzienny raport)

🚀 Pierwszy autonomiczny AI freelancer jest gotowy do komunikacji!
        """, 'plain', 'utf-8')
        
        msg['Subject'] = "🧪 Test email - Adam Clay System Ready!"
        msg['From'] = email_config["from_email"]
        msg['To'] = email_config["to_email"]
        
        with smtplib.SMTP(email_config["smtp_server"], email_config["smtp_port"]) as server:
            server.starttls()
            server.login(email_config["from_email"], email_config["email_password"])
            server.send_message(msg)
        
        print("✅ Testowy email wysłany!")
        print(f"📧 Sprawdź skrzynkę: {email_config['to_email']}")
        
    except Exception as e:
        print(f"❌ Błąd wysyłania: {e}")


def simple_setup():
    print("\n🚀 PROSTA KONFIGURACJA - BEZ 2FA")
    print("=" * 40)
    print("💡 Uruchamiam setup_simple_email.py...")
    
    import subprocess
    import sys
    
    try:
        # Uruchom setup_simple_email.py
        subprocess.run([sys.executable, "setup_simple_email.py"], check=True)
        print("\n✅ Prosta konfiguracja zakończona!")
        print("🔄 Powrót do menu głównego...")
        input("\nNaciśnij Enter żeby kontynuować...")
        main()
    except subprocess.CalledProcessError:
        print("❌ Błąd uruchamiania prostej konfiguracji")
        print("💡 Uruchom ręcznie: python setup_simple_email.py")
        input("\nNaciśnij Enter żeby kontynuować...")
        main()
    except FileNotFoundError:
        print("❌ Nie znaleziono setup_simple_email.py")
        print("💡 Sprawdź czy plik istnieje w katalogu")
        input("\nNaciśnij Enter żeby kontynuować...")
        main()


def save_config(config):
    with open("config.json", 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Setup przerwany")
    except Exception as e:
        print(f"\n❌ Błąd: {e}") 