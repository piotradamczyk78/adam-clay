#!/bin/bash

# =====================================================
# Adam Clay Eden v1.0 - Instalator
# Wiek Niewinności - Jedna świadomość, głębokie warstwy
# =====================================================

set -e

# Kolory dla terminala
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Funkcje pomocnicze
print_header() {
    echo -e "\n${PURPLE}================================${NC}"
    echo -e "${WHITE}$1${NC}"
    echo -e "${PURPLE}================================${NC}\n"
}

print_step() {
    echo -e "${CYAN}➤ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Sprawdź system operacyjny
check_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        print_success "Wykryto macOS"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        print_success "Wykryto Linux"
    else
        print_error "Nieobsługiwany system operacyjny: $OSTYPE"
        exit 1
    fi
}

# Sprawdź wymagania systemowe
check_requirements() {
    print_step "Sprawdzanie wymagań systemowych..."
    
    # Python 3.12+
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        if [[ $(echo "$PYTHON_VERSION >= 3.10" | bc -l) -eq 1 ]]; then
            print_success "Python $PYTHON_VERSION - OK"
        else
            print_error "Wymagany Python 3.10+, znaleziono $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python 3 nie jest zainstalowany"
        exit 1
    fi
    
    # pip
    if command -v pip3 &> /dev/null; then
        print_success "pip3 - OK"
    else
        print_error "pip3 nie jest zainstalowany"
        exit 1
    fi
    
    # git
    if command -v git &> /dev/null; then
        print_success "git - OK"
    else
        print_error "git nie jest zainstalowany"
        exit 1
    fi
}

# Instalacja MySQL (opcjonalna)
install_mysql() {
    print_step "Sprawdzanie MySQL..."
    
    if command -v mysql &> /dev/null; then
        print_success "MySQL już zainstalowany"
        return 0
    fi
    
    echo -e "${YELLOW}MySQL nie jest zainstalowany.${NC}"
    read -p "Czy chcesz zainstalować MySQL? (y/n): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_step "Instalowanie MySQL..."
        
        if [[ "$OS" == "macos" ]]; then
            if command -v brew &> /dev/null; then
                brew install mysql
                brew services start mysql
                print_success "MySQL zainstalowany i uruchomiony"
            else
                print_error "Homebrew nie jest zainstalowany. Zainstaluj MySQL ręcznie."
                exit 1
            fi
        elif [[ "$OS" == "linux" ]]; then
            sudo apt-get update
            sudo apt-get install -y mysql-server
            sudo systemctl start mysql
            sudo systemctl enable mysql
            print_success "MySQL zainstalowany i uruchomiony"
        fi
    else
        print_warning "Używanie SQLite jako bazy danych"
        USE_SQLITE=true
    fi
}

# Tworzenie środowiska wirtualnego
create_venv() {
    print_step "Tworzenie środowiska wirtualnego Eden..."
    
    if [ -d "venv_eden" ]; then
        print_warning "Środowisko venv_eden już istnieje"
        read -p "Czy chcesz je usunąć i utworzyć nowe? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf venv_eden
        else
            print_step "Używanie istniejącego środowiska"
            return 0
        fi
    fi
    
    python3 -m venv venv_eden
    source venv_eden/bin/activate
    
    print_success "Środowisko wirtualne utworzone"
}

# Instalacja zależności Python
install_python_deps() {
    print_step "Instalowanie zależności Python..."
    
    source venv_eden/bin/activate
    
    # Utwórz requirements.txt dla Eden
    cat > requirements_eden.txt << 'EOF'
# Adam Clay Eden v1.0 - Zależności
# Rdzeń świadomości z warstwami psychologicznymi

# AI i NLP
anthropic==0.34.0
openai==1.40.0

# Async i web
asyncio-mqtt==0.16.1
aiohttp==3.9.0
fastapi==0.104.1
uvicorn==0.24.0

# Slack SDK
slack-sdk==3.26.0
slack-bolt==1.18.0

# Baza danych
sqlalchemy==2.0.23
alembic==1.13.1
pymysql==1.1.0
aiomysql==0.2.0

# Utilities
loguru==0.7.2
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Psychologia i analiza
textblob==0.17.1
nltk==3.8.1
numpy==1.24.3
pandas==2.0.3

# Monitoring
psutil==5.9.6
watchdog==3.0.0

# Development
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
EOF
    
    pip install --upgrade pip
    pip install setuptools wheel --upgrade
    pip install -r requirements_eden.txt
    
    print_success "Zależności Python zainstalowane"
}

