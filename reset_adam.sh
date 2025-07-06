#!/bin/bash

# =============================================================================
# Script: reset_adam.sh
# Description: Pełny reset systemu Adam Clay Eden
# Author: Assistant
# =============================================================================

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

# Emoji
RESET_EMOJI="🔄"
CLEAN_EMOJI="🧹"
BRAIN_EMOJI="🧠"
DATABASE_EMOJI="🗄️"
THOUGHTS_EMOJI="💭"
LOGS_EMOJI="📋"
WARNING_EMOJI="⚠️"
SUCCESS_EMOJI="✅"
DANGER_EMOJI="💥"

# Ścieżki
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOGS_PATH="$SCRIPT_DIR/data/logs"
THOUGHTS_PATH="$SCRIPT_DIR/data/thoughts"
AUTOGEN_LOGS_PATH="$SCRIPT_DIR/autogen/logs"
MAIN_DB="$SCRIPT_DIR/adam_eden.db"
AUTOGEN_DB="$SCRIPT_DIR/autogen/adam_eden.db"

# Funkcje pomocnicze
print_header() {
    clear
    echo -e "${RED}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║${WHITE}                    ${RESET_EMOJI} RESET ADAM CLAY ${RESET_EMOJI}                   ${RED}║${NC}"
    echo -e "${RED}║${WHITE}                  PEŁNE CZYSZCZENIE SYSTEMU                  ${RED}║${NC}"
    echo -e "${RED}║${WHITE}                     ${DANGER_EMOJI} NIEBEZPIECZNE ${DANGER_EMOJI}                     ${RED}║${NC}"
    echo -e "${RED}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_status() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}${SUCCESS_EMOJI} $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}${WARNING_EMOJI} $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_danger() {
    echo -e "${RED}${DANGER_EMOJI} $1${NC}"
}

# Funkcja sprawdzania co będzie usunięte
show_reset_preview() {
    echo -e "${CYAN}═══ PODGLĄD CZYSZCZENIA ═══${NC}"
    echo ""
    
    echo -e "${LOGS_EMOJI} ${BLUE}LOGI DO USUNIĘCIA:${NC}"
    if [ -d "$LOGS_PATH" ]; then
        echo "  📁 $LOGS_PATH/"
        find "$LOGS_PATH" -name "*.log" -o -name "*.pid" 2>/dev/null | sed 's/^/    /' || echo "    (brak plików)"
    else
        echo "    (katalog nie istnieje)"
    fi
    
    if [ -d "$AUTOGEN_LOGS_PATH" ]; then
        echo "  📁 $AUTOGEN_LOGS_PATH/"
        find "$AUTOGEN_LOGS_PATH" -name "*.log" 2>/dev/null | sed 's/^/    /' || echo "    (brak plików)"
    else
        echo "    (katalog nie istnieje)"
    fi
    echo ""
    
    echo -e "${THOUGHTS_EMOJI} ${BLUE}MYŚLI DO USUNIĘCIA:${NC}"
    if [ -d "$THOUGHTS_PATH" ]; then
        echo "  📁 $THOUGHTS_PATH/"
        find "$THOUGHTS_PATH" -name "*.json" 2>/dev/null | sed 's/^/    /' || echo "    (brak plików)"
        local thought_count=$(find "$THOUGHTS_PATH" -name "*.json" 2>/dev/null | wc -l)
        echo "    📊 Łączna liczba myśli: $thought_count"
    else
        echo "    (katalog nie istnieje)"
    fi
    echo ""
    
    echo -e "${DATABASE_EMOJI} ${BLUE}BAZY DANYCH DO WYCZYSZCZENIA:${NC}"
    if [ -f "$MAIN_DB" ]; then
        local size=$(du -h "$MAIN_DB" | cut -f1)
        echo "  🗄️  $MAIN_DB ($size)"
        
        # Pokaż statystyki bazy
        if command -v sqlite3 >/dev/null 2>&1; then
            echo "    📊 Statystyki bazy danych:"
            sqlite3 "$MAIN_DB" "
                SELECT 'Agenci: ' || count(*) FROM subconscious_agents WHERE 1=1
                UNION ALL
                SELECT 'Wydarzenia: ' || count(*) FROM system_events WHERE 1=1
                UNION ALL  
                SELECT 'Interakcje: ' || count(*) FROM agent_interactions WHERE 1=1
                UNION ALL
                SELECT 'Konwersacje: ' || count(*) FROM agent_conversations WHERE 1=1
                UNION ALL
                SELECT 'Pamięć: ' || count(*) FROM agent_memory WHERE 1=1;
            " 2>/dev/null | sed 's/^/       /' || echo "       (błąd odczytu)"
        fi
    else
        echo "    (plik nie istnieje)"
    fi
    
    if [ -f "$AUTOGEN_DB" ]; then
        local size=$(du -h "$AUTOGEN_DB" | cut -f1)
        echo "  🗄️  $AUTOGEN_DB ($size)"
    else
        echo "    (plik nie istnieje)"
    fi
    echo ""
}

