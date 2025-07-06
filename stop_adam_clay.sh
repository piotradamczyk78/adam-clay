#!/bin/bash

echo "🛑 ADAM CLAY - STOP SYSTEMU"
echo "==========================="
echo ""

# Sprawdź jakie komponenty działają
laravel_pid=$(pgrep -f "php artisan serve")
consciousness_pid=$(pgrep -f "python3 main.py")

if [[ -z "$laravel_pid" ]] && [[ -z "$consciousness_pid" ]]; then
    echo "ℹ️  Adam Clay nie jest uruchomiony"
    echo ""
    echo "💡 Aby uruchomić system:"
    echo "   ./start_adam_clay.sh"
    exit 0
fi

echo "🔍 AKTYWNE KOMPONENTY SYSTEMU:"
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

# KROK 1: Zatrzymaj Consciousness (gracefully przez API jeśli możliwe)
if [[ -n "$consciousness_pid" ]]; then
    echo "🧠 KROK 1: ZATRZYMYWANIE CONSCIOUSNESS"
    echo "===================================="
    
    # Spróbuj zatrzymać przez Laravel API jeśli Laravel działa
    if [[ -n "$laravel_pid" ]]; then
        echo "🔗 Próbuję zatrzymać consciousness przez Laravel API..."
        
        response=$(curl -s -X POST -w "%{http_code}" -o /tmp/consciousness_stop.json "http://adamclay.local:8004/api/consciousness/stop" 2>/dev/null)
        http_code="${response: -3}"
        
        if [[ "$http_code" == "200" ]]; then
            echo "   ✅ Consciousness zatrzymany przez API"
            
            # Sprawdź czy proces rzeczywiście się zatrzymał
            sleep 3
            new_consciousness_pid=$(pgrep -f "python3 main.py")
            if [[ -z "$new_consciousness_pid" ]]; then
                echo "   ✅ Proces consciousness zatrzymany pomyślnie"
                consciousness_pid=""
            else
                echo "   ⚠️  Proces consciousness nadal aktywny - wymuszę zatrzymanie"
            fi
        else
            echo "   ⚠️  API nie odpowiedział - zatrzymuję bezpośrednio"
        fi
        
        rm -f /tmp/consciousness_stop.json
    fi
    
    # Jeśli proces nadal działa, zatrzymaj bezpośrednio
    if [[ -n "$consciousness_pid" ]]; then
        current_consciousness_pid=$(pgrep -f "python3 main.py")
        if [[ -n "$current_consciousness_pid" ]]; then
            echo "🛑 Zatrzymuję consciousness bezpośrednio (PID: $current_consciousness_pid)..."
            
            # Graceful shutdown (SIGTERM)
            kill -TERM $current_consciousness_pid 2>/dev/null
            
            # Czekaj na zatrzymanie
            echo -n "   ⏳ Czekam na zatrzymanie"
            for i in {1..10}; do
                sleep 1
                echo -n "."
                
                if ! kill -0 $current_consciousness_pid 2>/dev/null; then
                    echo ""
                    echo "   ✅ Consciousness zatrzymany gracefully"
                    consciousness_pid=""
                    break
                fi
            done
            
            # Jeśli nadal działa, wymuś zatrzymanie
            if [[ -n "$consciousness_pid" ]]; then
                echo ""
                echo "   ⚠️  Wymuszam zatrzymanie consciousness..."
                kill -KILL $current_consciousness_pid 2>/dev/null
                sleep 2
                
                if ! kill -0 $current_consciousness_pid 2>/dev/null; then
                    echo "   ✅ Consciousness zatrzymany wymuszenie"
                    consciousness_pid=""
                else
                    echo "   ❌ Nie udało się zatrzymać consciousness (PID: $current_consciousness_pid)"
                fi
            fi
        fi
    fi
    
    echo ""
fi

# KROK 2: Zatrzymaj Laravel
if [[ -n "$laravel_pid" ]]; then
    echo "🌐 KROK 2: ZATRZYMYWANIE LARAVEL"
    echo "==============================="
    
    ./stop_laravel.sh
    
    # Sprawdź wynik
    if [[ $? -eq 0 ]]; then
        sleep 2
        new_laravel_pid=$(pgrep -f "php artisan serve")
        if [[ -z "$new_laravel_pid" ]]; then
            echo "✅ Laravel zatrzymany pomyślnie"
            laravel_pid=""
        else
            echo "⚠️  Laravel może nadal działać (PID: $new_laravel_pid)"
        fi
    else
        echo "❌ Problem z zatrzymywaniem Laravel"
    fi
    
    echo ""
fi

# KROK 3: Sprawdź czy wszystko się zatrzymało
echo "🔍 WERYFIKACJA ZATRZYMANIA:"
echo "=========================="

final_laravel_pid=$(pgrep -f "php artisan serve")
final_consciousness_pid=$(pgrep -f "python3 main.py")

all_stopped=true

if [[ -n "$final_laravel_pid" ]]; then
    echo "   🌐 Laravel API: ⚠️  Nadal aktywny (PID: $final_laravel_pid)"
    all_stopped=false
else
    echo "   🌐 Laravel API: ✅ Zatrzymany"
fi

if [[ -n "$final_consciousness_pid" ]]; then
    echo "   🧠 Consciousness: ⚠️  Nadal aktywny (PID: $final_consciousness_pid)"
    all_stopped=false
else
    echo "   🧠 Consciousness: ✅ Zatrzymany"
fi

echo ""

if [[ "$all_stopped" == "true" ]]; then
    echo "🎉 ADAM CLAY SYSTEM ZATRZYMANY POMYŚLNIE!"
    echo "========================================"
    echo ""
    echo "💡 Aby uruchomić ponownie:"
    echo "   ./start_adam_clay.sh"
    echo ""
    echo "🧹 Aby zresetować system (wyczyścić dane):"
    echo "   ./reset_adam_clay.sh"
    echo ""
    echo "📊 Aby sprawdzić status:"
    echo "   ./status_adam_clay.sh"
    echo ""
    
else
    echo "⚠️  NIEKTÓRE KOMPONENTY NADAL DZIAŁAJĄ"
    echo "====================================="
    echo ""
    
    if [[ -n "$final_laravel_pid" ]]; then
        echo "🔧 Laravel nadal aktywny:"
        echo "   kill -KILL $final_laravel_pid"
    fi
    
    if [[ -n "$final_consciousness_pid" ]]; then
        echo "🔧 Consciousness nadal aktywny:"
        echo "   kill -KILL $final_consciousness_pid"
    fi
    
    echo ""
    echo "💡 Aby wymusić zatrzymanie wszystkich procesów:"
    echo "   pkill -f 'php artisan serve'"
    echo "   pkill -f 'python3 main.py'"
    echo ""
    
    exit 1
fi 