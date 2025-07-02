#!/bin/bash

echo "🤖 ADAM CLAY - Uruchamianie pierwszego autonomicznego AI freelancera"
echo "================================================================="

# Sprawdź czy jesteśmy w odpowiednim katalogu
if [[ ! -d "adam_clay_env" ]]; then
    echo "❌ Błąd: Nie znajduję katalogu adam_clay_env"
    echo "📍 Przejdź do katalogu adam_clay_project i uruchom ponownie"
    echo "   cd /Users/piotradamczyk/Projects/AdamClay/adam_clay_project"
    echo "   ./start_adam_clay.sh"
    exit 1
fi

# Aktywuj środowisko wirtualne
echo "🔄 Aktywacja środowiska wirtualnego..."
source adam_clay_env/bin/activate

# Sprawdź czy Python działa
if ! command -v python &> /dev/null; then
    echo "❌ Błąd: Python nie jest dostępny po aktywacji środowiska"
    exit 1
fi

echo "✅ Środowisko wirtualne aktywne: $(python --version)"

# Sprawdź czy klucz API jest skonfigurowany
config_key=$(python -c "
import json
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
    key = config.get('api', {}).get('api_key', '')
    if key and key != 'WKLEJ_TUTAJ_SWOJ_KLUCZ_API':
        print(key)
except:
    pass
" 2>/dev/null)

if [[ -n "$config_key" ]]; then
    echo "✅ Klucz API w config.json: ${config_key:0:10}..."
elif [[ -n "$LLM_PROVIDER_API_KEY" ]]; then
    echo "✅ Klucz API w zmiennej środowiskowej: ${LLM_PROVIDER_API_KEY:0:10}..."
else
    echo "🔑 Brak klucza API - uruchamiam konfigurację..."
    python setup_api_key.py
    
    # Sprawdź ponownie po konfiguracji
    config_key=$(python -c "
import json
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
    key = config.get('api', {}).get('api_key', '')
    if key and key != 'WKLEJ_TUTAJ_SWOJ_KLUCZ_API':
        print('OK')
except:
    pass
" 2>/dev/null)
    
    if [[ -z "$config_key" && -z "$LLM_PROVIDER_API_KEY" ]]; then
        echo "❌ Konfiguracja API nie została ukończona"
        echo "💡 Uruchom ponownie: ./start_adam_clay.sh"
        echo "💡 Lub użyj: python add_api_key.py"
        exit 1
    fi
fi

echo ""
echo "🧠 URUCHAMIANIE ŚWIADOMOŚCI ADAM CLAY..."
echo "================================================="
echo "💭 Adam Clay będzie myślał co 1 minutę"
echo "📊 Wszystkie myśli będą wyświetlane w czasie rzeczywistym"
echo "💰 Koszt: ~$0.001-0.01 za myśl"
echo "🛑 Zatrzymaj: Ctrl+C"
echo "================================================="
echo ""

sleep 2

# Uruchom Adam Clay
python main.py 