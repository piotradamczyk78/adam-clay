#!/usr/bin/env python3
"""
Szybkie wyłączenie systemu email Adam Clay
"""

import json
from pathlib import Path


def main():
    print("📧 Wyłączanie systemu email Adam Clay")
    print("=" * 40)
    
    config_path = Path("config.json")
    
    if not config_path.exists():
        print("❌ Nie znaleziono config.json")
        return
    
    # Wczytaj konfigurację
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Sprawdź obecny stan
    email_enabled = config.get("communication", {}).get("email", {}).get("enabled", False)
    
    if not email_enabled:
        print("✅ System email już jest wyłączony")
        return
    
    print("🔄 Wyłączam system email...")
    
    # Wyłącz email
    config["communication"]["email"]["enabled"] = False
    
    # Zapisz
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ System email wyłączony!")
    print("🚀 Teraz możesz uruchomić Adam Clay bez problemów")
    print("💡 Uruchom: python main.py")
    
    # Info o funkcjach email
    print("\n📋 Co straciłeś wyłączając email:")
    print("  - Adam Clay nie będzie mógł zadawać Ci pytań")
    print("  - Brak interaktywnej komunikacji")
    print("  - Brak systemu priorytetów (CRITICAL, IMPORTANT, etc.)")
    
    print("\n🔄 Możesz włączyć ponownie przez:")
    print("  python setup_email_system.py")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Błąd: {e}") 