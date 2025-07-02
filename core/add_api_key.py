#!/usr/bin/env python3
"""
Prosty skrypt do dodania klucza API do config.json
"""

import json
import getpass
from pathlib import Path


def main():
    print("🔑 Dodawanie klucza API do config.json")
    print("=" * 40)
    
    config_path = Path("config.json")
    
    if not config_path.exists():
        print("❌ Nie znaleziono config.json")
        return
    
    # Wczytaj obecną konfigurację
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Sprawdź obecny klucz
    current_key = config.get("api", {}).get("api_key", "WKLEJ_TUTAJ_SWOJ_KLUCZ_API")
    
    if current_key != "WKLEJ_TUTAJ_SWOJ_KLUCZ_API":
        print(f"✅ Klucz API już jest skonfigurowany: {current_key[:10]}...")
        choice = input("Czy chcesz go zmienić? (t/n): ").lower()
        if choice not in ['t', 'tak', 'y', 'yes']:
            print("👋 Klucz pozostaje bez zmian")
            return
    
    # Pobierz nowy klucz
    print("\n🔐 Wklej swój klucz API LLM provider:")
    print("   (Klucz zaczyna się od 'sk-ant-api03-')")
    
    api_key = getpass.getpass("Klucz API (ukryty): ").strip()
    
    if not api_key:
        print("❌ Klucz nie może być pusty")
        return
    
    if not api_key.startswith('sk-ant-api03-'):
        print("⚠️  Uwaga: Klucz nie wygląda jak typowy klucz LLM provider")
        choice = input("Czy mimo to chcesz kontynuować? (t/n): ").lower()
        if choice not in ['t', 'tak', 'y', 'yes']:
            return
    
    # Zaktualizuj konfigurację
    config["api"]["api_key"] = api_key
    
    # Zapisz
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ Klucz API zapisany do config.json!")
    print(f"🎯 Adam Clay używa klucza: {api_key[:10]}...")
    
    # Test
    print("\n🧪 Chcesz przetestować klucz?")
    if input("Test (t/n): ").lower() in ['t', 'tak', 'y', 'yes']:
        test_api_key()


def test_api_key():
    try:
        from src.utils.config_loader import ConfigLoader
        
        print("🔄 Testowanie klucza API...")
        config = ConfigLoader().load_config()
        api_key = ConfigLoader.get_api_key(config)
        
        print(f"✅ Klucz załadowany pomyślnie: {api_key[:10]}...")
        print("🚀 Adam Clay jest gotowy do uruchomienia!")
        
    except Exception as e:
        print(f"❌ Błąd testowania: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Anulowano")
    except Exception as e:
        print(f"\n❌ Błąd: {e}") 