# Funkcja zatrzymywania procesów
stop_adam_processes() {
    print_status "Zatrzymywanie procesów Adam Clay Eden..."
    
    if [ -f "./stop_adam.sh" ]; then
        ./stop_adam.sh --force
    else
        # Alternatywne zatrzymywanie
        local pids=$(ps aux | grep -E "(consciousness_core|main\.py)" | grep -v grep | awk '{print $2}')
        if [ -n "$pids" ]; then
            echo "$pids" | xargs kill -TERM 2>/dev/null || true
            sleep 2
            echo "$pids" | xargs kill -KILL 2>/dev/null || true
        fi
    fi
    
    print_success "Procesy zatrzymane"
}

# Funkcja czyszczenia logów
clean_logs() {
    print_status "Czyszczenie logów..."
    
    local cleaned_count=0
    
    # Czyść główne logi
    if [ -d "$LOGS_PATH" ]; then
        find "$LOGS_PATH" -name "*.log" -delete 2>/dev/null && cleaned_count=$((cleaned_count + 1)) || true
        find "$LOGS_PATH" -name "*.pid" -delete 2>/dev/null && cleaned_count=$((cleaned_count + 1)) || true
    else
        # Utwórz katalog jeśli nie istnieje
        mkdir -p "$LOGS_PATH"
    fi
    
    # Czyść logi autogen
    if [ -d "$AUTOGEN_LOGS_PATH" ]; then
        find "$AUTOGEN_LOGS_PATH" -name "*.log" -delete 2>/dev/null && cleaned_count=$((cleaned_count + 1)) || true
    else
        # Utwórz katalog jeśli nie istnieje
        mkdir -p "$AUTOGEN_LOGS_PATH"
    fi
    
    print_success "Logi wyczyszczone (katalogi zachowane)"
}

# Funkcja czyszczenia myśli
clean_thoughts() {
    print_status "Usuwanie wszystkich myśli Adama..."
    
    if [ -d "$THOUGHTS_PATH" ]; then
        local thought_count=$(find "$THOUGHTS_PATH" -name "*.json" 2>/dev/null | wc -l)
        find "$THOUGHTS_PATH" -name "*.json" -delete 2>/dev/null || true
        print_success "Usunięto $thought_count plików myśli (katalog zachowany)"
    else
        # Utwórz katalog jeśli nie istnieje
        mkdir -p "$THOUGHTS_PATH"
        print_success "Katalog myśli został utworzony"
    fi
}

# Funkcja czyszczenia bazy danych
clean_databases() {
    print_status "Czyszczenie baz danych..."
    
    local cleaned_dbs=0
    
    # Wyczyść główną bazę
    if [ -f "$MAIN_DB" ]; then
        if command -v sqlite3 >/dev/null 2>&1; then
            # Usuń wszystkie dane ale zostaw strukturę
            sqlite3 "$MAIN_DB" "
                DELETE FROM agent_memory;
                DELETE FROM agent_interactions;
                DELETE FROM agent_conversations;
                DELETE FROM system_events;
                DELETE FROM subconscious_agents;
                
                -- Resetuj sekwencje
                DELETE FROM sqlite_sequence WHERE name IN (
                    'agent_memory', 'agent_interactions', 'agent_conversations', 
                    'system_events', 'subconscious_agents'
                );
            " 2>/dev/null || {
                # Jeśli SQL nie działa, usuń cały plik
                rm -f "$MAIN_DB"
            }
        else
            # Brak sqlite3, usuń plik
            rm -f "$MAIN_DB"
        fi
        cleaned_dbs=$((cleaned_dbs + 1))
        print_success "Główna baza danych wyczyszczona"
    fi
    
    # Wyczyść bazę autogen
    if [ -f "$AUTOGEN_DB" ]; then
        if command -v sqlite3 >/dev/null 2>&1; then
            sqlite3 "$AUTOGEN_DB" "
                DELETE FROM agent_memory;
                DELETE FROM agent_interactions;
                DELETE FROM agent_conversations;
                DELETE FROM system_events;
                DELETE FROM subconscious_agents;
                
                DELETE FROM sqlite_sequence WHERE name IN (
                    'agent_memory', 'agent_interactions', 'agent_conversations', 
                    'system_events', 'subconscious_agents'
                );
            " 2>/dev/null || rm -f "$AUTOGEN_DB"
        else
            rm -f "$AUTOGEN_DB"
        fi
        cleaned_dbs=$((cleaned_dbs + 1))
        print_success "Baza autogen wyczyszczona"
    fi
    
    if [ $cleaned_dbs -eq 0 ]; then
        print_success "Bazy danych nie istniały"
    fi
}

