#!/bin/bash
set -e

# Konfiguracja
DB_USER="autogen_godmode"
DB_PASS=$(openssl rand -base64 12 | tr -d '/+' | cut -c1-16)
DB_NAME="adam_clay_autogen"
PROJECT_DIR="/Users/piotradamczyk/Projects/AdamClay/autogen"
LOG_FILE="$PROJECT_DIR/migration_$(date +%Y%m%d_%H%M%S).log"

# Funkcja do logowania
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# 1. Sprawdź MySQL
log "🔧 Sprawdzam MySQL..."
if ! mysqladmin ping -h localhost -u root --silent; then
    log "🚀 Uruchamiam MySQL..."
    sudo /usr/local/mysql/support-files/mysql.server start >> "$LOG_FILE" 2>&1 || {
        log "❌ MySQL nie chce wystartować"
        exit 1
    }
fi

# 2. Utwórz bazę danych
log "🔨 Tworzę bazę $DB_NAME..."
echo "💡 Podaj hasło roota MySQL:"
read -s MYSQL_ROOT_PASS

mysql -u root -p"$MYSQL_ROOT_PASS" <<EOF >> "$LOG_FILE" 2>&1 || {
    log "❌ Problem z bazą danych - sprawdź hasło roota"
    exit 1
}
CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
EOF

# 3. Utwórz plik .env
log "📝 Tworzę plik .env..."
cat > "$PROJECT_DIR/.env" << ENV_EOF
# Database Configuration
DATABASE_URL=mysql+pymysql://$DB_USER:$DB_PASS@localhost/$DB_NAME

# AutoGen Configuration
AUTOGEN_CONFIG_LIST_PATH=./OAI_CONFIG_LIST.json
AUTOGEN_CACHE_SEED=42
AUTOGEN_WORK_DIR=./autogen_work

# Logging
LOG_LEVEL=INFO
LOG_FILE=./autogen.log
ENV_EOF

chmod 600 "$PROJECT_DIR/.env"
log "✅ Plik .env utworzony z hasłem: $DB_PASS"

# 4. Zainstaluj zależności
log "📦 Instaluję zależności..."
cd "$PROJECT_DIR"
pip install -r requirements.txt >> "$LOG_FILE" 2>&1 || {
    log "❌ Problem z instalacją zależności"
    exit 1
}

# 5. Inicjalizuj bazę danych
log "🗃️ Inicjalizuję bazę danych..."
python -c "
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv('DATABASE_URL'))

# Tworzenie podstawowych tabel
with engine.connect() as conn:
    conn.execute(text('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            session_id VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            sender VARCHAR(50) NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_session (session_id),
            INDEX idx_timestamp (timestamp)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    '''))
    
    conn.execute(text('''
        CREATE TABLE IF NOT EXISTS agent_states (
            id INT AUTO_INCREMENT PRIMARY KEY,
            agent_name VARCHAR(255) NOT NULL,
            state_data JSON,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            UNIQUE KEY unique_agent (agent_name)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    '''))
    
    conn.commit()
    print('✅ Tabele utworzone pomyślnie')
" >> "$LOG_FILE" 2>&1 || {
    log "❌ Problem z inicjalizacją bazy danych"
    exit 1
}

# 6. Migruj dane z SQLite (jeśli istnieje)
if [ -f "$PROJECT_DIR/autogen.db" ]; then
    log "🔄 Migruję dane z SQLite..."
    python -c "
import sqlite3
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
mysql_engine = create_engine(os.getenv('DATABASE_URL'))

# Połącz z SQLite
sqlite_conn = sqlite3.connect('autogen.db')
sqlite_ide = sqlite_conn.ide()

try:
    # Sprawdź czy tabele istnieją w SQLite
    sqlite_ide.execute(\"SELECT name FROM sqlite_master WHERE type='table'\")
    tables = sqlite_ide.fetchall()
    print(f'Znalezione tabele w SQLite: {tables}')
    
    # Migruj conversations jeśli istnieje
    try:
        sqlite_ide.execute('SELECT * FROM conversations')
        conversations = sqlite_ide.fetchall()
        
        if conversations:
            with mysql_engine.connect() as mysql_conn:
                for row in conversations:
                    mysql_conn.execute(text('''
                        INSERT INTO conversations (session_id, message, sender, timestamp)
                        VALUES (:session_id, :message, :sender, :timestamp)
                    '''), {
                        'session_id': row[1],
                        'message': row[2], 
                        'sender': row[3],
                        'timestamp': row[4]
                    })
                mysql_conn.commit()
            print(f'✅ Zmigrowano {len(conversations)} konwersacji')
    except Exception as e:
        print(f'Tabela conversations nie istnieje lub jest pusta: {e}')
        
except Exception as e:
    print(f'Błąd migracji: {e}')
finally:
    sqlite_conn.close()
" >> "$LOG_FILE" 2>&1
fi

# 7. Testuj połączenie
log "🧪 Testuję połączenie..."
python -c "
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv('DATABASE_URL'))

with engine.connect() as conn:
    result = conn.execute(text('SELECT 1 as test'))
    print('✅ Połączenie z MySQL działa!')
    
    # Sprawdź tabele
    result = conn.execute(text('SHOW TABLES'))
    tables = result.fetchall()
    print(f'Dostępne tabele: {[table[0] for table in tables]}')
" >> "$LOG_FILE" 2>&1 || {
    log "❌ Problem z testowaniem połączenia"
    exit 1
}

# 8. Powiadomienie o sukcesie
log "🎉 Migracja zakończona sukcesem!"
log "📊 Szczegóły:"
log "   - Baza danych: $DB_NAME"
log "   - Użytkownik: $DB_USER"
log "   - Hasło: $DB_PASS"
log "   - Plik .env: $PROJECT_DIR/.env"
log "   - Log: $LOG_FILE"

# Wyświetl powiadomienie systemowe (macOS)
osascript -e "display notification \"AutoGen MySQL migration completed successfully!\" with title \"Migration Success\" sound name \"Glass\"" 2>/dev/null || true

echo ""
echo "🚀 GOTOWE! Możesz teraz uruchomić AutoGen z MySQL!"
echo "💡 Sprawdź plik .env dla szczegółów konfiguracji"
echo "📋 Log migracji: $LOG_FILE" 