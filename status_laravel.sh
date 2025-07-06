#!/bin/bash

echo "📊 LARAVEL - STATUS SERWERA"
echo "==========================="
echo ""

# Sprawdź czy proces Laravel działa
pid=$(pgrep -f "php artisan serve")

if [[ -z "$pid" ]]; then
    echo "🔴 LARAVEL SERWER: ZATRZYMANY"
    echo ""
    echo "💡 Aby uruchomić:"
    echo "   ./start_laravel.sh"
    echo ""
    exit 0
fi

echo "🟢 LARAVEL SERWER: AKTYWNY"
echo ""

# Pokaż szczegóły procesu
process_info=$(ps aux | grep "$pid" | grep -v grep | head -1)
if [[ -n "$process_info" ]]; then
    echo "📊 SZCZEGÓŁY PROCESU:"
    echo "   🔍 PID: $pid"
    
    # CPU i pamięć
    cpu=$(echo "$process_info" | awk '{print $3}')
    memory=$(echo "$process_info" | awk '{print $4}')
    echo "   🖥️  CPU: ${cpu}%"
    echo "   💾 RAM: ${memory}%"
    
    # Czas działania
    time_info=$(echo "$process_info" | awk '{print $(NF-1)}')
    echo "   ⏰ Czas działania: $time_info"
    
    # Host i port
    if [[ "$process_info" =~ --host=([^[:space:]]+) ]]; then
        host="${BASH_REMATCH[1]}"
        echo "   🌐 Host: $host"
    fi
    
    if [[ "$process_info" =~ --port=([0-9]+) ]]; then
        port="${BASH_REMATCH[1]}"
        echo "   🔌 Port: $port"
        
        url="http://$host:$port"
        echo "   🔗 URL: $url"
    fi
fi

echo ""

# Test połączenia API
echo "🔍 TEST POŁĄCZENIA API:"
response_time_start=$(date +%s%N)
response=$(curl -s -w "%{http_code}" -o /tmp/laravel_status.json "$url/api/hello" 2>/dev/null)
response_time_end=$(date +%s%N)
http_code="${response: -3}"

# Oblicz czas odpowiedzi w ms
response_time=$(( (response_time_end - response_time_start) / 1000000 ))

if [[ "$http_code" == "200" ]]; then
    echo "   ✅ API dostępne (HTTP 200)"
    echo "   ⚡ Czas odpowiedzi: ${response_time}ms"
    
    # Pokaż wiadomość z API
    message=$(cat /tmp/laravel_status.json 2>/dev/null | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
    if [[ -n "$message" ]]; then
        echo "   💬 Odpowiedź: $message"
    fi
    
    # Sprawdź timestamp
    timestamp=$(cat /tmp/laravel_status.json 2>/dev/null | grep -o '"timestamp":"[^"]*"' | cut -d'"' -f4)
    if [[ -n "$timestamp" ]]; then
        echo "   🕐 Server time: $timestamp"
    fi
    
else
    echo "   ❌ API niedostępne (HTTP $http_code)"
    echo "   ⚡ Czas odpowiedzi: ${response_time}ms"
fi

rm -f /tmp/laravel_status.json

# Test bazy danych
echo ""
echo "🗄️  TEST BAZY DANYCH:"

cd web 2>/dev/null || {
    echo "   ❌ Nie można przejść do katalogu web"
    exit 1
}

db_test=$(php artisan tinker --execute="
try {
    \$pdo = DB::connection()->getPdo();
    echo 'OK';
} catch (Exception \$e) {
    echo 'ERROR: ' . \$e->getMessage();
}
" 2>/dev/null | tail -n +2)

if [[ "$db_test" == "OK" ]]; then
    echo "   ✅ Baza danych dostępna"
    
    # Sprawdź przykładową tabelę
    table_count=$(php artisan tinker --execute="
    try {
        \$count = DB::table('thoughts')->count();
        echo \$count;
    } catch (Exception \$e) {
        echo 'ERROR';
    }
    " 2>/dev/null | tail -n +2)
    
    if [[ "$table_count" =~ ^[0-9]+$ ]]; then
        echo "   📊 Thoughts w bazie: $table_count"
    fi
    
else
    echo "   ❌ Błąd bazy danych: $db_test"
fi

cd - > /dev/null

# Sprawdź logi
echo ""
echo "📋 OSTATNIE LOGI:"

log_file="../data/logs/laravel_server.log"
if [[ -f "$log_file" ]]; then
    echo "   📄 Plik logu: $log_file"
    
    # Pokaż rozmiar pliku
    log_size=$(du -h "$log_file" | cut -f1)
    echo "   📏 Rozmiar: $log_size"
    
    # Pokaż ostatnie 3 linie
    echo "   📰 Ostatnie wpisy:"
    tail -3 "$log_file" 2>/dev/null | sed 's/^/      /'
    
    echo ""
    echo "   💡 Aby zobaczyć więcej logów:"
    echo "      tail -f data/logs/laravel_server.log"
    
else
    echo "   ⚠️  Brak pliku logu: $log_file"
fi

echo ""
echo "🎛️  ZARZĄDZANIE:"
echo "   🛑 Stop: ./stop_laravel.sh"
echo "   🔄 Restart: ./restart_laravel.sh"
echo "   🌐 Dashboard: $url/consciousness"
echo "" 