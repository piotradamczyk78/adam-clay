#!/usr/bin/env python3
"""
Prosta konfiguracja email bez 2FA
Alternatywni dostawcy email dla Adam Clay
"""

import json
import getpass
import smtplib
import imaplib
from pathlib import Path
from email.mime.text import MIMEText


def main():
    print("📧 PROSTA KONFIGURACJA EMAIL - BEZ 2FA")
    print("=" * 50)
    
    print("🎯 Dostawcy email bez weryfikacji dwuetapowej:")
    print("1. 📨 Outlook.com / Hotmail (Microsoft)")
    print("2. 📬 Yahoo Mail") 
    print("3. 🛠️  Mailtrap (testowy)")
    print("4. 🏠 Własny serwer SMTP")
    print("5. 🚪 Powrót")
    
    choice = input("\nWybierz dostawcę (1-5): ").strip()
    
    if choice == "1":
        setup_outlook()
    elif choice == "2":
        setup_yahoo()
    elif choice == "3":
        setup_mailtrap()
    elif choice == "4":
        setup_custom_smtp()
    elif choice == "5":
        return
    else:
        print("❌ Nieprawidłowy wybór")
        main()


def setup_outlook():
    print("\n📨 OUTLOOK.COM / HOTMAIL")
    print("=" * 30)
    
    print("✅ ZALETY:")
    print("  - BEZ weryfikacji dwuetapowej!")
    print("  - Wystarczy zwykłe hasło")
    print("  - Darmowe konto")
    
    print("\n📋 INSTRUKCJE:")
    print("1. Utwórz konto: https://outlook.com")
    print("2. Email: adam.clay.ai@outlook.com (lub podobny)")
    print("3. Użyj zwykłego hasła konta")
    
    # Konfiguracja
    from_email = input("\n📧 Email Adam Clay (@outlook.com): ").strip()
    if not from_email:
        from_email = "adam.clay.ai@outlook.com"
    
    to_email = input("📧 Twój email: ").strip()
    if not to_email:
        print("❌ Email odbiorcy jest wymagany")
        return
    
    password = getpass.getpass("🔐 Hasło Outlook (ukryte): ").strip()
    if not password:
        print("❌ Hasło jest wymagane")
        return
    
    config = {
        "enabled": True,
        "from_email": from_email,
        "email_password": password,
        "to_email": to_email,
        "smtp_server": "smtp-mail.outlook.com",
        "smtp_port": 587,
        "imap_server": "outlook.office365.com",
        "imap_port": 993,
        "check_interval": 60
    }
    
    if test_email_connection(config):
        save_email_config(config)
        print("🎉 Outlook skonfigurowany pomyślnie!")


def setup_yahoo():
    print("\n📬 YAHOO MAIL")
    print("=" * 20)
    
    print("⚠️  UWAGA: Yahoo może wymagać App Password")
    print("✅ ALTERNATYWA: Włącz 'Less secure app access'")
    
    print("\n📋 INSTRUKCJE:")
    print("1. Utwórz konto: https://mail.yahoo.com")
    print("2. Account Security → Less secure app access → ON")
    print("   LUB wygeneruj App Password")
    
    from_email = input("\n📧 Email Adam Clay (@yahoo.com): ").strip()
    if not from_email:
        from_email = "adam.clay.ai@yahoo.com"
    
    to_email = input("📧 Twój email: ").strip()
    password = getpass.getpass("🔐 Hasło Yahoo (ukryte): ").strip()
    
    config = {
        "enabled": True,
        "from_email": from_email,
        "email_password": password,
        "to_email": to_email,
        "smtp_server": "smtp.mail.yahoo.com",
        "smtp_port": 587,
        "imap_server": "imap.mail.yahoo.com",
        "imap_port": 993,
        "check_interval": 60
    }
    
    if test_email_connection(config):
        save_email_config(config)
        print("🎉 Yahoo skonfigurowany pomyślnie!")


def setup_mailtrap():
    print("\n🛠️  MAILTRAP - TESTOWY SERWER EMAIL")
    print("=" * 40)
    
    print("✅ ZALETY:")
    print("  - Tylko do testów (nie wysyła prawdziwych emaili)")
    print("  - Bez 2FA")
    print("  - Darmowy plan")
    print("  - Webowy podgląd emaili")
    
    print("\n📋 INSTRUKCJE:")
    print("1. Zarejestruj się: https://mailtrap.io")
    print("2. Email Testing → My Inbox → Show Credentials")
    print("3. Skopiuj Username i Password")
    
    username = input("\n👤 Mailtrap Username: ").strip()
    password = getpass.getpass("🔐 Mailtrap Password: ").strip()
    
    config = {
        "enabled": True,
        "from_email": "adam.clay@test.com",  # Może być fake dla testów
        "email_password": password,
        "to_email": "piotr@test.com",       # Może być fake dla testów
        "smtp_server": "smtp.mailtrap.io",
        "smtp_port": 587,
        "smtp_username": username,          # Dodatkowe pole dla Mailtrap
        "imap_server": "smtp.mailtrap.io",  # Mailtrap nie ma IMAP, tylko SMTP
        "imap_port": 993,
        "check_interval": 60
    }
    
    print("🧪 Testowanie połączenia Mailtrap...")
    try:
        with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
            server.starttls()
            server.login(username, password)
        print("✅ Mailtrap połączenie OK!")
        save_email_config(config)
        print("🎉 Mailtrap skonfigurowany!")
        print("📧 Wszystkie emaile będą widoczne w panelu Mailtrap")
        
    except Exception as e:
        print(f"❌ Błąd połączenia: {e}")


