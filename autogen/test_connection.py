#!/usr/bin/env python3

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

print("🧪 Testowanie połączenia z MySQL...")

# Załaduj .env
load_dotenv()
db_url = os.getenv('DATABASE_URL')

if not db_url:
    print("❌ Brak DATABASE_URL w .env")
    exit(1)

print(f"📡 Próbuję połączyć się z: {db_url.replace('1voNPq3vTeLsvlog', '***')}")

try:
    engine = create_engine(db_url)
    
    with engine.connect() as conn:
        # Test podstawowy
        result = conn.execute(text('SELECT 1 as test'))
        print('✅ Podstawowe połączenie działa!')
        
        # Sprawdź bazę danych
        result = conn.execute(text('SELECT DATABASE() as current_db'))
        current_db = result.fetchone()[0]
        print(f'📊 Aktualna baza danych: {current_db}')
        
        # Sprawdź tabele
        result = conn.execute(text('SHOW TABLES'))
        tables = result.fetchall()
        print(f'📋 Dostępne tabele: {[table[0] for table in tables]}')
        
        # Utwórz tabele jeśli nie istnieją
        print('🔨 Tworzę tabele...')
        
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
        print('✅ Tabele utworzone/sprawdzone')
        
        # Sprawdź tabele ponownie
        result = conn.execute(text('SHOW TABLES'))
        tables = result.fetchall()
        print(f'📋 Tabele po utworzeniu: {[table[0] for table in tables]}')
        
        print('\n🎉 SUKCES! MySQL jest gotowy dla AutoGen!')
        print('📊 Szczegóły:')
        print('   - Baza danych: adam_clay_autogen')
        print('   - Użytkownik: autogen_godmode')
        print('   - Hasło: 1voNPq3vTeLsvlog')
        print('   - Tabele: conversations, agent_states')
        
except Exception as e:
    print(f'❌ Błąd połączenia: {e}')
    print('\n💡 Prawdopodobnie musisz najpierw utworzyć bazę danych i użytkownika.')
    print('Wykonaj w MySQL jako root:')
    print('   mysql -u root -p')
    print('Następnie:')
    print('   CREATE DATABASE IF NOT EXISTS adam_clay_autogen CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;')
    print('   CREATE USER IF NOT EXISTS "autogen_godmode"@"localhost" IDENTIFIED BY "1voNPq3vTeLsvlog";')
    print('   GRANT ALL PRIVILEGES ON adam_clay_autogen.* TO "autogen_godmode"@"localhost";')
    print('   FLUSH PRIVILEGES;')
    exit(1)
