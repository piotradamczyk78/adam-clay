#!/bin/bash
set -e

# Konfiguracja
DB_USER="autogen_godmode"
DB_PASS=$(openssl rand -base64 12 | tr -d '/+' | cut -c1-16)
DB_NAME="adam_clay_autogen"
PROJECT_DIR="/Users/piotradamczyk/Projects/AdamClay/autogen"
LOG_FILE="$PROJECT_DIR/simple_migration_$(date +%Y%m%d_%H%M%S).log"

# Funkcja do logowania
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

echo "🚀 Prosta migracja AutoGen do MySQL"
echo "=================================="

# 1. Sprawdź MySQL
log "🔧 Sprawdzam MySQL..."
if ! mysqladmin ping -h localhost -u root --silent; then
    log "🚀 Uruchamiam MySQL..."
    sudo /usr/local/mysql/support-files/mysql.server start || {
        log "❌ MySQL nie chce wystartować"
        exit 1
    }
fi

# 2. Próbuj różne opcje logowania
log "🔨 Próbuję utworzyć bazę $DB_NAME..."

# Opcja 1: bez hasła
if mysql -u root -e "SELECT 1;" 2>/dev/null; then
    log "✅ MySQL root bez hasła - tworzę bazę..."
    mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
EOF
else
    # Opcja 2: z hasłem - używamy mysql_config_editor lub pytamy
    log "🔑 MySQL wymaga hasła. Próbuję z mysql_config_editor..."
    if mysql --login-path=root -e "SELECT 1;" 2>/dev/null; then
        log "✅ Używam mysql_config_editor..."
        mysql --login-path=root <<EOF
CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
EOF
    else
        log "❌ Nie mogę połączyć się z MySQL jako root"
        echo ""
        echo "💡 Opcje rozwiązania:"
        echo "1. Uruchom: mysql -u root -p"
        echo "   Następnie wykonaj:"
        echo "   CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        echo "   CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';"
        echo "   GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';"
        echo "   FLUSH PRIVILEGES;"
        echo ""
        echo "2. Lub zresetuj hasło roota MySQL:"
        echo "   sudo /usr/local/mysql/support-files/mysql.server stop"
        echo "   sudo /usr/local/mysql/bin/mysqld_safe --skip-grant-tables &"
        echo "   mysql -u root"
        echo "   ALTER USER 'root'@'localhost' IDENTIFIED BY '';"
        echo "   FLUSH PRIVILEGES;"
        echo ""
        echo "3. Lub ustaw mysql_config_editor:"
        echo "   mysql_config_editor set --login-path=root --host=localhost --user=root --password"
        echo ""
        echo "Hasło dla nowego użytkownika: $DB_PASS"
        echo "Zapisz to hasło!"
        exit 1
    fi
fi

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
log "✅ Plik .env utworzony"

# 4. Testuj połączenie
log "🧪 Testuję połączenie..."
python -c "
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv('DATABASE_URL'))

try:
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1 as test'))
        print('✅ Połączenie z MySQL działa!')
        
        # Tworzenie tabel
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
        
        # Sprawdź tabele
        result = conn.execute(text('SHOW TABLES'))
        tables = result.fetchall()
        print(f'Dostępne tabele: {[table[0] for table in tables]}')
        
except Exception as e:
    print(f'❌ Błąd: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    log "🎉 Migracja zakończona sukcesem!"
    echo ""
    echo "🚀 GOTOWE! MySQL skonfigurowany dla AutoGen!"
    echo "📊 Szczegóły:"
    echo "   - Baza danych: $DB_NAME"
    echo "   - Użytkownik: $DB_USER"
    echo "   - Hasło: $DB_PASS"
    echo "   - Plik .env: $PROJECT_DIR/.env"
    echo ""
    echo "💡 Zapisz hasło: $DB_PASS"
    
    # Wyświetl powiadomienie systemowe (macOS)
    osascript -e "display notification \"AutoGen MySQL migration completed!\" with title \"Migration Success\" sound name \"Glass\"" 2>/dev/null || true
else
    log "❌ Migracja nieudana"
    exit 1
fi 