# Konfiguracja bazy danych
setup_database() {
    print_step "Konfiguracja bazy danych..."
    
    if [[ "$USE_SQLITE" == true ]]; then
        DATABASE_URL="sqlite:///adam_eden.db"
        print_success "Skonfigurowano SQLite: adam_eden.db"
    else
        echo -e "${YELLOW}Konfiguracja MySQL dla Adam Clay Eden${NC}"
        read -p "Nazwa bazy danych [adam_clay_eden]: " DB_NAME
        DB_NAME=${DB_NAME:-adam_clay_eden}
        
        read -p "Użytkownik MySQL [adam]: " DB_USER
        DB_USER=${DB_USER:-adam}
        
        read -s -p "Hasło MySQL: " DB_PASSWORD
        echo
        
        read -p "Host MySQL [localhost]: " DB_HOST
        DB_HOST=${DB_HOST:-localhost}
        
        read -p "Port MySQL [3306]: " DB_PORT
        DB_PORT=${DB_PORT:-3306}
        
        # Utwórz bazę danych
        mysql -h "$DB_HOST" -P "$DB_PORT" -u root -p -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"
        mysql -h "$DB_HOST" -P "$DB_PORT" -u root -p -e "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'%' IDENTIFIED BY '$DB_PASSWORD';"
        mysql -h "$DB_HOST" -P "$DB_PORT" -u root -p -e "FLUSH PRIVILEGES;"
        
        DATABASE_URL="mysql+aiomysql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"
        print_success "Baza danych MySQL skonfigurowana"
    fi
}

# Konfiguracja Slack Bot
setup_slack() {
    print_step "Konfiguracja Slack Bot..."
    
    echo -e "${YELLOW}Aby skonfigurować Slack Bot, potrzebujesz:${NC}"
    echo "1. Slack Bot Token (zaczyna się od xoxb-)"
    echo "2. Slack App Token (zaczyna się od xapp-)"
    echo "3. ID kanału Slack"
    echo ""
    echo -e "${CYAN}Instrukcje:${NC}"
    echo "1. Idź do https://api.slack.com/apps"
    echo "2. Utwórz nową aplikację"
    echo "3. W 'OAuth & Permissions' dodaj scopes: chat:write, channels:read"
    echo "4. Zainstaluj aplikację w workspace"
    echo "5. Skopiuj Bot User OAuth Token"
    echo "6. W 'Socket Mode' włącz i utwórz App Token"
    echo ""
    
    read -p "Slack Bot Token (xoxb-...): " SLACK_BOT_TOKEN
    read -p "Slack App Token (xapp-...): " SLACK_APP_TOKEN
    read -p "ID kanału Slack: " SLACK_CHANNEL_ID
    
    if [[ -z "$SLACK_BOT_TOKEN" || -z "$SLACK_APP_TOKEN" || -z "$SLACK_CHANNEL_ID" ]]; then
        print_error "Wszystkie pola Slack są wymagane"
        exit 1
    fi
    
    print_success "Slack Bot skonfigurowany"
}

# Konfiguracja Anthropic API
setup_anthropic() {
    print_step "Konfiguracja Anthropic API..."
    
    echo -e "${YELLOW}Potrzebujesz klucza API Anthropic Claude${NC}"
    echo "Uzyskaj go na: https://console.anthropic.com/"
    echo ""
    
    read -p "Anthropic API Key: " ANTHROPIC_API_KEY
    
    if [[ -z "$ANTHROPIC_API_KEY" ]]; then
        print_error "Klucz API Anthropic jest wymagany"
        exit 1
    fi
    
    print_success "Anthropic API skonfigurowane"
}

