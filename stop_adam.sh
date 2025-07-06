#!/bin/bash

# =============================================================================
# Script: stop_adam.sh
# Description: Zatrzymuje wszystkie aktywne procesy Adam Clay Eden
# Author: Assistant
# =============================================================================

echo "🛑 Adam Clay Eden - Skrypt zatrzymywania procesów"
echo "================================================="

# Kolory dla lepszej czytelności
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funkcja do wyświetlania kolorowego tekstu
print_status() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Funkcja do znajdowania procesów Adama
find_adam_processes() {
    # Szukaj specyficznych procesów Adam Clay Eden
    CONSCIOUSNESS_PIDS=$(ps aux | grep "consciousness_core.py" | grep -v grep | awk '{print $2}')
    MAIN_PIDS=$(ps aux | grep "python.*main.py" | grep -v grep | grep -v "Cursor" | awk '{print $2}')
    
    # Szukaj procesów Python związanych z projektem AdamClay (ale nie edytorami)
    EDEN_PIDS=$(ps aux | grep "python" | grep -E "(eden|AdamClay)" | grep -v "Cursor" | grep -v "vscode" | grep -v grep | awk '{print $2}')
    
    # Połącz wszystkie PID i usuń duplikaty oraz puste linie
    ALL_PIDS=$(echo "$CONSCIOUSNESS_PIDS $MAIN_PIDS $EDEN_PIDS" | tr ' ' '\n' | sort -u | grep -E '^[0-9]+$')
    
    echo "$ALL_PIDS"
}

# Funkcja do wyświetlania informacji o procesach
show_processes() {
    local pids="$1"
    
    if [ -z "$pids" ]; then
        print_success "Brak aktywnych procesów Adam Clay Eden"
        return 0
    fi
    
    print_warning "Znalezione procesy Adam Clay Eden:"
    echo
    printf "%-8s %-8s %-8s %s\n" "PID" "CPU%" "MEM%" "COMMAND"
    echo "----------------------------------------------------------------"
    
    for pid in $pids; do
        if kill -0 "$pid" 2>/dev/null; then
            # Kompatybilność z macOS - używamy prostszej składni ps
            ps -p "$pid" -o pid,pcpu,pmem,command | tail -n +2
        fi
    done
    echo
}

# Funkcja do zatrzymywania procesów
stop_processes() {
    local pids="$1"
    local stopped_count=0
    
    if [ -z "$pids" ]; then
        return 0
    fi
    
    print_status "Zatrzymywanie procesów..."
    
    for pid in $pids; do
        if kill -0 "$pid" 2>/dev/null; then
            print_status "Zatrzymywanie procesu PID: $pid"
            
            # Najpierw próbuj delikatnie (SIGTERM)
            if kill "$pid" 2>/dev/null; then
                sleep 2
                
                # Sprawdź czy proces się zatrzymał
                if ! kill -0 "$pid" 2>/dev/null; then
                    print_success "Proces $pid zatrzymany pomyślnie"
                    ((stopped_count++))
                else
                    print_warning "Proces $pid nie odpowiada, użycie SIGKILL..."
                    # Jeśli nie, użyj force kill
                    if kill -9 "$pid" 2>/dev/null; then
                        sleep 1
                        if ! kill -0 "$pid" 2>/dev/null; then
                            print_success "Proces $pid zatrzymany siłą"
                            ((stopped_count++))
                        else
                            print_error "Nie udało się zatrzymać procesu $pid"
                        fi
                    fi
                fi
            else
                print_error "Nie udało się wysłać sygnału do procesu $pid"
            fi
        else
            print_warning "Proces $pid już nie istnieje"
        fi
    done
    
    return $stopped_count
}

# Funkcja do weryfikacji zatrzymania
verify_stopped() {
    print_status "Weryfikacja zatrzymania procesów..."
    sleep 2
    
    local remaining_pids=$(find_adam_processes)
    
    if [ -z "$remaining_pids" ]; then
        print_success "Wszystkie procesy Adam Clay Eden zostały zatrzymane"
        return 0
    else
        print_error "Następujące procesy nadal działają:"
        show_processes "$remaining_pids"
        return 1
    fi
}

# Główna logika skryptu
main() {
    # Sprawdź czy skrypt jest uruchomiony z odpowiednimi uprawnieniami
    if [ "$EUID" -eq 0 ]; then
        print_warning "Skrypt uruchomiony jako root - może zatrzymać procesy innych użytkowników"
    fi
    
    # Znajdź procesy
    print_status "Szukanie aktywnych procesów Adam Clay Eden..."
    ADAM_PIDS=$(find_adam_processes)
    
    # Pokaż znalezione procesy
    show_processes "$ADAM_PIDS"
    
    # Jeśli nie ma procesów, zakończ
    if [ -z "$ADAM_PIDS" ]; then
        echo "🎉 Adam Clay Eden nie jest aktywny"
        exit 0
    fi
    
    # Zapytaj użytkownika o potwierdzenie (jeśli nie ma flagi -f)
    if [ "$1" != "-f" ] && [ "$1" != "--force" ]; then
        echo
        read -p "Czy chcesz zatrzymać te procesy? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_warning "Anulowano zatrzymywanie procesów"
            exit 0
        fi
    fi
    
    # Zatrzymaj procesy
    stop_processes "$ADAM_PIDS"
    stopped_count=$?
    
    # Weryfikuj zatrzymanie
    verify_stopped
    
    if [ $? -eq 0 ]; then
        echo
        print_success "🎉 Adam Clay Eden został pomyślnie zatrzymany"
        print_status "Zatrzymano $stopped_count procesów"
    else
        echo
        print_error "⚠️ Niektóre procesy mogą nadal działać"
        exit 1
    fi
}

# Wyświetl pomoc
show_help() {
    echo "Użycie: $0 [OPCJE]"
    echo
    echo "Opcje:"
    echo "  -f, --force    Zatrzymaj procesy bez pytania o potwierdzenie"
    echo "  -h, --help     Wyświetl tę pomoc"
    echo
    echo "Przykłady:"
    echo "  $0             # Interaktywne zatrzymywanie"
    echo "  $0 -f          # Automatyczne zatrzymywanie"
}

# Parsowanie argumentów
case "$1" in
    -h|--help)
        show_help
        exit 0
        ;;
    -f|--force)
        main -f
        ;;
    "")
        main
        ;;
    *)
        print_error "Nieznana opcja: $1"
        show_help
        exit 1
        ;;
esac 