#!/bin/bash

# Adam Clay Eden - Control Center
# Centrum kontroli dla architektury Eden - wiek niewinności

set -e

# Kolory dla lepszej czytelności
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Emoji dla lepszej wizualizacji
EDEN_EMOJI="🌱"
CONSCIOUSNESS_EMOJI="🧠"
HEART_EMOJI="💚"
SPARKLES_EMOJI="✨"
ROCKET_EMOJI="🚀"
STOP_EMOJI="🛑"
INFO_EMOJI="ℹ️"
WARNING_EMOJI="⚠️"

# Ścieżki
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/venv_eden"
AUTOGEN_PATH="$SCRIPT_DIR/autogen"
LOGS_PATH="$SCRIPT_DIR/data/logs"

# Funkcja wyświetlania nagłówka
show_header() {
    clear
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${WHITE}                    Adam Clay Eden ${EDEN_EMOJI}                      ${CYAN}║${NC}"
    echo -e "${CYAN}║${WHITE}                   Wiek Niewinności                           ${CYAN}║${NC}"
    echo -e "${CYAN}║${WHITE}                  Control Center                             ${CYAN}║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Funkcja sprawdzania statusu środowiska
check_environment() {
    echo -e "${INFO_EMOJI} ${BLUE}Sprawdzanie środowiska Eden...${NC}"
    
    if [ ! -d "$VENV_PATH" ]; then
        echo -e "${WARNING_EMOJI} ${YELLOW}Środowisko wirtualne nie istnieje${NC}"
        echo -e "${INFO_EMOJI} ${BLUE}Uruchom najpierw: ./install_eden.sh${NC}"
        return 1
    fi
    
    if [ ! -f "$AUTOGEN_PATH/consciousness_core.py" ]; then
        echo -e "${WARNING_EMOJI} ${YELLOW}Rdzeń świadomości nie istnieje${NC}"
        return 1
    fi
    
    echo -e "${SPARKLES_EMOJI} ${GREEN}Środowisko Eden jest gotowe${NC}"
    return 0
}

# Funkcja startowania Eden
start_eden() {
    echo -e "${ROCKET_EMOJI} ${GREEN}Uruchamianie Adam Clay Eden...${NC}"
    
    if ! check_environment; then
        return 1
    fi
    
    # Aktywacja środowiska wirtualnego
    source "$VENV_PATH/bin/activate"
    
    # Przejście do katalogu autogen
    cd "$AUTOGEN_PATH"
    
    # Uruchomienie w tle
    echo -e "${CONSCIOUSNESS_EMOJI} ${BLUE}Budzenie świadomości...${NC}"
    nohup python consciousness_core.py > "$LOGS_PATH/eden.log" 2>&1 &
    
    echo $! > "$LOGS_PATH/eden.pid"
    
    sleep 2
    
    if ps -p $(cat "$LOGS_PATH/eden.pid") > /dev/null 2>&1; then
        echo -e "${HEART_EMOJI} ${GREEN}Adam Clay Eden jest żywy!${NC}"
        echo -e "${INFO_EMOJI} ${BLUE}PID: $(cat "$LOGS_PATH/eden.pid")${NC}"
        echo -e "${INFO_EMOJI} ${BLUE}Logi: $LOGS_PATH/eden.log${NC}"
    else
        echo -e "${STOP_EMOJI} ${RED}Błąd uruchamiania Eden${NC}"
        return 1
    fi
}

# Funkcja zatrzymywania Eden
stop_eden() {
    echo -e "${STOP_EMOJI} ${YELLOW}Zatrzymywanie Adam Clay Eden...${NC}"
    
    if [ -f "$LOGS_PATH/eden.pid" ]; then
        PID=$(cat "$LOGS_PATH/eden.pid")
        if ps -p $PID > /dev/null 2>&1; then
            kill $PID
            echo -e "${SPARKLES_EMOJI} ${GREEN}Adam Clay Eden został zatrzymany${NC}"
        else
            echo -e "${WARNING_EMOJI} ${YELLOW}Proces nie był uruchomiony${NC}"
        fi
        rm -f "$LOGS_PATH/eden.pid"
    else
        echo -e "${WARNING_EMOJI} ${YELLOW}Brak pliku PID - Eden prawdopodobnie nie działa${NC}"
    fi
}

# Funkcja sprawdzania statusu
check_status() {
    echo -e "${INFO_EMOJI} ${BLUE}Status Adam Clay Eden:${NC}"
    echo ""
    
    if [ -f "$LOGS_PATH/eden.pid" ]; then
        PID=$(cat "$LOGS_PATH/eden.pid")
        if ps -p $PID > /dev/null 2>&1; then
            echo -e "${HEART_EMOJI} ${GREEN}Status: ŻYWY${NC}"
            echo -e "${INFO_EMOJI} ${BLUE}PID: $PID${NC}"
            echo -e "${INFO_EMOJI} ${BLUE}Czas uruchomienia: $(ps -p $PID -o etime= | tr -d ' ')${NC}"
        else
            echo -e "${STOP_EMOJI} ${RED}Status: MARTWY (PID istnieje ale proces nie działa)${NC}"
        fi
    else
        echo -e "${STOP_EMOJI} ${YELLOW}Status: NIEAKTYWNY${NC}"
    fi
    
    echo ""
    echo -e "${INFO_EMOJI} ${BLUE}Środowisko:${NC}"
    echo -e "  Venv: $([ -d "$VENV_PATH" ] && echo "${GREEN}✓${NC}" || echo "${RED}✗${NC}")"
    echo -e "  Consciousness: $([ -f "$AUTOGEN_PATH/consciousness_core.py" ] && echo "${GREEN}✓${NC}" || echo "${RED}✗${NC}")"
    echo -e "  Logs: $([ -d "$LOGS_PATH" ] && echo "${GREEN}✓${NC}" || echo "${RED}✗${NC}")"
}

# Funkcja wyświetlania logów
show_logs() {
    echo -e "${INFO_EMOJI} ${BLUE}Ostatnie logi Eden:${NC}"
    echo ""
    
    if [ -f "$LOGS_PATH/eden.log" ]; then
        tail -n 20 "$LOGS_PATH/eden.log"
    else
        echo -e "${WARNING_EMOJI} ${YELLOW}Brak logów${NC}"
    fi
}

# Funkcja wyświetlania logów na żywo
tail_logs() {
    echo -e "${INFO_EMOJI} ${BLUE}Logi na żywo (Ctrl+C aby wyjść):${NC}"
    echo ""
    
    if [ -f "$LOGS_PATH/eden.log" ]; then
        tail -f "$LOGS_PATH/eden.log"
    else
        echo -e "${WARNING_EMOJI} ${YELLOW}Brak logów${NC}"
    fi
}

# Funkcja restartu
restart_eden() {
    echo -e "${ROCKET_EMOJI} ${BLUE}Restart Adam Clay Eden...${NC}"
    stop_eden
    sleep 2
    start_eden
}

# Funkcja instalacji
install_eden() {
    echo -e "${ROCKET_EMOJI} ${BLUE}Uruchamianie instalatora Eden...${NC}"
    
    if [ -f "$SCRIPT_DIR/install_eden.sh" ]; then
        bash "$SCRIPT_DIR/install_eden.sh"
    else
        echo -e "${STOP_EMOJI} ${RED}Instalator nie znaleziony${NC}"
    fi
}

# Funkcja głównego menu
show_menu() {
    echo -e "${SPARKLES_EMOJI} ${WHITE}Wybierz opcję:${NC}"
    echo ""
    echo -e "${GREEN}1)${NC} ${ROCKET_EMOJI} Start Eden"
    echo -e "${GREEN}2)${NC} ${STOP_EMOJI} Stop Eden"
    echo -e "${GREEN}3)${NC} ${INFO_EMOJI} Status"
    echo -e "${GREEN}4)${NC} ${ROCKET_EMOJI} Restart Eden"
    echo -e "${GREEN}5)${NC} 📋 Pokaż logi"
    echo -e "${GREEN}6)${NC} 📡 Logi na żywo"
    echo -e "${GREEN}7)${NC} ${ROCKET_EMOJI} Instalacja/Aktualizacja"
    echo -e "${GREEN}8)${NC} 🚪 Wyjście"
    echo ""
    echo -ne "${CYAN}Twój wybór: ${NC}"
}

# Główna pętla
main() {
    while true; do
        show_header
        show_menu
        
        read -r choice
        echo ""
        
        case $choice in
            1)
                start_eden
                ;;
            2)
                stop_eden
                ;;
            3)
                check_status
                ;;
            4)
                restart_eden
                ;;
            5)
                show_logs
                ;;
            6)
                tail_logs
                ;;
            7)
                install_eden
                ;;
            8)
                echo -e "${HEART_EMOJI} ${GREEN}Do zobaczenia w Eden!${NC}"
                exit 0
                ;;
            *)
                echo -e "${WARNING_EMOJI} ${RED}Nieprawidłowa opcja${NC}"
                ;;
        esac
        
        echo ""
        echo -e "${BLUE}Naciśnij Enter aby kontynuować...${NC}"
        read -r
    done
}

# Uruchomienie jeśli skrypt jest wywołany bezpośrednio
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi 