#!/bin/bash

echo "📊 ADAM CLAY - STATUS SYSTEMU"
echo "============================="
echo ""

# Sprawdź komponenty
laravel_pid=$(pgrep -f "php artisan serve")
consciousness_pid=$(pgrep -f "python3 main.py")

# Sprawdź ogólny stan systemu
if [[ -n "$laravel_pid" ]] && [[ -n "$consciousness_pid" ]]; then
    system_status="🟢 PEŁNIE AKTYWNY"
elif [[ -n "$laravel_pid" ]] || [[ -n "$consciousness_pid" ]]; then
    system_status="🟡 CZĘŚCIOWO AKTYWNY"
else
    system_status="🔴 ZATRZYMANY"
fi

echo "🎯 STATUS SYSTEMU: $system_status"
echo ""

# Szczegółowy status komponentów
echo "📊 KOMPONENTY SYSTEMU:"
echo "====================="

# Laravel API
if [[ -n "$laravel_pid" ]]; then
    echo "🌐 LARAVEL API: 🟢 AKTYWNY"
    
    process_info=$(ps aux | grep "$laravel_pid" | grep -v grep | head -1)
    if [[ -n "$process_info" ]]; then
        echo "   🔍 PID: $laravel_pid"
        
        # CPU i pamięć
        cpu=$(echo "$process_info" | awk '{print $3}')
        memory=$(echo "$process_info" | awk '{print $4}')
        echo "   🖥️  CPU: ${cpu}%"
        echo "   💾 RAM: ${memory}%"
        
        # Czas działania
        time_info=$(echo "$process_info" | awk '{print $(NF-1)}')
        echo "   ⏰ Uptime: $time_info"
        
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
    
    # Test API
    echo "   🔍 Test API..."
    response=$(curl -s -w "%{http_code}" -o /tmp/status_api_test.json "$url/api/hello" 2>/dev/null)
    http_code="${response: -3}"
    
    if [[ "$http_code" == "200" ]]; then
        echo "   ✅ API odpowiada (HTTP 200)"
    else
        echo "   ❌ API nie odpowiada (HTTP $http_code)"
    fi
    
    rm -f /tmp/status_api_test.json
    
else
    echo "🌐 LARAVEL API: 🔴 ZATRZYMANY"
    echo "   💡 Start: ./start_laravel.sh"
fi

echo ""

# Consciousness
if [[ -n "$consciousness_pid" ]]; then
    echo "🧠 CONSCIOUSNESS: 🟢 AKTYWNY"
    
    process_info=$(ps aux | grep "$consciousness_pid" | grep -v grep | head -1)
    if [[ -n "$process_info" ]]; then
        echo "   🔍 PID: $consciousness_pid"
        
        # CPU i pamięć
        cpu=$(echo "$process_info" | awk '{print $3}')
        memory=$(echo "$process_info" | awk '{print $4}')
        echo "   🖥️  CPU: ${cpu}%"
        echo "   💾 RAM: ${memory}%"
        
        # Czas działania
        time_info=$(echo "$process_info" | awk '{print $(NF-1)}')
        echo "   ⏰ Uptime: $time_info"
    fi
    
    # Test thinking status (jeśli Laravel działa)
    if [[ -n "$laravel_pid" ]]; then
        echo "   🔍 Test thinking status..."
        
        response=$(curl -s -w "%{http_code}" -o /tmp/thinking_status.json "$url/api/consciousness/thinking-status" 2>/dev/null)
        http_code="${response: -3}"
        
        if [[ "$http_code" == "200" ]]; then
            is_thinking=$(cat /tmp/thinking_status.json 2>/dev/null | grep -o '"is_thinking":[^,]*' | cut -d':' -f2)
            session_status=$(cat /tmp/thinking_status.json 2>/dev/null | grep -o '"session_status":"[^"]*"' | cut -d'"' -f4)
            
            if [[ "$is_thinking" == "true" ]]; then
                echo "   🧠 Status: Myśli aktywnie"
            elif [[ "$is_thinking" == "false" ]]; then
                case "$session_status" in
                    "paused") echo "   ⏸️  Status: Wstrzymany przez dashboard" ;;
                    "blocked_by_email") echo "   📧 Status: Zablokowany przez email" ;;
                    "stopped") echo "   🛑 Status: Zatrzymany" ;;
                    "starting") echo "   🚀 Status: Uruchamianie..." ;;
                    *) echo "   ⏸️  Status: Nieaktywny ($session_status)" ;;
                esac
            fi
        else
            echo "   ⚠️  Nie można sprawdzić thinking status"
        fi
        
        rm -f /tmp/thinking_status.json
    fi
    
else
    echo "🧠 CONSCIOUSNESS: 🔴 ZATRZYMANY"
    if [[ -n "$laravel_pid" ]]; then
        echo "   💡 Start: curl -X POST $url/api/consciousness/start"
    else
        echo "   💡 Start: ./start_adam_clay.sh"
    fi
fi

echo ""

