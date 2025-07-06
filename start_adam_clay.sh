#!/bin/bash

echo "🚀 ADAM CLAY - START SYSTEMU"
echo "============================"
echo ""

# Sprawdź czy jesteśmy w odpowiednim katalogu
if [[ ! -d "web" ]] || [[ ! -d "core" ]]; then
    echo "❌ Błąd: Nie znaleziono katalogów 'web' i 'core'"
    echo "   📁 Upewnij się, że uruchamiasz skrypt z głównego katalogu AdamClay"
    exit 1
fi

echo "🔧 SPRAWDZANIE KOMPONENTÓW SYSTEMU:"
echo "==================================="

# Sprawdź Laravel
laravel_pid=$(pgrep -f "php artisan serve")
laravel_status="❌ Zatrzymany"
if [[ -n "$laravel_pid" ]]; then
    laravel_status="✅ Aktywny (PID: $laravel_pid)"
fi

# Sprawdź Consciousness
consciousness_pid=$(pgrep -f "python3 main.py")
consciousness_status="❌ Zatrzymany"
if [[ -n "$consciousness_pid" ]]; then
    consciousness_status="✅ Aktywny (PID: $consciousness_pid)"
fi

echo "   🌐 Laravel API: $laravel_status"
echo "   🧠 Consciousness: $consciousness_status"
echo ""

# KROK 1: Uruchom Laravel jeśli nie działa
if [[ -z "$laravel_pid" ]]; then
    echo "🌐 KROK 1: URUCHAMIANIE LARAVEL API"
    echo "=================================="
    
    ./start_laravel.sh
    
    if [[ $? -ne 0 ]]; then
        echo "❌ Błąd uruchamiania Laravel - zatrzymuję proces"
        exit 1
    fi
    
    echo ""
    echo "✅ Laravel uruchomiony pomyślnie"
    
    # Sprawdź czy Laravel rzeczywiście odpowiada
    echo "🔍 Testowanie API..."
    sleep 3
    
    response=$(curl -s -w "%{http_code}" -o /tmp/adam_start_test.json "http://adamclay.local:8004/api/hello" 2>/dev/null)
    http_code="${response: -3}"
    
    if [[ "$http_code" == "200" ]]; then
        echo "   ✅ Laravel API odpowiada poprawnie"
    else
        echo "   ⚠️  Laravel API nie odpowiada jeszcze - czekam dłużej..."
        sleep 5
        
        response=$(curl -s -w "%{http_code}" -o /tmp/adam_start_test.json "http://adamclay.local:8004/api/hello" 2>/dev/null)
        http_code="${response: -3}"
        
        if [[ "$http_code" != "200" ]]; then
            echo "   ❌ Laravel API nie odpowiada - problem z konfiguracją"
            exit 1
        fi
    fi
    
    rm -f /tmp/adam_start_test.json
    
else
    echo "✅ Laravel już działa - pomijam uruchomienie"
fi

echo ""

# KROK 2: Uruchom Consciousness jeśli nie działa
if [[ -z "$consciousness_pid" ]]; then
    echo "🧠 KROK 2: URUCHAMIANIE CONSCIOUSNESS"
    echo "===================================="
    
    # Sprawdź czy istnieje Python environment
    if [[ ! -d "core/adam_clay_env" ]]; then
        echo "❌ Błąd: Nie znaleziono Python environment w core/adam_clay_env"
        echo "   🔧 Uruchom setup środowiska przed uruchomieniem"
        exit 1
    fi
    
    # Sprawdź czy istnieje main.py
    if [[ ! -f "core/main.py" ]]; then
        echo "❌ Błąd: Nie znaleziono core/main.py"
        exit 1
    fi
    
    echo "🧠 Uruchamiam consciousness przez Laravel API..."
    
    # Użyj Laravel API do uruchomienia consciousness
    response=$(curl -s -X POST -w "%{http_code}" -o /tmp/consciousness_start.json "http://adamclay.local:8004/api/consciousness/start")
    http_code="${response: -3}"
    
    if [[ "$http_code" == "200" ]]; then
        echo "   ✅ Consciousness uruchomiony przez Laravel API"
        
        result=$(cat /tmp/consciousness_start.json 2>/dev/null)
        echo "   📄 Odpowiedź: $result"
        
        # Sprawdź czy proces rzeczywiście działa
        sleep 5
        new_consciousness_pid=$(pgrep -f "python3 main.py")
        if [[ -n "$new_consciousness_pid" ]]; then
            echo "   🧠 Proces consciousness aktywny (PID: $new_consciousness_pid)"
        else
            echo "   ⚠️  Proces consciousness może potrzebować więcej czasu na start"
        fi
        
    else
        echo "   ❌ Błąd uruchamiania consciousness przez API (HTTP $http_code)"
        
        error_msg=$(cat /tmp/consciousness_start.json 2>/dev/null)
        echo "   📄 Błąd: $error_msg"
        
        exit 1
    fi
    
    rm -f /tmp/consciousness_start.json
    