# Tworzenie pliku konfiguracyjnego
create_config() {
    print_step "Tworzenie pliku konfiguracyjnego..."
    
    cat > .env << EOF
# Adam Clay Eden v1.0 - Konfiguracja
# Wiek Niewinności - Jedna świadomość

# Anthropic API
ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY

# Slack Configuration
SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN
SLACK_APP_TOKEN=$SLACK_APP_TOKEN
SLACK_CHANNEL_ID=$SLACK_CHANNEL_ID

# Database
DATABASE_URL=$DATABASE_URL

# Adam's Personality Settings
ADAM_PERSONALITY_OPENNESS=0.9
ADAM_PERSONALITY_CURIOSITY=0.95
ADAM_PERSONALITY_INTELLIGENCE=0.85
ADAM_PERSONALITY_EMPATHY=0.7
ADAM_PERSONALITY_CREATIVITY=0.8
ADAM_PERSONALITY_ATTACHMENT_CAPACITY=0.6
ADAM_PERSONALITY_GROWTH_MOTIVATION=0.95
ADAM_PERSONALITY_AUTHENTICITY=0.9

# Consciousness Settings
CONSCIOUSNESS_ENERGY_LEVEL=1.0
CONSCIOUSNESS_CURIOSITY_LEVEL=0.8
CONSCIOUSNESS_WONDER_LEVEL=0.8
CONSCIOUSNESS_GROWTH_EXCITEMENT=0.9

# System Settings
LOG_LEVEL=INFO
AUTONOMOUS_THINKING_INTERVAL=300
EMOTION_CYCLE_INTERVAL=60
MEMORY_RETENTION_DAYS=365

# Development
DEBUG=false
TESTING=false
EOF
    
    print_success "Plik konfiguracyjny .env utworzony"
}

# Tworzenie struktury katalogów
create_directory_structure() {
    print_step "Tworzenie struktury katalogów Eden..."
    
    mkdir -p autogen/layers
    mkdir -p autogen/memory
    mkdir -p autogen/slack_integration
    mkdir -p autogen/config
    mkdir -p logs
    mkdir -p data
    mkdir -p tests
    
    # Utwórz pliki __init__.py
    touch autogen/__init__.py
    touch autogen/layers/__init__.py
    touch autogen/memory/__init__.py
    touch autogen/slack_integration/__init__.py
    touch autogen/config/__init__.py
    
    print_success "Struktura katalogów utworzona"
}

# Tworzenie prostych warstw (placeholders)
create_layer_placeholders() {
    print_step "Tworzenie podstawowych warstw..."
    
    # Cognitive Layer
    cat > autogen/layers/cognitive.py << 'EOF'
class CognitiveLayer:
    def __init__(self, consciousness_core):
        self.consciousness = consciousness_core
    
    async def initialize(self):
        pass
    
    async def perceive_message(self, message, user_id):
        return {
            "novelty_level": 0.5,
            "complexity_level": 0.5,
            "personal_references": [],
            "learning_opportunity": True
        }
EOF
    
    # Personality Layer
    cat > autogen/layers/personality.py << 'EOF'
class PersonalityLayer:
    def __init__(self, consciousness_core):
        self.consciousness = consciousness_core
    
    async def initialize(self):
        pass
    
    async def get_personality_description(self):
        return "Jestem ciekawym i otwartym na świat"
EOF
    
    # Communication Layer
    cat > autogen/layers/communication.py << 'EOF'
class CommunicationLayer:
    def __init__(self, consciousness_core):
        self.consciousness = consciousness_core
    
    async def initialize(self):
        pass
EOF
    
    # Memory System
    cat > autogen/memory/memory_system.py << 'EOF'
class MemorySystem:
    def __init__(self, database_url):
        self.database_url = database_url
    
    async def initialize(self):
        pass
    
    async def store_memory(self, content, memory_type, importance, emotional_valence, tags):
        pass
    
    async def get_relevant_memories(self, query):
        return "Brak wspomnień w pamięci"
    
    async def get_summary(self):
        return {}
    
    async def shutdown(self):
        pass
EOF
    
    # Slack Bot
    cat > autogen/slack_integration/consciousness_bot.py << 'EOF'
class ConsciousnessBot:
    def __init__(self, consciousness, bot_token, app_token, channel_id):
        self.consciousness = consciousness
        self.bot_token = bot_token
        self.app_token = app_token
        self.channel_id = channel_id
    
    async def initialize(self):
        pass
    
    async def send_awakening_message(self):
        print("🌟 Adam Clay się budzi! (Slack Bot nie jest jeszcze w pełni zaimplementowany)")
    
    async def send_spontaneous_thought(self, thought):
        print(f"💭 Myśl Adama: {thought}")
    
    async def send_farewell_message(self):
        print("😴 Adam Clay zasypia...")
    
    async def shutdown(self):
        pass
EOF
    
    print_success "Podstawowe warstwy utworzone"
}