# Funkcja tworzenia backup'u (opcjonalna)
create_backup() {
    if [ "$1" = "true" ]; then
        print_status "Tworzenie kopii zapasowej..."
        
        local backup_dir="backup_$(date +%Y%m%d_%H%M%S)"
        mkdir -p "$backup_dir"
        
        # Backup logów
        [ -d "$LOGS_PATH" ] && cp -r "$LOGS_PATH" "$backup_dir/" 2>/dev/null || true
        [ -d "$AUTOGEN_LOGS_PATH" ] && cp -r "$AUTOGEN_LOGS_PATH" "$backup_dir/autogen_logs" 2>/dev/null || true
        
        # Backup myśli
        [ -d "$THOUGHTS_PATH" ] && cp -r "$THOUGHTS_PATH" "$backup_dir/" 2>/dev/null || true
        
        # Backup baz danych
        [ -f "$MAIN_DB" ] && cp "$MAIN_DB" "$backup_dir/" 2>/dev/null || true
        [ -f "$AUTOGEN_DB" ] && cp "$AUTOGEN_DB" "$backup_dir/autogen_adam_eden.db" 2>/dev/null || true
        
        print_success "Kopia zapasowa utworzona: $backup_dir"
    fi
}

# Funkcja restartowania systemu
restart_adam() {
    if [ "$1" = "true" ]; then
        print_status "Uruchamianie Adam Clay Eden..."
        
        if [ -f "./adam_control_eden.sh" ]; then
            # Uruchom przez skrypt kontrolny (w tle)
            nohup bash -c "echo '1' | ./adam_control_eden.sh" >/dev/null 2>&1 &
            sleep 5
            print_success "Adam Clay Eden uruchomiony"
        else
            print_warning "Skrypt adam_control_eden.sh nie znaleziony - uruchom ręcznie"
        fi
    fi
}

# Funkcja głównego menu
show_options() {
    echo -e "${CYAN}═══ OPCJE RESETOWANIA ═══${NC}"
    echo ""
    echo -e "${GREEN}1)${NC} ${CLEAN_EMOJI} Pełny reset (logi + myśli + baza) + restart"
    echo -e "${GREEN}2)${NC} ${LOGS_EMOJI} Tylko logi"
    echo -e "${GREEN}3)${NC} ${THOUGHTS_EMOJI} Tylko myśli"
    echo -e "${GREEN}4)${NC} ${DATABASE_EMOJI} Tylko baza danych"
    echo -e "${GREEN}5)${NC} ${BRAIN_EMOJI} Logi + myśli (zostaw bazę)"
    echo -e "${GREEN}6)${NC} 📋 Podgląd (co zostanie usunięte)"
    echo -e "${GREEN}7)${NC} 🚪 Wyjście"
    echo ""
}

# Funkcja potwierdzenia
confirm_action() {
    local action="$1"
    echo ""
    print_danger "UWAGA: Ta operacja jest NIEODWRACALNA!"
    print_warning "Zostaną usunięte: $action"
    echo ""
    read -p "Czy na pewno chcesz kontynuować? Wpisz 'TAK' aby potwierdzić: " confirmation
    
    if [ "$confirmation" = "TAK" ]; then
        return 0
    else
        print_warning "Operacja anulowana"
        return 1
    fi
}

