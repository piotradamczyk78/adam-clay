#!/bin/bash

echo "🔄 LARAVEL - RESTART SERWERA"
echo "============================"
echo ""

# Sprawdź czy jesteśmy w odpowiednim katalogu
if [[ ! -f "start_laravel.sh" ]] || [[ ! -f "stop_laravel.sh" ]]; then
    echo "❌ Błąd: Nie znaleziono skryptów start_laravel.sh lub stop_laravel.sh"
    echo "   📁 Upewnij się, że uruchamiasz skrypt z głównego katalogu AdamClay"
    exit 1
fi

# Sprawdź czy Laravel działa
pid=$(pgrep -f "php artisan serve")

if [[ -n "$pid" ]]; then
    echo "🔍 Laravel serwer jest uruchomiony (PID: $pid)"
    echo ""
    echo "🛑 KROK 1: Zatrzymywanie serwera..."
    echo "==============================="
    
    # Zatrzymaj Laravel
    ./stop_laravel.sh
    
    # Sprawdź czy rzeczywiście się zatrzymał
    sleep 2
    new_pid=$(pgrep -f "php artisan serve")
    if [[ -n "$new_pid" ]]; then
        echo "❌ Błąd: Proces Laravel nadal działa (PID: $new_pid)"
        echo "   🔧 Spróbuj ręcznego zatrzymania przed restartem"
        exit 1
    fi
    
    echo ""
    echo "✅ Serwer zatrzymany pomyślnie"
    
else
    echo "ℹ️  Laravel serwer nie jest uruchomiony"
fi

echo ""
echo "🚀 KROK 2: Uruchamianie serwera..."
echo "=================================="

# Krótka pauza przed uruchomieniem
sleep 3

# Uruchom Laravel
./start_laravel.sh

# Sprawdź wynik uruchomienia
if [[ $? -eq 0 ]]; then
    # Dodatkowo sprawdź czy proces rzeczywiście działa
    sleep 3
    final_pid=$(pgrep -f "php artisan serve")
    
    if [[ -n "$final_pid" ]]; then
        echo ""
        echo "🎉 RESTART ZAKOŃCZONY POMYŚLNIE!"
        echo "==============================="
        echo ""
        echo "✅ Laravel serwer działa (PID: $final_pid)"
        
        # Sprawdź czy serwer odpowiada
        echo "🔍 Testowanie połączenia..."
        sleep 2
        
        response=$(curl -s -w "%{http_code}" -o /tmp/laravel_test.json "http://adamclay.local:8004/api/hello" 2>/dev/null)
        http_code="${response: -3}"
        
        if [[ "$http_code" == "200" ]]; then
            echo "   ✅ API odpowiada poprawnie (HTTP 200)"
            message=$(cat /tmp/laravel_test.json 2>/dev/null | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
            if [[ -n "$message" ]]; then
                echo "   💬 Odpowiedź: $message"
            fi
        else
            echo "   ⚠️  API nie odpowiada jeszcze - może potrzebować chwili na pełne uruchomienie"
        fi
        
        rm -f /tmp/laravel_test.json
        
        echo ""
        echo "🌐 DOSTĘPNE USŁUGI:"
        echo "   Dashboard: http://adamclay.local:8004/consciousness"
        echo "   API Test: http://adamclay.local:8004/api/hello"
        echo "   Status: ./status_laravel.sh"
        
    else
        echo ""
        echo "❌ BŁĄD: Proces się uruchomił ale nie działa"
        echo "   📋 Sprawdź logi: tail -f data/logs/laravel_server.log"
        exit 1
    fi
    
else
    echo ""
    echo "❌ BŁĄD PODCZAS URUCHAMIANIA"
    echo "   🔧 Sprawdź konfigurację i spróbuj ponownie"
    echo "   📋 Logi: tail -f data/logs/laravel_server.log"
    exit 1
fi 