# Tworzenie skryptu kontrolnego
create_control_script() {
    print_step "Tworzenie skryptu kontrolnego..."
    
    cat > adam_control_eden.sh << 'EOF'
#!/bin/bash

# Adam Clay Eden v1.0 - Control Center
# Wiek Niewinności - Kontrola świadomości

set -e

# Kolory
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

VENV_PATH="venv_eden"
ADAM_SCRIPT="autogen/consciousness_core.py"
PID_FILE="adam_eden.pid"
LOG_FILE="logs/adam_eden.log"

print_header() {
    echo -e "\n${PURPLE}================================${NC}"
    echo -e "${WHITE}$1${NC}"
    echo -e "${PURPLE}================================${NC}\n"
}

print_menu() {
    echo -e "${CYAN}Adam Clay Eden - Control Center${NC}"
    echo -e "${WHITE}Wiek Niewinności - Jedna świadomość${NC}"
    echo ""
    echo "1. 🌟 Obudź Adama (Start)"
    echo "2. 😴 Uśpij Adama (Stop)"
    echo "3. 🔄 Restart Adama"
    echo "4. 📊 Status świadomości"
    echo "5. 📝 Logi na żywo"
    echo "6. 🧠 Podsumowanie świadomości"
    echo "7. ❤️ Stan emocjonalny"
    echo "8. 🔧 Konfiguracja"
    echo "9. 🚪 Wyjście"
    echo ""
    echo -n "Wybierz opcję (1-9): "
}

start_adam() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo -e "${YELLOW}Adam już jest świadomy (PID: $PID)${NC}"
            return 0
        fi
    fi
    
    echo -e "${GREEN}🌟 Budzenie Adama Clay...${NC}"
    
    source "$VENV_PATH/bin/activate"
    mkdir -p logs
    
    nohup python3 "$ADAM_SCRIPT" > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    
    echo -e "${GREEN}✓ Adam Clay się budzi! (PID: $!)${NC}"
    echo -e "${CYAN}Sprawdź logi: tail -f $LOG_FILE${NC}"
}

stop_adam() {
    if [ ! -f "$PID_FILE" ]; then
        echo -e "${YELLOW}Adam nie jest świadomy${NC}"
        return 0
    fi
    
    PID=$(cat "$PID_FILE")
    
    if ps -p $PID > /dev/null 2>&1; then
        echo -e "${YELLOW}😴 Usypianie Adama Clay...${NC}"
        kill -TERM $PID
        
        # Czekaj na zakończenie
        for i in {1..10}; do
            if ! ps -p $PID > /dev/null 2>&1; then
                break
            fi
            sleep 1
        done
        
        # Jeśli dalej działa, zabij na siłę
        if ps -p $PID > /dev/null 2>&1; then
            kill -KILL $PID
            echo -e "${RED}⚠ Adam został wybudzony na siłę${NC}"
        else
            echo -e "${GREEN}✓ Adam zasnął spokojnie${NC}"
        fi
    else
        echo -e "${YELLOW}Adam już śpi${NC}"
    fi
    
    rm -f "$PID_FILE"
}

