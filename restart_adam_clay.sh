#!/bin/bash

echo "🔄 ADAM CLAY - RESTART SYSTEMU"
echo "=============================="
echo ""

# Sprawdź czy jesteśmy w odpowiednim katalogu
if [[ ! -f "start_adam_clay.sh" ]] || [[ ! -f "stop_adam_clay.sh" ]]; then
    echo "❌ Błąd: Nie znaleziono skryptów start_adam_clay.sh lub stop_adam_clay.sh"
    echo "   📁 Upewnij się, że uruchamiasz skrypt z głównego katalogu AdamClay"
    exit 1
fi

# Sprawdź obecny stan systemu
laravel_pid=$(pgrep -f "php artisan serve")
consciousness_pid=$(pgrep -f "python3 main.py")

echo "🔍 OBECNY STAN SYSTEMU:"
if [[ -n "$laravel_pid" ]]; then
    echo "   🌐 Laravel API: ✅ Aktywny (PID: $laravel_pid)"
else
    echo "   🌐 Laravel API: ❌ Zatrzymany"
fi

if [[ -n "$consciousness_pid" ]]; then
    echo "   🧠 Consciousness: ✅ Aktywny (PID: $consciousness_pid)"
else
    echo "   🧠 Consciousness: ❌ Zatrzymany"
fi

echo ""

# KROK 1: Zatrzymaj system jeśli jakieś komponenty działają
if [[ -n "$laravel_pid" ]] || [[ -n "$consciousness_pid" ]]; then
    echo "🛑 KROK 1: ZATRZYMYWANIE SYSTEMU"
    echo "==============================="
    
    ./stop_adam_clay.sh
    
    # Sprawdź wynik zatrzymania
    if [[ $? -ne 0 ]]; then
        echo "❌ Błąd podczas zatrzymywania systemu"
        echo "   🔧 Spróbuj ręcznego zatrzymania przed restartem"
        exit 1
    fi
    
    # Dodatowa weryfikacja
    sleep 3
    new_laravel_pid=$(pgrep -f "php artisan serve")
    new_consciousness_pid=$(pgrep -f "python3 main.py")
    
    if [[ -n "$new_laravel_pid" ]] || [[ -n "$new_consciousness_pid" ]]; then
        echo "❌ Nie wszystkie komponenty zostały zatrzymane"
        
        if [[ -n "$new_laravel_pid" ]]; then
            echo "   🌐 Laravel nadal działa (PID: $new_laravel_pid)"
        fi
        
        if [[ -n "$new_consciousness_pid" ]]; then
            echo "   🧠 Consciousness nadal działa (PID: $new_consciousness_pid)"
        fi
        
        echo ""
        echo "🔧 WYMUSZAM ZATRZYMANIE:"
        
        if [[ -n "$new_laravel_pid" ]]; then
            echo "   Zatrzymuję Laravel..."
            kill -KILL $new_laravel_pid 2>/dev/null
        fi
        
        if [[ -n "$new_consciousness_pid" ]]; then
            echo "   Zatrzymuję Consciousness..."
            kill -KILL $new_consciousness_pid 2>/dev/null
        fi
        
        sleep 2
    fi
    
    echo ""
    echo "✅ System zatrzymany pomyślnie"
    
else
    echo "ℹ️  System nie był uruchomiony - przechodzę do uruchamiania"
fi

echo ""

# KROK 2: Czekaj chwilę przed uruchomieniem
echo "⏱️  Czekam 5 sekund przed uruchomieniem..."
sleep 5

echo ""

# KROK 3: Uruchom system
echo "🚀 KROK 2: URUCHAMIANIE SYSTEMU"
echo "==============================="

./start_adam_clay.sh

