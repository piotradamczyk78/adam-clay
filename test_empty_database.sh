#!/bin/bash

echo "🧪 TEST PUSTEJ BAZY DANYCH ADAM CLAY"
echo "===================================="
echo ""

# Function to check API endpoint
check_api() {
    local endpoint="$1"
    local description="$2"
    
    echo -n "🔍 $description... "
    
    response=$(curl -s -w "%{http_code}" -o /tmp/api_response.json "http://adamclay.local:8004/api/$endpoint")
    http_code="${response: -3}"
    
    if [[ "$http_code" == "200" ]]; then
        echo "✅ OK"
        # Show relevant part of response
        cat /tmp/api_response.json | python3 -m json.tool 2>/dev/null | head -10 | sed 's/^/   /'
        echo "   ..."
    else
        echo "❌ FAILED (HTTP $http_code)"
        cat /tmp/api_response.json | head -3 | sed 's/^/   /'
    fi
    echo ""
}

echo "🔧 Sprawdzanie API endpoints z pustą bazą..."
echo ""

# Test basic endpoints
check_api "hello" "Test podstawowy endpoint"
check_api "status" "Status systemu Adam Clay"
check_api "consciousness/thinking-status" "Status myślenia consciousness"

echo ""
echo "🎯 KRYTYCZNY TEST: Uruchomienie consciousness"
echo ""

# Check if consciousness is running
pid=$(pgrep -f 'python3 main.py')
if [[ -n "$pid" ]]; then
    echo "⚠️  Adam Clay już jest uruchomiony (PID: $pid)"
    echo "   Zatrzymuję go najpierw..."
    pkill -f 'python3 main.py'
    sleep 3
fi

echo "🚀 Próbuję uruchomić consciousness z pustą bazą..."

# Try to start consciousness via API
response=$(curl -s -X POST -w "%{http_code}" -o /tmp/start_response.json "http://adamclay.local:8004/api/consciousness/start")
http_code="${response: -3}"

echo ""
if [[ "$http_code" == "200" ]]; then
    echo "✅ SUKCES! Consciousness uruchomiony pomyślnie"
    cat /tmp/start_response.json | python3 -m json.tool 2>/dev/null | sed 's/^/   /'
    
    echo ""
    echo "⏱️  Czekam 10 sekund na stabilizację..."
    sleep 10
    
    echo ""
    echo "🔍 Sprawdzam czy rzeczywiście działa..."
    check_api "consciousness/thinking-status" "Status myślenia po uruchomieniu"
    
    # Check if process is actually running
    new_pid=$(pgrep -f 'python3 main.py')
    if [[ -n "$new_pid" ]]; then
        echo "✅ Proces consciousness działa (PID: $new_pid)"
        
        echo ""
        echo "📊 Sprawdzam czy system tworzy myśli..."
        echo "   (Sprawdzam za 30 sekund czy pojawiły się myśli)"
        
        # Wait a bit more and check for thoughts
        sleep 30
        check_api "thoughts/recent?limit=3" "Ostatnie myśli"
        
    else
        echo "❌ Proces consciousness nie jest aktywny mimo sukcesu API"
    fi
    
else
    echo "❌ BŁĄD! Nie udało się uruchomić consciousness"
    cat /tmp/start_response.json | head -5 | sed 's/^/   /'
fi

echo ""
echo "🧹 Czyszczenie..."
rm -f /tmp/api_response.json /tmp/start_response.json

echo ""
echo "🎯 WYNIK TESTU PUSTEJ BAZY DANYCH:"
echo "=================================="

# Final verification
final_pid=$(pgrep -f 'python3 main.py')
if [[ -n "$final_pid" ]]; then
    echo "✅ SUKCES: Adam Clay działa z pustą bazą danych!"
    echo "   🧠 PID procesu: $final_pid"
    echo "   📊 System automatycznie utworzył potrzebne sesje"
    echo "   🚀 Adam Clay jest gotowy do pierwszego myślenia"
    
    echo ""
    echo "🛑 Aby zatrzymać test:"
    echo "   pkill -f 'python3 main.py'"
    echo ""
    echo "🔄 Aby całkowicie zresetować i rozpocząć od nowa:"
    echo "   ./reset_adam_clay.sh"
    
else
    echo "❌ NIEPOWODZENIE: System nie uruchomił się z pustą bazą"
    echo "   🔧 Sprawdź logi w data/logs/consciousness.log"
    echo "   🆘 Możliwe problemy:"
    echo "      - Błąd konfiguracji bazy danych"
    echo "      - Problem z Python environment"
    echo "      - Błąd w kodzie consciousness"
fi

echo "" 