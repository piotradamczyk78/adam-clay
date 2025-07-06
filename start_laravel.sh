#!/bin/bash

echo "🚀 LARAVEL - START SERWERA"
echo "=========================="
echo ""

# Sprawdź czy Laravel już działa
pid=$(pgrep -f "php artisan serve")
if [[ -n "$pid" ]]; then
    echo "⚠️  Laravel serwer już jest uruchomiony!"
    echo "   🔍 PID: $pid"
    
    # Sprawdź szczegóły procesu
    process_info=$(ps aux | grep "$pid" | grep -v grep | head -1)
    if [[ -n "$process_info" ]]; then
        echo "   📊 Proces: $process_info"
        
        # Wyciągnij host i port z linii procesu
        if [[ "$process_info" =~ --host=([^[:space:]]+) ]]; then
            host="${BASH_REMATCH[1]}"
        else
            host="127.0.0.1"
        fi
        
        if [[ "$process_info" =~ --port=([0-9]+) ]]; then
            port="${BASH_REMATCH[1]}"
        else
            port="8000"
        fi
        
        echo "   🌐 URL: http://$host:$port"
    fi
    
    echo ""
    echo "💡 Aby zatrzymać istniejący serwer:"
    echo "   ./stop_laravel.sh"
    echo ""
    echo "🔄 Aby zrestartować serwer:"
    echo "   ./restart_laravel.sh"
    
    exit 0
fi

echo "🔧 Sprawdzanie konfiguracji Laravel..."

# Sprawdź czy jesteśmy w katalogu projektu
if [[ ! -d "web" ]]; then
    echo "❌ Błąd: Nie znaleziono katalogu 'web' z projektem Laravel"
    echo "   📁 Upewnij się, że uruchamiasz skrypt z głównego katalogu AdamClay"
    exit 1
fi

cd web

# Sprawdź czy istnieje artisan
if [[ ! -f "artisan" ]]; then
    echo "❌ Błąd: Nie znaleziono pliku 'artisan' w katalogu web"
    echo "   📁 Sprawdź czy katalog web zawiera prawidłowy projekt Laravel"
    exit 1
fi

# Sprawdź czy istnieje .env
if [[ ! -f ".env" ]]; then
    echo "⚠️  Uwaga: Brak pliku .env"
    echo "   📝 Kopiuję .env.example do .env..."
    
    if [[ -f ".env.example" ]]; then
        cp .env.example .env
        echo "   ✅ Skopiowano .env.example do .env"
    else
        echo "   ❌ Brak .env.example - utwórz plik .env ręcznie"
        exit 1
    fi
fi

# Sprawdź czy baza danych jest dostępna
echo "🔍 Sprawdzanie połączenia z bazą danych..."
php artisan tinker --execute="
try {
    DB::connection()->getPdo();
    echo 'Database: Connected' . PHP_EOL;
} catch (Exception \$e) {
    echo 'Database Error: ' . \$e->getMessage() . PHP_EOL;
    exit(1);
}
" | tail -n +2

if [[ $? -ne 0 ]]; then
    echo "❌ Błąd połączenia z bazą danych"
    echo "   🔧 Sprawdź konfigurację w pliku .env"
    echo "   📊 Sprawdź czy MySQL działa: brew services list | grep mysql"
    exit 1
fi

echo "   ✅ Baza danych dostępna"

# Uruchom Laravel serwer
echo ""
echo "🚀 Uruchamianie Laravel serwera..."
echo "   🌐 Host: adamclay.local"
echo "   🔌 Port: 8004"
echo "   📁 Katalog: $(pwd)"

# Utwórz katalog dla logów Laravel jeśli nie istnieje
mkdir -p ../data/logs

# Uruchom serwer w tle z logowaniem
nohup php artisan serve --host=adamclay.local --port=8004 >> ../data/logs/laravel_server.log 2>&1 &
server_pid=$!

# Czekaj chwilę na start
sleep 3

# Sprawdź czy proces się uruchomił
if kill -0 $server_pid 2>/dev/null; then
    echo "   ✅ Serwer uruchomiony pomyślnie (PID: $server_pid)"
    echo ""
    echo "🌐 LARAVEL SERWER DOSTĘPNY:"
    echo "   URL: http://adamclay.local:8004"
    echo "   Dashboard: http://adamclay.local:8004/consciousness"
    echo "   API Test: http://adamclay.local:8004/api/hello"
    echo ""
    echo "📊 MONITORING:"
    echo "   Status: ./status_laravel.sh"
    echo "   Logi: tail -f data/logs/laravel_server.log"
    echo "   Stop: ./stop_laravel.sh"
    echo ""
    echo "🎉 Laravel gotowy do pracy!"
else
    echo "   ❌ Błąd uruchamiania serwera"
    echo "   📋 Sprawdź logi: cat data/logs/laravel_server.log"
    exit 1
fi 