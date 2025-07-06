#!/usr/bin/env python3
"""
Adam Clay Eden - Configuration Test Script
Skrypt testowy do weryfikacji konfiguracji
"""

import os
import sys
import json
from pathlib import Path

# Dodaj autogen do ścieżki
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'autogen'))

def test_environment_variables():
    """Test zmiennych środowiskowych"""
    print("🔧 Testowanie zmiennych środowiskowych...")
    
    required_vars = [
        'ANTHROPIC_API_KEY',
        'SLACK_BOT_TOKEN', 
        'SLACK_APP_TOKEN',
        'SLACK_CHANNEL_ID',
        'SLACK_USER_ID'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('your_') or value == 'C1234567890':
            missing_vars.append(var)
        else:
            print(f"  ✅ {var}: {'*' * 10}...{value[-4:]}")
    
    if missing_vars:
        print(f"  ❌ Brakujące zmienne: {', '.join(missing_vars)}")
        return False
    
    print("  ✅ Wszystkie zmienne środowiskowe są ustawione!")
    return True

def test_anthropic_api():
    """Test Anthropic API"""
    print("\n🧠 Testowanie Anthropic API...")
    
    try:
        import anthropic
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("  ❌ Brak ANTHROPIC_API_KEY")
            return False
        
        client = anthropic.Anthropic(api_key=api_key)
        
        # Test prostego requesta
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=50,
            messages=[{"role": "user", "content": "Powiedz 'test' po polsku"}]
        )
        
        if response.content[0].text:
            print(f"  ✅ Anthropic API działa! Odpowiedź: {response.content[0].text[:30]}...")
            return True
        else:
            print("  ❌ Brak odpowiedzi z Anthropic API")
            return False
            
    except ImportError:
        print("  ❌ Brak biblioteki anthropic (pip install anthropic)")
        return False
    except Exception as e:
        print(f"  ❌ Błąd Anthropic API: {e}")
        return False

def test_slack_api():
    """Test Slack API"""
    print("\n🔔 Testowanie Slack API...")
    
    try:
        from slack_sdk import WebClient
        
        bot_token = os.getenv('SLACK_BOT_TOKEN')
        if not bot_token:
            print("  ❌ Brak SLACK_BOT_TOKEN")
            return False
        
        client = WebClient(token=bot_token)
        
        # Test autoryzacji
        response = client.auth_test()
        
        if response['ok']:
            print(f"  ✅ Slack API działa! Bot: {response['user']}")
            
            # Test dostępu do kanału
            channel_id = os.getenv('SLACK_CHANNEL_ID')
            if channel_id:
                try:
                    channel_info = client.conversations_info(channel=channel_id)
                    if channel_info['ok']:
                        print(f"  ✅ Dostęp do kanału: #{channel_info['channel']['name']}")
                    else:
                        print(f"  ⚠️ Brak dostępu do kanału {channel_id}")
                except:
                    print(f"  ⚠️ Nie można sprawdzić kanału {channel_id}")
            
            return True
        else:
            print(f"  ❌ Błąd autoryzacji Slack: {response.get('error', 'Unknown')}")
            return False
            
    except ImportError:
        print("  ❌ Brak biblioteki slack_sdk (pip install slack_sdk)")
        return False
    except Exception as e:
        print(f"  ❌ Błąd Slack API: {e}")
        return False

def test_configuration_files():
    """Test plików konfiguracyjnych"""
    print("\n⚙️ Testowanie plików konfiguracyjnych...")
    
    # Test settings.py
    try:
        from config.settings import get_config
        config = get_config()
        
        if config.validate_config():
            print("  ✅ Plik settings.py jest prawidłowy")
        else:
            print("  ❌ Błędy w pliku settings.py")
            return False
            
    except ImportError as e:
        print(f"  ❌ Nie można załadować config.settings: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Błąd konfiguracji: {e}")
        return False
    
    # Test eden_config.json
    config_path = "autogen/config/eden_config.json"
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            print(f"  ✅ Plik {config_path} jest prawidłowy")
        except json.JSONDecodeError as e:
            print(f"  ❌ Błąd JSON w {config_path}: {e}")
            return False
    else:
        print(f"  ⚠️ Plik {config_path} nie istnieje")
    
    return True