else
    echo "✅ Consciousness już działa - pomijam uruchomienie"
fi

echo ""
echo "🎉 ADAM CLAY SYSTEM URUCHOMIONY!"
echo "==============================="
echo ""

# Pokaż końcowy status
final_laravel_pid=$(pgrep -f "php artisan serve")
final_consciousness_pid=$(pgrep -f "python3 main.py")

echo "📊 STATUS KOMPONENTÓW:"
if [[ -n "$final_laravel_pid" ]]; then
    echo "   🌐 Laravel API: ✅ Aktywny (PID: $final_laravel_pid)"
else
    echo "   🌐 Laravel API: ❌ Problem z uruchomieniem"
fi

if [[ -n "$final_consciousness_pid" ]]; then
    echo "   🧠 Consciousness: ✅ Aktywny (PID: $final_consciousness_pid)"
else
    echo "   🧠 Consciousness: ⚠️  Może potrzebować więcej czasu"
fi

echo ""
echo "🌐 DOSTĘPNE USŁUGI:"
echo "   Dashboard: http://adamclay.local:8004/consciousness"
echo "   API Test: http://adamclay.local:8004/api/hello"
echo "   Thinking Status: http://adamclay.local:8004/api/consciousness/thinking-status"
echo ""
echo "📊 MONITORING:"
echo "   Status systemu: ./status_adam_clay.sh"
echo "   Status Laravel: ./status_laravel.sh"
echo "   Logi Laravel: tail -f data/logs/laravel_server.log"
echo "   Logi Consciousness: tail -f data/logs/consciousness.log"
echo ""
echo "🛑 ZATRZYMYWANIE:"
echo "   Stop systemu: ./stop_adam_clay.sh"
echo "   Stop Laravel: ./stop_laravel.sh"
echo "   Stop Consciousness: curl -X POST http://adamclay.local:8004/api/consciousness/stop"
echo ""

# Finalny test połączenia po 10 sekundach
echo "🔍 Test pełnej funkcjonalności za 10 sekund..."
sleep 10

# Test thinking status
response=$(curl -s -w "%{http_code}" -o /tmp/final_test.json "http://adamclay.local:8004/api/consciousness/thinking-status" 2>/dev/null)
http_code="${response: -3}"

if [[ "$http_code" == "200" ]]; then
    echo "✅ System pełnie funkcjonalny!"
    
    thinking_status=$(cat /tmp/final_test.json 2>/dev/null | grep -o '"is_thinking":[^,]*' | cut -d':' -f2)
    if [[ "$thinking_status" == "true" ]]; then
        echo "   🧠 Adam Clay myśli aktywnie"
    elif [[ "$thinking_status" == "false" ]]; then
        echo "   ⏸️  Adam Clay w trybie oczekiwania"
    fi
    
else
    echo "⚠️  System uruchomiony ale może potrzebować jeszcze chwili na pełną synchronizację"
fi

rm -f /tmp/final_test.json

echo ""
echo "🎯 Adam Clay jest gotowy do pracy!" 