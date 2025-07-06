#!/bin/bash

echo "🛑 LARAVEL - STOP SERWERA"
echo "========================="
echo ""

# Znajdź PID procesu Laravel
pid=$(pgrep -f "php artisan serve")

if [[ -z "$pid" ]]; then
    echo "ℹ️  Laravel serwer nie jest uruchomiony"
    echo ""
    echo "💡 Aby uruchomić serwer:"
    echo "   ./start_laravel.sh"
    exit 0
fi

echo "🔍 Znaleziony proces Laravel:"

# Pokaż szczegóły procesu
process_info=$(ps aux | grep "$pid" | grep -v grep | head -1)
if [[ -n "$process_info" ]]; then
    echo "   📊 PID: $pid"
    
    # Wyciągnij host i port z linii procesu
    if [[ "$process_info" =~ --host=([^[:space:]]+) ]]; then
        host="${BASH_REMATCH[1]}"
        echo "   🌐 Host: $host"
    fi
    
    if [[ "$process_info" =~ --port=([0-9]+) ]]; then
        port="${BASH_REMATCH[1]}"
        echo "   🔌 Port: $port"
    fi
fi

echo ""
echo "🛑 Zatrzymuję serwer Laravel..."

# Próba graceful shutdown (SIGTERM)
kill -TERM $pid 2>/dev/null

# Czekaj na zatrzymanie procesu
echo -n "   ⏳ Czekam na zatrzymanie procesu"
for i in {1..10}; do
    sleep 1
    echo -n "."
    
    # Sprawdź czy proces się zatrzymał
    if ! kill -0 $pid 2>/dev/null; then
        echo ""
        echo "   ✅ Proces zatrzymany gracefully"
        
        echo ""
        echo "🎉 LARAVEL SERWER ZATRZYMANY"
        echo ""
        echo "💡 Aby uruchomić ponownie:"
        echo "   ./start_laravel.sh"
        echo ""
        echo "🔄 Aby zrestartować:"
        echo "   ./restart_laravel.sh"
        
        exit 0
    fi
done

echo ""
echo "⚠️  Proces nie zatrzymał się gracefully, wymuszam zatrzymanie..."

# Force kill (SIGKILL)
kill -KILL $pid 2>/dev/null

# Sprawdź czy wymuszenie zadziałało
sleep 2
if ! kill -0 $pid 2>/dev/null; then
    echo "   ✅ Proces zatrzymany wymuszenie"
    
    echo ""
    echo "🎉 LARAVEL SERWER ZATRZYMANY"
    echo ""
    echo "💡 Aby uruchomić ponownie:"
    echo "   ./start_laravel.sh"
    
else
    echo "   ❌ Nie udało się zatrzymać procesu $pid"
    echo ""
    echo "🆘 MANUAL INTERVENTION NEEDED:"
    echo "   Spróbuj ręcznego zatrzymania:"
    echo "   sudo kill -KILL $pid"
    echo ""
    echo "   Lub restart systemu jeśli problem persistuje"
    exit 1
fi 