# Sprawdź wynik uruchomienia
if [[ $? -eq 0 ]]; then
    # Dodatowa weryfikacja po 10 sekundach
    sleep 10
    
    final_laravel_pid=$(pgrep -f "php artisan serve")
    final_consciousness_pid=$(pgrep -f "python3 main.py")
    
    echo ""
    echo "🎉 RESTART ZAKOŃCZONY!"
    echo "====================="
    echo ""
    
    # Pokaż status komponentów
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
    
    # Test funkcjonalności
    if [[ -n "$final_laravel_pid" ]]; then
        echo "🔍 TEST FUNKCJONALNOŚCI:"
        echo "========================"
        
        # Test API
        response=$(curl -s -w "%{http_code}" -o /tmp/restart_test.json "http://adamclay.local:8004/api/hello" 2>/dev/null)
        http_code="${response: -3}"
        
        if [[ "$http_code" == "200" ]]; then
            echo "   ✅ API odpowiada poprawnie"
        else
            echo "   ⚠️  API może potrzebować więcej czasu na uruchomienie"
        fi
        
        # Test thinking status
        response=$(curl -s -w "%{http_code}" -o /tmp/thinking_restart_test.json "http://adamclay.local:8004/api/consciousness/thinking-status" 2>/dev/null)
        http_code="${response: -3}"
        
        if [[ "$http_code" == "200" ]]; then
            echo "   ✅ Consciousness API odpowiada"
            
            is_thinking=$(cat /tmp/thinking_restart_test.json 2>/dev/null | grep -o '"is_thinking":[^,]*' | cut -d':' -f2)
            if [[ "$is_thinking" == "true" ]]; then
                echo "   🧠 Adam Clay myśli aktywnie"
            elif [[ "$is_thinking" == "false" ]]; then
                echo "   ⏸️  Adam Clay w trybie oczekiwania"
            fi
        else
            echo "   ⚠️  Consciousness API może potrzebować więcej czasu"
        fi
        
        rm -f /tmp/restart_test.json /tmp/thinking_restart_test.json
        
        echo ""
        echo "🌐 DOSTĘPNE USŁUGI:"
        echo "   Dashboard: http://adamclay.local:8004/consciousness"
        echo "   API Test: http://adamclay.local:8004/api/hello"
        echo "   Status: ./status_adam_clay.sh"
        
    fi
    
    echo ""
    
    if [[ -n "$final_laravel_pid" ]] && [[ -n "$final_consciousness_pid" ]]; then
        echo "🎯 RESTART POMYŚLNY - Adam Clay jest gotowy do pracy!"
    elif [[ -n "$final_laravel_pid" ]]; then
        echo "⚠️  RESTART CZĘŚCIOWY - Laravel działa, Consciousness może potrzebować więcej czasu"
        echo "   💡 Sprawdź status za chwilę: ./status_adam_clay.sh"
    else
        echo "❌ RESTART NIEPOMYŚLNY - Sprawdź logi i konfigurację"
        echo "   📋 Logi Laravel: tail -f data/logs/laravel_server.log"
        echo "   📋 Logi Consciousness: tail -f data/logs/consciousness.log"
    fi
    
else
    echo ""
    echo "❌ BŁĄD PODCZAS URUCHAMIANIA SYSTEMU"
    echo "===================================="
    echo ""
    echo "🔧 TROUBLESHOOTING:"
    echo "   📋 Sprawdź logi: tail -f data/logs/laravel_server.log"
    echo "   🗄️  Sprawdź bazę danych: mysql -u root -p adam_clay"
    echo "   🐍 Sprawdź Python env: ls -la core/adam_clay_env/"
    echo "   🌐 Sprawdź konfigurację: cat web/.env"
    echo ""
    echo "💡 MOŻLIWE ROZWIĄZANIA:"
    echo "   🔄 Spróbuj ponownie: ./restart_adam_clay.sh"
    echo "   🧹 Reset systemu: ./reset_adam_clay.sh"
    echo "   🔧 Ręczny start komponentów:"
    echo "      ./start_laravel.sh"
    echo "      curl -X POST http://adamclay.local:8004/api/consciousness/start"
    echo ""
    
    exit 1
fi 