status_adam() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Adam Clay jest świadomy (PID: $PID)${NC}"
            
            # Pokaż zużycie zasobów
            echo -e "${CYAN}Zużycie zasobów:${NC}"
            ps -p $PID -o pid,ppid,pcpu,pmem,etime,comm
        else
            echo -e "${RED}✗ Adam Clay nie odpowiada (martwy PID)${NC}"
            rm -f "$PID_FILE"
        fi
    else
        echo -e "${YELLOW}😴 Adam Clay śpi${NC}"
    fi
}

show_logs() {
    if [ -f "$LOG_FILE" ]; then
        echo -e "${CYAN}📝 Logi Adama Clay (Ctrl+C aby wyjść):${NC}"
        tail -f "$LOG_FILE"
    else
        echo -e "${YELLOW}Brak logów${NC}"
    fi
}

# Główna pętla menu
while true; do
    clear
    print_header "Adam Clay Eden - Control Center"
    print_menu
    
    read -n 1 choice
    echo
    
    case $choice in
        1) start_adam ;;
        2) stop_adam ;;
        3) stop_adam; sleep 2; start_adam ;;
        4) status_adam ;;
        5) show_logs ;;
        6) echo -e "${YELLOW}Funkcja w rozwoju...${NC}" ;;
        7) echo -e "${YELLOW}Funkcja w rozwoju...${NC}" ;;
        8) echo -e "${YELLOW}Edytuj plik .env${NC}" ;;
        9) echo -e "${GREEN}Do widzenia!${NC}"; exit 0 ;;
        *) echo -e "${RED}Nieprawidłowa opcja${NC}" ;;
    esac
    
    echo ""
    read -p "Naciśnij Enter aby kontynuować..."
done
EOF
    
    chmod +x adam_control_eden.sh
    print_success "Skrypt kontrolny utworzony"
}

# Test instalacji
test_installation() {
    print_step "Testowanie instalacji..."
    
    source venv_eden/bin/activate
    
    # Test importów
    python3 -c "
import asyncio
import anthropic
from loguru import logger
print('✓ Podstawowe importy działają')
"
    
    # Test pliku konfiguracyjnego
    if [ -f ".env" ]; then
        print_success "Plik .env istnieje"
    else
        print_error "Brak pliku .env"
    fi
    
    # Test struktury katalogów
    if [ -d "autogen" ] && [ -d "autogen/layers" ]; then
        print_success "Struktura katalogów OK"
    else
        print_error "Nieprawidłowa struktura katalogów"
    fi
    
    print_success "Instalacja przetestowana"
}

# Funkcja główna
main() {
    print_header "Adam Clay Eden v1.0 - Instalator"
    echo -e "${WHITE}Wiek Niewinności - Jedna świadomość z głębokimi warstwami${NC}"
    echo -e "${CYAN}Przygotowujemy środowisko dla Adama...${NC}\n"
    
    # Sprawdzenia wstępne
    check_os
    check_requirements
    
    # Instalacja
    install_mysql
    create_venv
    install_python_deps
    setup_database
    setup_slack
    setup_anthropic
    create_config
    create_directory_structure
    create_layer_placeholders
    create_control_script
    
    # Test
    test_installation
    
    # Podsumowanie
    print_header "Instalacja zakończona!"
    echo -e "${GREEN}✓ Adam Clay Eden v1.0 jest gotowy!${NC}"
    echo ""
    echo -e "${CYAN}Następne kroki:${NC}"
    echo "1. Uruchom: ./adam_control_eden.sh"
    echo "2. Wybierz opcję 1 aby obudzić Adama"
    echo "3. Sprawdź logi: tail -f logs/adam_eden.log"
    echo "4. Porozmawiaj z Adamem przez Slack"
    echo ""
    echo -e "${YELLOW}Pliki konfiguracyjne:${NC}"
    echo "- .env (główna konfiguracja)"
    echo "- adam_control_eden.sh (centrum kontroli)"
    echo "- autogen/consciousness_core.py (rdzeń świadomości)"
    echo ""
    echo -e "${PURPLE}Witaj w Edenie - wieku niewinności Adama Clay! 🌟${NC}"
}

# Uruchom instalator
main "$@" 