def test_database_connection():
    """Test połączenia z bazą danych"""
    print("\n🗄️ Testowanie bazy danych...")
    
    db_type = os.getenv('DATABASE_TYPE', 'sqlite')
    
    if db_type == 'sqlite':
        try:
            import sqlite3
            db_path = os.getenv('DATABASE_PATH', 'data/eden.db')
            
            # Utwórz katalog jeśli nie istnieje
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            # Test połączenia
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                
            if result:
                print(f"  ✅ SQLite działa! Ścieżka: {db_path}")
                return True
            else:
                print("  ❌ Błąd SQLite")
                return False
                
        except Exception as e:
            print(f"  ❌ Błąd SQLite: {e}")
            return False
    
    elif db_type == 'mysql':
        try:
            import mysql.connector
            
            config = {
                'host': os.getenv('MYSQL_HOST', 'localhost'),
                'port': int(os.getenv('MYSQL_PORT', 3306)),
                'user': os.getenv('MYSQL_USERNAME'),
                'password': os.getenv('MYSQL_PASSWORD'),
                'database': os.getenv('MYSQL_DATABASE')
            }
            
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
            if result:
                print(f"  ✅ MySQL działa! Baza: {config['database']}")
                conn.close()
                return True
            else:
                print("  ❌ Błąd MySQL")
                return False
                
        except ImportError:
            print("  ❌ Brak biblioteki mysql-connector-python")
            return False
        except Exception as e:
            print(f"  ❌ Błąd MySQL: {e}")
            return False
    
    else:
        print(f"  ❌ Nieznany typ bazy danych: {db_type}")
        return False

def test_budget_manager():
    """Test Budget Manager"""
    print("\n💰 Testowanie Budget Manager...")
    
    try:
        from config.settings import get_config
        from managers.budget_manager import BudgetManager
        
        config = get_config()
        budget_manager = BudgetManager(config)
        
        # Test podstawowych funkcji
        status = budget_manager.get_budget_status()
        print(f"  ✅ Status budżetu: {status['color']} {status['status']}")
        
        # Test przewidywania kosztów
        prediction = budget_manager.get_cost_prediction()
        print(f"  ✅ Przewidywane koszty: ${prediction['predicted_daily_cost']:.2f}")
        
        # Test mnożnika dopaminy
        multiplier = budget_manager.get_request_frequency_multiplier()
        print(f"  ✅ Mnożnik dopaminy: {multiplier:.2f}x")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Błąd Budget Manager: {e}")
        return False

def test_directory_structure():
    """Test struktury katalogów"""
    print("\n📁 Testowanie struktury katalogów...")
    
    required_dirs = [
        'autogen',
        'autogen/config',
        'autogen/layers',
        'autogen/managers',
        'data',
        'data/logs'
    ]
    
    required_files = [
        'autogen/consciousness_core.py',
        'autogen/models.py',
        'autogen/config/settings.py',
        'autogen/layers/emotional.py',
        'autogen/managers/budget_manager.py',
        'install_eden.sh',
        'adam_control_eden.sh'
    ]
    
    missing_dirs = []
    missing_files = []
    
    for directory in required_dirs:
        if not os.path.exists(directory):
            missing_dirs.append(directory)
        else:
            print(f"  ✅ {directory}/")
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"  ✅ {file_path}")
    
    if missing_dirs:
        print(f"  ❌ Brakujące katalogi: {', '.join(missing_dirs)}")
        return False
    
    if missing_files:
        print(f"  ❌ Brakujące pliki: {', '.join(missing_files)}")
        return False
    
    print("  ✅ Struktura katalogów jest kompletna!")
    return True

def main():
    """Główna funkcja testowa"""
    print("🌱 Adam Clay Eden - Test Konfiguracji\n")
    print("=" * 50)
    
    tests = [
        ("Struktura katalogów", test_directory_structure),
        ("Zmienne środowiskowe", test_environment_variables),
        ("Pliki konfiguracyjne", test_configuration_files),
        ("Baza danych", test_database_connection),
        ("Budget Manager", test_budget_manager),
        ("Anthropic API", test_anthropic_api),
        ("Slack API", test_slack_api),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"  ❌ Nieoczekiwany błąd w {test_name}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Wyniki testów: {passed}/{total} przeszło pomyślnie")
    
    if passed == total:
        print("🎉 Wszystkie testy przeszły! Adam Clay Eden jest gotowy!")
        return 0
    else:
        print("⚠️ Niektóre testy nie przeszły. Sprawdź konfigurację.")
        print("\n💡 Wskazówki:")
        print("1. Uruchom ./install_eden.sh jeśli nie był uruchamiany")
        print("2. Skopiuj env.example do .env i wypełnij własnymi kluczami")
        print("3. Zobacz SETUP_INTEGRATIONS.md dla szczegółowych instrukcji")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 