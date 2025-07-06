#!/bin/bash
# Kompletna migracja SQLite → MySQL
set -e
echo "🔐 [1/5] Konfiguracja MySQL..."
sudo /usr/local/mysql/support-files/mysql.server stop 2>/dev/null || true
sudo mysqld_safe --skip-grant-tables &
sleep 5
mysql -u root <<-EOSQL
    FLUSH PRIVILEGES;
    ALTER USER 'root'@'localhost' IDENTIFIED BY 'TempRootPass123!';
    FLUSH PRIVILEGES;
    CREATE DATABASE IF NOT EXISTS adam_clay_autogen CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    CREATE USER 'autogen_user'@'localhost' IDENTIFIED BY 'AutoGenSecure123!';
    GRANT ALL PRIVILEGES ON adam_clay_autogen.* TO 'autogen_user'@'localhost';
    FLUSH PRIVILEGES;
EOSQL
sudo /usr/local/mysql/support-files/mysql.server restart
sleep 3
echo "💾 [2/5] Backup SQLite..."
BACKUP_FILE="autogen_$(date +%Y%m%d_%H%M%S).db.backup"
cp instance/autogen.db "instance/$BACKUP_FILE"
echo "✅ Backup: instance/$BACKUP_FILE"
echo "⚙️ [3/5] Aktualizacja .env..."
cat > .env <<EOT
AUTOGEN_DATABASE_HOST="localhost"
AUTOGEN_DATABASE_PORT=3306
AUTOGEN_DATABASE_USERNAME="autogen_user"
AUTOGEN_DATABASE_PASSWORD="AutoGenSecure123!"
AUTOGEN_DATABASE_NAME="adam_clay_autogen"
EOT
chmod 600 .env
echo "🔄 [4/5] Migracja danych..."
pip install sqlite3-to-mysql >/dev/null 2>&1 || { echo "❌ Błąd instalacji"; exit 1; }
sqlite3mysql --sqlite-file instance/autogen.db --mysql-user autogen_user --mysql-password AutoGenSecure123! --mysql-database adam_clay_autogen --mysql-host localhost --skip-foreign-keys 2>migration_errors.log || { echo "❌ Błąd migracji - sprawdz migration_errors.log"; exit 1; }
echo "🔍 [5/5] Weryfikacja..."
python3 - <<END || { echo "❌ Test połączenia nieudany"; exit 1; }
from database import test_database_connection, init_db
if test_database_connection():
    print("✅ Połączenie z MySQL działa")
    init_db()
else: exit(1)
END
python3 - <<END
from models import SubconsciousAgent
from database import SessionLocal
db = SessionLocal()
print(f"✅ Migracja udana! Agentów w MySQL: {db.query(SubconsciousAgent).count()}")
db.close()
END
echo "✨ Migracja zakończona!"