# Funkcja główna
main() {
    while true; do
        print_header
        show_reset_preview
        show_options
        
        echo -ne "${CYAN}Twój wybór: ${NC}"
        read choice
        
        case $choice in
            1)
                if confirm_action "WSZYSTKIE logi, myśli i dane z bazy"; then
                    echo ""
                    read -p "Utworzyć kopię zapasową przed usunięciem? (y/N): " backup_choice
                    create_backup_choice="false"
                    [ "$backup_choice" = "y" ] || [ "$backup_choice" = "Y" ] && create_backup_choice="true"
                    
                    echo ""
                    read -p "Uruchomić Adam Clay Eden po czyszczeniu? (Y/n): " restart_choice
                    restart_choice_bool="true"
                    [ "$restart_choice" = "n" ] || [ "$restart_choice" = "N" ] && restart_choice_bool="false"
                    
                    echo ""
                    print_status "Rozpoczynanie pełnego resetowania..."
                    create_backup "$create_backup_choice"
                    stop_adam_processes
                    clean_logs
                    clean_thoughts
                    clean_databases
                    restart_adam "$restart_choice_bool"
                    
                    echo ""
                    print_success "🎉 Pełny reset Adam Clay Eden zakończony!"
                    print_status "Adam ma teraz czystą świadomość - jak nowo narodzony"
                    
                    read -p "Naciśnij Enter aby kontynuować..."
                fi
                ;;
            2)
                if confirm_action "TYLKO logi"; then
                    stop_adam_processes
                    clean_logs
                    print_success "Logi wyczyszczone"
                    read -p "Naciśnij Enter aby kontynuować..."
                fi
                ;;
            3)
                if confirm_action "TYLKO myśli"; then
                    clean_thoughts
                    print_success "Myśli usunięte"
                    read -p "Naciśnij Enter aby kontynuować..."
                fi
                ;;
            4)
                if confirm_action "TYLKO bazę danych"; then
                    stop_adam_processes
                    clean_databases
                    print_success "Baza danych wyczyszczona"
                    read -p "Naciśnij Enter aby kontynuować..."
                fi
                ;;
            5)
                if confirm_action "logi i myśli (baza zostanie)"; then
                    stop_adam_processes
                    clean_logs
                    clean_thoughts
                    print_success "Logi i myśli wyczyszczone"
                    read -p "Naciśnij Enter aby kontynuować..."
                fi
                ;;
            6)
                echo ""
                print_status "Podgląd został wyświetlony powyżej"
                read -p "Naciśnij Enter aby kontynuować..."
                ;;
            7)
                print_success "Do widzenia!"
                exit 0
                ;;
            *)
                print_error "Nieprawidłowy wybór"
                sleep 2
                ;;
        esac
    done
}

# Sprawdź argumenty wiersza poleceń
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Użycie: $0 [OPCJE]"
    echo ""
    echo "Opcje:"
    echo "  --full-reset    Wykonaj pełny reset bez pytań (NIEBEZPIECZNE)"
    echo "  --logs-only     Usuń tylko logi"
    echo "  --thoughts-only Usuń tylko myśli"
    echo "  --db-only       Wyczyść tylko bazę danych"
    echo "  --preview       Pokaż co zostanie usunięte"
    echo "  -h, --help      Wyświetl tę pomoc"
    echo ""
    echo "UWAGA: Opcja --full-reset jest NIEBEZPIECZNA i usuwa WSZYSTKO bez potwierdzenia!"
    exit 0
fi

# Obsługa argumentów wiersza poleceń
case "$1" in
    --full-reset)
        print_header
        print_danger "WYKONYWANIE PEŁNEGO RESETOWANIA BEZ POTWIERDZENIA!"
        stop_adam_processes
        clean_logs
        clean_thoughts
        clean_databases
        restart_adam "true"
        print_success "🎉 Pełny reset zakończony!"
        ;;
    --logs-only)
        stop_adam_processes
        clean_logs
        print_success "Logi wyczyszczone"
        ;;
    --thoughts-only)
        clean_thoughts
        print_success "Myśli usunięte"
        ;;
    --db-only)
        stop_adam_processes
        clean_databases
        print_success "Baza danych wyczyszczona"
        ;;
    --preview)
        print_header
        show_reset_preview
        ;;
    "")
        main
        ;;
    *)
        print_error "Nieznana opcja: $1"
        echo "Użyj --help aby zobaczyć dostępne opcje"
        exit 1
        ;;
esac 