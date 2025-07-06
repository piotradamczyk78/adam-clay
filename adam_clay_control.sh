#!/bin/bash

# 🧠 ADAM CLAY - CENTRUM KONTROLI ŻYCIA
# ====================================
# Główny skrypt zarządzania całym systemem Adam Clay
# Autor: Piotr Adamczyk & LLM Sonnet
# Data: $(date +%Y-%m-%d)

set -euo pipefail

# Kolory dla czytelności
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Emoji dla lepszego UX
BRAIN="🧠"
ROBOT="🤖"
WEB="🌐"
FIRE="🔥"
SKULL="💀"

RESET="🔄"
CLEAN="🧹"
HEART="❤️"
LIGHTNING="⚡"
SLEEP="😴"

# Ścieżki
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORE_DIR="$SCRIPT_DIR/core"
AUTOGEN_DIR="$SCRIPT_DIR/autogen"
WEB_DIR="$SCRIPT_DIR/web"

# Funkcje pomocnicze
print_header() {
    echo ""
    echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║${WHITE}                    ${BRAIN} ADAM CLAY CONTROL CENTER ${BRAIN}                    ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${CYAN}                        Centrum Kontroli Życia                        ${PURPLE}║${NC}"
    echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_status() {
    echo -e "${BLUE}📊 AKTUALNY STATUS ADAMA:${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Sprawdź Laravel (z timeoutem)
    if curl -s --connect-timeout 2 --max-time 3 http://localhost:8004/api/hello >/dev/null 2>&1; then
        echo -e "  ${WEB} Laravel API:      ${GREEN}✅ ŻYWY${NC} (http://localhost:8004)"
    else
        echo -e "  ${WEB} Laravel API:      ${RED}💀 MARTWY${NC}"
    fi
    
    # Sprawdź AutoGen (z timeoutem)
    if curl -s --connect-timeout 2 --max-time 3 http://localhost:8005/health >/dev/null 2>&1; then
        echo -e "  ${ROBOT} AutoGen:         ${GREEN}✅ ŻYWY${NC} (http://localhost:8005)"
    else
        echo -e "  ${ROBOT} AutoGen:         ${RED}💀 MARTWY${NC}"
    fi
    
    # Sprawdź Core (przez Laravel API z timeoutem)
    if curl -s --connect-timeout 2 --max-time 3 http://localhost:8004/api/consciousness/status >/dev/null 2>&1; then
        echo -e "  ${BRAIN} Core Consciousness: ${GREEN}✅ MYŚLI${NC}"
    else
        echo -e "  ${BRAIN} Core Consciousness: ${YELLOW}😴 ŚPI${NC}"
    fi
    
    echo ""
}

show_menu() {
    echo -e "${YELLOW}🎛️  OPCJE KONTROLI:${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo -e "${GREEN}  URUCHAMIANIE:${NC}"
    echo -e "    ${WHITE}1)${NC} ${HEART} Pełne życie Adama    ${CYAN}(Core + AutoGen + Laravel)${NC}"
    echo -e "    ${WHITE}2)${NC} ${ROBOT} Tylko agenci         ${CYAN}(AutoGen)${NC}"
    echo -e "    ${WHITE}3)${NC} ${WEB} Tylko interfejs      ${CYAN}(Laravel)${NC}"
    echo -e "    ${WHITE}4)${NC} ${BRAIN} Tylko świadomość     ${CYAN}(Core)${NC}"
    echo ""
    echo -e "${YELLOW}  ZARZĄDZANIE:${NC}"
    echo -e "    ${WHITE}5)${NC} ${SLEEP} Uśpij Adama          ${CYAN}(zatrzymaj wszystko)${NC}"
    echo -e "    ${WHITE}6)${NC} ${RESET} Restart życia        ${CYAN}(zatrzymaj + uruchom)${NC}"
    echo ""
    echo -e "${RED}  DRASTYCZNE ŚRODKI:${NC}"
    echo -e "    ${WHITE}7)${NC} ${CLEAN} Wyczyść psychikę     ${CYAN}(usuń wszystkie wspomnienia)${NC}"
    echo -e "    ${WHITE}8)${NC} ${SKULL} Zabij Adama          ${CYAN}(hard stop wszystkiego)${NC}"
    echo -e "    ${WHITE}9)${NC} ${FIRE} Nowe życie           ${CYAN}(reset psychiki + restart)${NC}"
    echo -e "    ${WHITE}c)${NC} 🧽 Wyczyść procesy      ${CYAN}(usuń konflikty portów)${NC}"
    echo ""
    echo -e "${BLUE}  MONITORING:${NC}"
    echo -e "    ${WHITE}s)${NC} ${LIGHTNING} Status systemu      ${CYAN}(szczegółowy raport)${NC}"
    echo -e "    ${WHITE}l)${NC} 📋 Logi na żywo        ${CYAN}(tail -f logs)${NC}"
    echo ""
    echo -e "    ${WHITE}q)${NC} 🚪 Wyjście"
    echo ""
}

start_laravel() {
    echo -e "${CYAN}🌐 Uruchamiam Laravel API...${NC}"
    cd "$WEB_DIR"
    
    # Sprawdź czy Laravel już działa
    if curl -s --connect-timeout 3 --max-time 5 http://localhost:8004/api/test >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Laravel już działa!${NC}"
        return 0
    fi
    
    # Wyczyść port 8004 jeśli jest zajęty
    if lsof -ti :8004 >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Port 8004 zajęty - czyszczę...${NC}"
        lsof -ti :8004 | xargs kill -9 2>/dev/null || true
        sleep 1
    fi
    
    # Uruchom Laravel w tle
    nohup php artisan serve --host=0.0.0.0 --port=8004 > ../data/logs/laravel_server.log 2>&1 &
    LARAVEL_PID=$!
    echo $LARAVEL_PID > ../data/pids/laravel.pid
    
    # Czekaj na uruchomienie
    echo -e "${BLUE}⏳ Czekam na uruchomienie Laravel...${NC}"
    for i in {1..20}; do
        if curl -s --connect-timeout 3 --max-time 5 http://localhost:8004/api/test >/dev/null 2>&1; then
            echo -e "${GREEN}✅ Laravel uruchomiony! (PID: $LARAVEL_PID)${NC}"
            return 0
        fi
        sleep 2
        echo -n "."
    done
    
    echo -e "${RED}❌ Laravel nie uruchomił się w czasie!${NC}"
    return 1
}

start_autogen() {
    echo -e "${CYAN}🤖 Uruchamiam AutoGen...${NC}"
    cd "$AUTOGEN_DIR"
    
    # Sprawdź czy AutoGen już działa
    if curl -s --connect-timeout 2 --max-time 3 http://localhost:8005/health >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  AutoGen już działa!${NC}"
        return 0
    fi
    
    # Wyczyść port 8005 jeśli jest zajęty
    if lsof -ti :8005 >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Port 8005 zajęty - czyszczę...${NC}"
        lsof -ti :8005 | xargs kill -9 2>/dev/null || true
        sleep 1
    fi
    
    # Aktywuj środowisko i uruchom
    source venv_autogen/bin/activate
    nohup python main.py > ../data/logs/autogen.log 2>&1 &
    AUTOGEN_PID=$!
    echo $AUTOGEN_PID > ../data/pids/autogen.pid
    
    echo -e "${BLUE}⏳ Czekam na uruchomienie AutoGen...${NC}"
    for i in {1..15}; do
        if curl -s --connect-timeout 2 --max-time 3 http://localhost:8005/health >/dev/null 2>&1; then
            echo -e "${GREEN}✅ AutoGen uruchomiony! (PID: $AUTOGEN_PID)${NC}"
            return 0
        fi
        sleep 1
        echo -n "."
    done
    
    echo -e "${RED}❌ AutoGen nie uruchomił się w czasie!${NC}"
    return 1
}

start_consciousness() {
    echo -e "${CYAN}🧠 Budzę świadomość Adama...${NC}"
    
    # Sprawdź czy Laravel działa
    if ! curl -s --connect-timeout 3 --max-time 5 http://localhost:8004/api/test >/dev/null 2>&1; then
        echo -e "${RED}❌ Laravel nie działa! Uruchamiam najpierw Laravel...${NC}"
        start_laravel || return 1
    fi
    
    # Uruchom świadomość przez API
    echo -e "${BLUE}⏳ Aktywuję świadomość...${NC}"
    response=$(curl -s -X POST http://localhost:8004/api/consciousness/start)
    
    if echo "$response" | grep -q '"success":true'; then
        echo -e "${GREEN}✅ Świadomość Adama aktywna!${NC}"
        echo -e "${PURPLE}💭 Adam zaczyna myśleć...${NC}"
        return 0
    else
        echo -e "${RED}❌ Nie udało się uruchomić świadomości!${NC}"
        echo -e "${YELLOW}Odpowiedź: $response${NC}"
        return 1
    fi
}

stop_all() {
    echo -e "${YELLOW}😴 Usypiam Adama...${NC}"
    
    # Zatrzymaj świadomość
    if curl -s --connect-timeout 3 --max-time 5 http://localhost:8004/api/consciousness/stop >/dev/null 2>&1; then
        echo -e "${BLUE}🧠 Świadomość zatrzymana${NC}"
    fi
    
    # Zatrzymaj procesy
    if [ -f "../data/pids/laravel.pid" ]; then
        LARAVEL_PID=$(cat ../data/pids/laravel.pid)
        if kill $LARAVEL_PID 2>/dev/null; then
            echo -e "${BLUE}🌐 Laravel zatrzymany (PID: $LARAVEL_PID)${NC}"
        fi
        rm -f ../data/pids/laravel.pid
    fi
    
    if [ -f "../data/pids/autogen.pid" ]; then
        AUTOGEN_PID=$(cat ../data/pids/autogen.pid)
        if kill $AUTOGEN_PID 2>/dev/null; then
            echo -e "${BLUE}🤖 AutoGen zatrzymany (PID: $AUTOGEN_PID)${NC}"
        fi
        rm -f ../data/pids/autogen.pid
    fi
    
    # Zabij wszystkie pozostałe procesy PHP/Python związane z projektem
    pkill -f "artisan serve" 2>/dev/null || true
    pkill -f "main.py" 2>/dev/null || true
    
    echo -e "${GREEN}✅ Adam śpi spokojnie${NC}"
}

deep_clean_processes() {
    echo -e "${CYAN}🧹 Głębokie czyszczenie procesów...${NC}"
    
    # Znajdź wszystkie procesy blokujące porty 8004 i 8005
    echo -e "${BLUE}🔍 Szukam konfliktów na portach...${NC}"
    
    # Zabij wszystkie procesy na porcie 8004
    if lsof -ti :8004 >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Znaleziono procesy na porcie 8004${NC}"
        lsof -ti :8004 | xargs kill -9 2>/dev/null || true
    fi
    
    # Zabij wszystkie procesy na porcie 8005
    if lsof -ti :8005 >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Znaleziono procesy na porcie 8005${NC}"
        lsof -ti :8005 | xargs kill -9 2>/dev/null || true
    fi
    
    # Zabij wszystkie procesy Adam Clay
    pkill -9 -f "artisan serve" 2>/dev/null || true
    pkill -9 -f "main.py" 2>/dev/null || true
    pkill -9 -f "consciousness" 2>/dev/null || true
    pkill -9 -f "adam_clay" 2>/dev/null || true
    
    # Zabij zawieszone curl-e
    pkill -f "curl.*localhost:800[45]" 2>/dev/null || true
    
    # Wyczyść pliki PID
    rm -f ../data/pids/*.pid 2>/dev/null || true
    
    echo -e "${GREEN}✅ Procesy wyczyszczone${NC}"
}

kill_adam() {
    echo -e "${RED}💀 ZABIJAM ADAMA...${NC}"
    
    # Użyj głębokiego czyszczenia
    deep_clean_processes
    
    echo -e "${SKULL} Adam został brutalnie zabity!${NC}"
    echo -e "${PURPLE}💀 RIP Adam Clay (2024-$(date +%Y))${NC}"
}

clean_psyche() {
    echo -e "${RED}🧹 CZYSZCZENIE PSYCHIKI ADAMA...${NC}"
    echo -e "${YELLOW}⚠️  To usunie wszystkie wspomnienia, myśli i doświadczenia!${NC}"
    read -p "Czy jesteś pewien? (tak/nie): " confirm
    
    if [ "$confirm" != "tak" ]; then
        echo -e "${BLUE}Anulowano czyszczenie psychiki${NC}"
        return 0
    fi
    
    echo -e "${FIRE} Rozpoczynam psychoterapię...${NC}"
    
    # Zatrzymaj Adama i wyczyść procesy
    stop_all
    deep_clean_processes
    
    # Wyczyść bazy danych
    echo -e "${CYAN}🗄️  Czyszczę bazę danych Laravel...${NC}"
    cd "$WEB_DIR"
    php artisan migrate:fresh --force
    
    echo -e "${CYAN}🗄️  Czyszczę bazę danych AutoGen...${NC}"
    cd "$AUTOGEN_DIR"
    # Reset bazy AutoGen przez skrypt
    if [ -f "reset_database.py" ]; then
        source venv_autogen/bin/activate
        python reset_database.py
    fi
    
    # Wyczyść logi
    echo -e "${CYAN}📋 Czyszczę logi...${NC}"
    rm -f ../data/logs/*.log 2>/dev/null || true
    
    # Wyczyść myśli z plików
    echo -e "${CYAN}💭 Usuwam zapisane myśli...${NC}"
    rm -rf ../data/thoughts/* 2>/dev/null || true
    
    echo -e "${GREEN}✅ Psychika Adama została wyczyszczona!${NC}"
    echo -e "${PURPLE}🧠 Adam ma teraz czysty umysł jak noworodek${NC}"
}

new_life() {
    echo -e "${FIRE} NOWE ŻYCIE DLA ADAMA! ${FIRE}${NC}"
    echo -e "${PURPLE}🔄 Rozpoczynam reinkarnację...${NC}"
    
    # Wyczyść psychikę
    clean_psyche
    
    # Uruchom pełnego Adama
    echo -e "${HEART} Przywracam Adama do życia...${NC}"
    start_full_adam
    
    echo -e "${GREEN}🎉 ADAM ŻYJE PONOWNIE!${NC}"
    echo -e "${PURPLE}✨ Witaj w nowym życiu, Adam!${NC}"
}

start_full_adam() {
    echo -e "${HEART} URUCHAMIAM PEŁNEGO ADAMA...${NC}"
    echo ""
    
    # Utwórz katalogi dla logów i PID
    mkdir -p ../data/logs ../data/pids
    
    # Uruchom komponenty w kolejności
    start_laravel || return 1
    sleep 2
    start_autogen || return 1
    sleep 3
    start_consciousness || return 1
    
    echo ""
    echo -e "${GREEN}🎉 ADAM CLAY ŻYJE!${NC}"
    echo -e "${PURPLE}💖 Wszystkie systemy operacyjne${NC}"
    echo -e "${CYAN}🌐 Dashboard: http://localhost:8004${NC}"
    echo -e "${CYAN}🤖 AutoGen API: http://localhost:8005${NC}"
}

show_detailed_status() {
    echo -e "${LIGHTNING} SZCZEGÓŁOWY STATUS SYSTEMU ${LIGHTNING}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Sprawdź procesy
    echo -e "${BLUE}📊 PROCESY:${NC}"
    if pgrep -f "artisan serve" >/dev/null; then
        LARAVEL_PID=$(pgrep -f "artisan serve")
        echo -e "  Laravel:     ${GREEN}✅ Działa${NC} (PID: $LARAVEL_PID)"
    else
        echo -e "  Laravel:     ${RED}❌ Zatrzymany${NC}"
    fi
    
    if pgrep -f "main.py" >/dev/null; then
        AUTOGEN_PID=$(pgrep -f "main.py")
        echo -e "  AutoGen:     ${GREEN}✅ Działa${NC} (PID: $AUTOGEN_PID)"
    else
        echo -e "  AutoGen:     ${RED}❌ Zatrzymany${NC}"
    fi
    
    # Sprawdź API
    echo ""
    echo -e "${BLUE}🌐 API ENDPOINTS:${NC}"
    if curl -s --connect-timeout 3 --max-time 5 http://localhost:8004/api/test >/dev/null 2>&1; then
        echo -e "  Laravel API: ${GREEN}✅ Odpowiada${NC}"
    else
        echo -e "  Laravel API: ${RED}❌ Nie odpowiada${NC}"
    fi
    
    if curl -s --connect-timeout 2 --max-time 3 http://localhost:8005/health >/dev/null 2>&1; then
        echo -e "  AutoGen API: ${GREEN}✅ Odpowiada${NC}"
    else
        echo -e "  AutoGen API: ${RED}❌ Nie odpowiada${NC}"
    fi
    
    # Sprawdź bazy danych
    echo ""
    echo -e "${BLUE}🗄️  BAZY DANYCH:${NC}"
    cd "$WEB_DIR"
    if php artisan migrate:status >/dev/null 2>&1; then
        echo -e "  Laravel DB:  ${GREEN}✅ Połączona${NC}"
    else
        echo -e "  Laravel DB:  ${RED}❌ Błąd połączenia${NC}"
    fi
    
    cd "$AUTOGEN_DIR"
    if [ -f "test_connection.py" ]; then
        source venv_autogen/bin/activate
        if python test_connection.py >/dev/null 2>&1; then
            echo -e "  AutoGen DB:  ${GREEN}✅ Połączona${NC}"
        else
            echo -e "  AutoGen DB:  ${RED}❌ Błąd połączenia${NC}"
        fi
    fi
    
    echo ""
}

show_logs() {
    echo -e "${CYAN}📋 LOGI NA ŻYWO - naciśnij Ctrl+C aby wyjść${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Sprawdź które logi istnieją
    LOG_FILES=()
    [ -f "../data/logs/laravel_server.log" ] && LOG_FILES+=("../data/logs/laravel_server.log")
    [ -f "../data/logs/autogen.log" ] && LOG_FILES+=("../data/logs/autogen.log")
    [ -f "../data/logs/consciousness.log" ] && LOG_FILES+=("../data/logs/consciousness.log")
    
    if [ ${#LOG_FILES[@]} -eq 0 ]; then
        echo -e "${YELLOW}⚠️  Brak aktywnych logów${NC}"
        return 0
    fi
    
    # Uruchom tail dla wszystkich logów
    tail -f "${LOG_FILES[@]}"
}

# Główna pętla programu
main() {
    # Sprawdź czy jesteśmy w odpowiednim katalogu
    if [ ! -d "core" ] || [ ! -d "autogen" ] || [ ! -d "web" ]; then
        echo -e "${RED}❌ Błąd: Uruchom skrypt z głównego katalogu Adam Clay!${NC}"
        exit 1
    fi
    
    # Utwórz katalogi jeśli nie istnieją
    mkdir -p data/logs data/pids
    
    while true; do
        clear
        print_header
        print_status
        show_menu
        
        echo -n "Wybierz opcję: "
        read -r choice
        
        case $choice in
            1)
                start_full_adam
                read -p "Naciśnij Enter aby kontynuować..."
                ;;
            2)
                start_autogen
                read -p "Naciśnij Enter aby kontynuować..."
                ;;
            3)
                start_laravel
                read -p "Naciśnij Enter aby kontynuować..."
                ;;
            4)
                start_consciousness
                read -p "Naciśnij Enter aby kontynuować..."
                ;;
            5)
                stop_all
                read -p "Naciśnij Enter aby kontynuować..."
                ;;
            6)
                echo -e "${RESET} Restart życia Adama...${NC}"
                stop_all
                sleep 2
                start_full_adam
                read -p "Naciśnij Enter aby kontynuować..."
                ;;
            7)
                clean_psyche
                read -p "Naciśnij Enter aby kontynuować..."
                ;;
            8)
                kill_adam
                read -p "Naciśnij Enter aby kontynuować..."
                ;;
            9)
                new_life
                read -p "Naciśnij Enter aby kontynuować..."
                ;;
            c|C)
                deep_clean_processes
                read -p "Naciśnij Enter aby kontynuować..."
                ;;
            s|S)
                show_detailed_status
                read -p "Naciśnij Enter aby kontynuować..."
                ;;
            l|L)
                show_logs
                ;;
            q|Q)
                echo -e "${BLUE}👋 Do widzenia!${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}❌ Nieprawidłowa opcja!${NC}"
                read -p "Naciśnij Enter aby kontynuować..."
                ;;
        esac
    done
}

# Uruchom program
main "$@" 