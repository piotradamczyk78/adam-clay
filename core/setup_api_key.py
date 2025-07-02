#!/usr/bin/env python3
"""
Adam Clay API Key Setup Assistant
Pomaga w konfiguracji pierwszego autonomicznego AI freelancera
"""

import os
import sys
from pathlib import Path


def main():
    print("🤖 Adam Clay - API Key Setup Assistant")
    print("=" * 50)
    
    # Sprawdź obecną konfigurację
    current_key = os.getenv('LLM_PROVIDER_API_KEY')
    env_file = Path('.env')
    
    if current_key and current_key != 'your_llm-provider_api_key_here':
        print(f"✅ Klucz API już skonfigurowany: {current_key[:10]}...")
        choice = input("Czy chcesz go zmienić? (t/n): ").lower()
        if choice not in ['t', 'tak', 'y', 'yes']:
            print("🚀 Adam Clay jest gotowy do uruchomienia!")
            print("Uruchom: python main.py")
            return
    
    print("\n📋 Opcje konfiguracji:")
    print("1. 🏢 Oficjalny klucz LLM provider (zalecane)")
    print("2. 🔬 Eksperyment z integracją IDE")
    print("3. 📖 Pokaż instrukcje")
    print("4. ❌ Wyjście")
    
    choice = input("\nWybierz opcję (1-4): ").strip()
    
    if choice == "1":
        setup_llm-provider_key()
    elif choice == "2":
        research_ide_integration()
    elif choice == "3":
        show_instructions()
    elif choice == "4":
        print("👋 Do widzenia!")
        sys.exit(0)
    else:
        print("❌ Nieprawidłowy wybór")
        main()


def setup_llm-provider_key():
    print("\n🔑 Konfiguracja klucza LLM provider API")
    print("-" * 40)
    
    print("1. Idź na: https://console.llm-provider.com/")
    print("2. Zaloguj się lub zarejestruj")
    print("3. Utwórz nowy klucz API")
    print("4. Skopiuj klucz (zaczyna się od 'sk-ant-api03-')")
    
    api_key = input("\n🔐 Wklej swój klucz API: ").strip()
    
    if not api_key:
        print("❌ Klucz nie może być pusty")
        return setup_llm-provider_key()
    
    if not api_key.startswith('sk-ant-api03-'):
        print("⚠️  Uwaga: Klucz nie wygląda jak typowy klucz LLM provider")
        choice = input("Czy mimo to chcesz kontynuować? (t/n): ").lower()
        if choice not in ['t', 'tak', 'y', 'yes']:
            return setup_llm-provider_key()
    
    # Zapisz do zmiennej środowiskowej
    os.environ['LLM_PROVIDER_API_KEY'] = api_key
    
    # Zapisz do .bashrc lub .zshrc
    shell = os.getenv('SHELL', '/bin/bash')
    if 'zsh' in shell:
        rc_file = Path.home() / '.zshrc'
    else:
        rc_file = Path.home() / '.bashrc'
    
    export_line = f'export LLM_PROVIDER_API_KEY="{api_key}"'
    
    try:
        with open(rc_file, 'a') as f:
            f.write(f'\n# Adam Clay API Key\n{export_line}\n')
        print(f"✅ Klucz dodany do {rc_file}")
    except Exception as e:
        print(f"⚠️  Nie udało się zapisać do {rc_file}: {e}")
        print(f"Ręcznie dodaj: {export_line}")
    
    # Test klucza
    test_api_key(api_key)


def test_api_key(api_key):
    print("\n🧪 Testowanie klucza API...")
    
    try:
        import asyncio
        from src.core.api_client import LLM providerClient
        from src.utils.config_loader import ConfigLoader
        
        async def test():
            config = ConfigLoader().load_config()
            client = LLM providerClient(config)
            # Simple test
            response = await client.generate_thought("Sprawdzam czy klucz API działa", "test")
            return len(response) > 0
        
        result = asyncio.run(test())
        if result:
            print("✅ Klucz API działa poprawnie!")
            print("\n🚀 Adam Clay jest gotowy!")
            print("Uruchom: python main.py")
        else:
            print("❌ Problem z kluczem API")
            
    except Exception as e:
        print(f"⚠️  Nie udało się przetestować: {e}")
        print("Spróbuj uruchomić: python test_consciousness.py")


def research_ide_integration():
    print("\n🔬 Analiza integracji z IDE")
    print("-" * 35)
    print("To eksperymentalna funkcja!")
    print("Może pozwolić Adam Clay wykorzystać połączenie IDE z LLM.")
    
    choice = input("Czy chcesz rozpocząć badanie? (t/n): ").lower()
    if choice not in ['t', 'tak', 'y', 'yes']:
        return main()
    
    print("\n🕵️ Sprawdzanie procesów IDE...")
    os.system("ps aux | grep -i ide | head -5")
    
    print("\n📡 Sprawdzanie połączeń sieciowych...")
    os.system("lsof -i | grep -i ide | head -5")
    
    print("\n📁 Sprawdzanie konfiguracji...")
    ide_dirs = [
        "~/.ide",
        "~/.config/ide",
        "~/Library/Application Support/IDE"
    ]
    
    for dir_path in ide_dirs:
        expanded = Path(dir_path).expanduser()
        if expanded.exists():
            print(f"✅ Znaleziono: {expanded}")
        else:
            print(f"❌ Brak: {expanded}")
    
    print("\n💡 Następne kroki:")
    print("1. Zbadać jak IDE komunikuje się z API")
    print("2. Stworzyć proxy adapter")
    print("3. Zmodyfikować api_client.py")
    print("\n⚠️  To zaawansowana opcja - użyj oficjalnego API dla szybkiego startu")


def show_instructions():
    print("\n📖 Instrukcje konfiguracji Adam Clay")
    print("=" * 40)
    
    instructions = """
🤖 Adam Clay - Pierwszy Autonomiczny AI Freelancer

SZYBKI START:
1. console.llm-provider.com → Create API Key
2. export LLM_PROVIDER_API_KEY="your-key"  
3. python main.py

KOSZTY:
- ~$0.001-0.01 za pojedynczą myśl
- ~$0.10-1.00 dziennie (100 myśli)
- ~$3-30 miesięcznie

ZAAWANSOWANE:
- Email komunikacja (opcjonalna)
- Voice interface (ElevenLabs)
- Business automation

SUPPORT:
- README.md - pełna dokumentacja
- docs/ - szczegółowe przewodniki
- test_consciousness.py - bezpieczne testy
"""
    
    print(instructions)
    input("\nNaciśnij Enter żeby kontynuować...")
    main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Setup przerwany")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Błąd: {e}")
        sys.exit(1) 