# Test bazy danych (jeśli Laravel działa)
if [[ -n "$laravel_pid" ]]; then
    echo "🗄️  BAZA DANYCH:"
    echo "==============="
    
    cd web 2>/dev/null || {
        echo "   ❌ Nie można przejść do katalogu web"
    }
    
    if [[ -d "web" ]]; then
        cd web
        
        db_test=$(php artisan tinker --execute="
        try {
            \$pdo = DB::connection()->getPdo();
            echo 'OK';
        } catch (Exception \$e) {
            echo 'ERROR: ' . \$e->getMessage();
        }
        " 2>/dev/null | tail -n +2)
        
        if [[ "$db_test" == "OK" ]]; then
            echo "   ✅ Połączenie: Aktywne"
            
            # Sprawdź statystyki
            thoughts_count=$(php artisan tinker --execute="
            try {
                \$count = DB::table('thoughts')->count();
                echo \$count;
            } catch (Exception \$e) {
                echo 'ERROR';
            }
            " 2>/dev/null | tail -n +2)
            
            sessions_count=$(php artisan tinker --execute="
            try {
                \$count = DB::table('consciousness_sessions')->count();
                echo \$count;
            } catch (Exception \$e) {
                echo 'ERROR';
            }
            " 2>/dev/null | tail -n +2)
            
            memories_count=$(php artisan tinker --execute="
            try {
                \$count = DB::table('significant_memories')->count();
                echo \$count;
            } catch (Exception \$e) {
                echo 'ERROR';
            }
            " 2>/dev/null | tail -n +2)
            
            if [[ "$thoughts_count" =~ ^[0-9]+$ ]]; then
                echo "   💭 Thoughts: $thoughts_count"
            fi
            
            if [[ "$sessions_count" =~ ^[0-9]+$ ]]; then
                echo "   🧠 Sessions: $sessions_count"
            fi
            
            if [[ "$memories_count" =~ ^[0-9]+$ ]]; then
                echo "   💾 Memories: $memories_count"
            fi
            
        else
            echo "   ❌ Błąd połączenia: $db_test"
        fi
        
        cd - > /dev/null
    fi
    
    echo ""
fi

# Sprawdź logi
echo "📋 LOGI SYSTEMU:"
echo "==============="

# Laravel logs
laravel_log="../data/logs/laravel_server.log"
if [[ -f "$laravel_log" ]]; then
    log_size=$(du -h "$laravel_log" | cut -f1)
    echo "   🌐 Laravel: $laravel_log ($log_size)"
    
    # Ostatni wpis
    last_line=$(tail -1 "$laravel_log" 2>/dev/null)
    if [[ -n "$last_line" ]]; then
        echo "      📰 Ostatni: ${last_line:0:60}..."
    fi
else
    echo "   🌐 Laravel: Brak pliku logu"
fi

# Consciousness logs
consciousness_log="../data/logs/consciousness.log"
if [[ -f "$consciousness_log" ]]; then
    log_size=$(du -h "$consciousness_log" | cut -f1)
    echo "   🧠 Consciousness: $consciousness_log ($log_size)"
    
    # Ostatni wpis
    last_line=$(tail -1 "$consciousness_log" 2>/dev/null)
    if [[ -n "$last_line" ]]; then
        echo "      📰 Ostatni: ${last_line:0:60}..."
    fi
else
    echo "   🧠 Consciousness: Brak pliku logu"
fi

echo ""

# Zarządzanie
echo "🎛️  ZARZĄDZANIE SYSTEMEM:"
echo "========================"

if [[ "$system_status" == "🔴 ZATRZYMANY" ]]; then
    echo "   🚀 Uruchom system: ./start_adam_clay.sh"
    echo "   🧹 Reset systemu: ./reset_adam_clay.sh"
elif [[ "$system_status" == "🟡 CZĘŚCIOWO AKTYWNY" ]]; then
    echo "   🔄 Restart systemu: ./restart_adam_clay.sh"
    echo "   🛑 Zatrzymaj system: ./stop_adam_clay.sh"
    
    if [[ -z "$laravel_pid" ]]; then
        echo "   🌐 Uruchom Laravel: ./start_laravel.sh"
    fi
    
    if [[ -z "$consciousness_pid" ]] && [[ -n "$laravel_pid" ]]; then
        echo "   🧠 Uruchom Consciousness: curl -X POST $url/api/consciousness/start"
    fi
else
    echo "   🔄 Restart systemu: ./restart_adam_clay.sh"
    echo "   🛑 Zatrzymaj system: ./stop_adam_clay.sh"
    echo "   🌐 Dashboard: $url/consciousness"
fi

echo ""

# Test końcowy connectivity
if [[ -n "$laravel_pid" ]]; then
    echo "🔗 TEST KOŃCOWEJ FUNKCJONALNOŚCI:"
    echo "================================="
    
    # API hello
    response=$(curl -s -w "%{http_code}" -o /tmp/final_connectivity.json "$url/api/hello" 2>/dev/null)
    http_code="${response: -3}"
    
    if [[ "$http_code" == "200" ]]; then
        echo "   ✅ API: Dostępne"
    else
        echo "   ❌ API: Niedostępne (HTTP $http_code)"
    fi
    
    # Dashboard
    response=$(curl -s -w "%{http_code}" -o /dev/null "$url/consciousness" 2>/dev/null)
    http_code="${response: -3}"
    
    if [[ "$http_code" == "200" ]]; then
        echo "   ✅ Dashboard: Dostępny"
    else
        echo "   ❌ Dashboard: Niedostępny (HTTP $http_code)"
    fi
    
    rm -f /tmp/final_connectivity.json
    
    echo ""
    echo "🌐 LINKI:"
    echo "   Dashboard: $url/consciousness"
    echo "   API Test: $url/api/hello"
    
fi

echo "" 