def setup_custom_smtp():
    print("\n🏠 WŁASNY SERWER SMTP")
    print("=" * 25)
    
    print("💡 Dla zaawansowanych użytkowników")
    print("  - Własny serwer email")
    print("  - Hostingi z SMTP (np. nazwa.pl, home.pl)")
    print("  - Lokalne serwery testowe")
    
    from_email = input("\n📧 Email nadawcy: ").strip()
    to_email = input("📧 Email odbiorcy: ").strip()
    password = getpass.getpass("🔐 Hasło SMTP: ").strip()
    
    smtp_server = input("🌐 Serwer SMTP: ").strip()
    smtp_port = input("🔌 Port SMTP (587): ").strip() or "587"
    
    imap_server = input("📥 Serwer IMAP (opcjonalnie): ").strip() or smtp_server
    imap_port = input("🔌 Port IMAP (993): ").strip() or "993"
    
    config = {
        "enabled": True,
        "from_email": from_email,
        "email_password": password,
        "to_email": to_email,
        "smtp_server": smtp_server,
        "smtp_port": int(smtp_port),
        "imap_server": imap_server,
        "imap_port": int(imap_port),
        "check_interval": 60
    }
    
    if test_email_connection(config):
        save_email_config(config)
        print("🎉 Własny SMTP skonfigurowany!")


def test_email_connection(config):
    print("\n🧪 Testowanie połączenia...")
    
    try:
        # Test SMTP
        print("📤 Test SMTP...")
        with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
            server.starttls()
            
            # Mailtrap używa oddzielnego username
            if "smtp_username" in config:
                server.login(config["smtp_username"], config["email_password"])
            else:
                server.login(config["from_email"], config["email_password"])
        
        print("✅ SMTP połączenie OK!")
        
        # Test IMAP (opcjonalnie, bo nie wszędzie dostępne)
        try:
            print("📥 Test IMAP...")
            with imaplib.IMAP4_SSL(config["imap_server"], config["imap_port"]) as imap:
                if "smtp_username" in config:
                    imap.login(config["smtp_username"], config["email_password"])
                else:
                    imap.login(config["from_email"], config["email_password"])
            print("✅ IMAP połączenie OK!")
        except:
            print("⚠️  IMAP niedostępny (tylko SMTP)")
        
        # Wysłij testowy email
        if input("\nWysłać testowy email? (t/n): ").lower() in ['t', 'tak', 'y', 'yes']:
            send_test_email(config)
        
        return True
        
    except Exception as e:
        print(f"❌ Błąd połączenia: {e}")
        print("\n💡 Sprawdź:")
        print("  - Poprawność emaila i hasła")
        print("  - Ustawienia bezpieczeństwa konta")
        print("  - Czy dostawca blokuje aplikacje trzecie")
        return False


def send_test_email(config):
    try:
        msg = MIMEText(f"""🤖 Test email od Adam Clay - PROSTA KONFIGURACJA

To jest testowy email z prostego systemu konfiguracji (bez 2FA).

✅ Konfiguracja działa poprawnie!
📧 Dostawca: {config['smtp_server']}
🕐 Czas: {__import__('datetime').datetime.now()}

🚀 Adam Clay jest gotowy do komunikacji!
        """, 'plain', 'utf-8')
        
        msg['Subject'] = "🧪 Test Adam Clay - Prosta konfiguracja"
        msg['From'] = config["from_email"]
        msg['To'] = config["to_email"]
        
        with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
            server.starttls()
            
            if "smtp_username" in config:
                server.login(config["smtp_username"], config["email_password"])
            else:
                server.login(config["from_email"], config["email_password"])
            
            server.send_message(msg)
        
        print("✅ Testowy email wysłany!")
        print(f"📧 Sprawdź skrzynkę: {config['to_email']}")
        
    except Exception as e:
        print(f"❌ Błąd wysyłania: {e}")


def save_email_config(config):
    config_path = Path("config.json")
    
    # Wczytaj obecną konfigurację
    with open(config_path, 'r', encoding='utf-8') as f:
        full_config = json.load(f)
    
    # Zaktualizuj sekcję email
    full_config["communication"]["email"] = config
    
    # Zapisz
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(full_config, f, indent=2, ensure_ascii=False)
    
    print("✅ Konfiguracja email zapisana do config.json")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Konfiguracja przerwana")
    except Exception as e:
        print(f"\n❌ Błąd: {e}") 