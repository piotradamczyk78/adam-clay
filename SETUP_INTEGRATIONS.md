# 🔧 Instrukcja Konfiguracji Integracji - Adam Clay Eden

Ten dokument opisuje jak skonfigurować wszystkie niezbędne integracje dla Adam Clay Eden.

## 📋 Spis Treści

1. [Anthropic Claude API](#1-anthropic-claude-api)
2. [Slack Integration](#2-slack-integration)
3. [Baza Danych](#3-baza-danych)
4. [Konfiguracja Środowiska](#4-konfiguracja-środowiska)
5. [Weryfikacja Konfiguracji](#5-weryfikacja-konfiguracji)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. 🧠 Anthropic Claude API

### Krok 1: Uzyskanie API Key

1. **Zarejestruj się** na [Anthropic Console](https://console.anthropic.com/)
2. **Potwierdź email** i zaloguj się
3. **Przejdź do API Keys** w menu bocznym
4. **Kliknij "Create Key"**
5. **Skopiuj klucz** - UWAGA: Będzie widoczny tylko raz!

### Krok 2: Dodanie do konfiguracji

```bash
# W pliku .env
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Krok 3: Ustawienie limitu budżetu

1. W Anthropic Console przejdź do **"Usage & Billing"**
2. Ustaw **daily spending limit** (zalecane: $10/dzień)
3. Skonfiguruj **alerts** przy 80% wykorzystania

---

## 2. 🔔 Slack Integration

### Krok 1: Tworzenie Slack App

1. **Przejdź do** [Slack API](https://api.slack.com/apps)
2. **Kliknij "Create New App"**
3. **Wybierz "From scratch"**
4. **Nazwa aplikacji:** `Adam Clay Eden`
5. **Wybierz workspace** gdzie chcesz zainstalować

### Krok 2: Konfiguracja Bot Token Scopes

1. W **"OAuth & Permissions"** dodaj następujące **Bot Token Scopes:**
   ```
   app_mentions:read    # Czytanie wzmianek
   channels:read        # Czytanie kanałów
   chat:write          # Pisanie wiadomości
   chat:write.public   # Pisanie na kanałach publicznych
   im:read             # Czytanie DM
   im:write            # Pisanie DM
   users:read          # Czytanie profili użytkowników
   files:write         # Przesyłanie plików (opcjonalne)
   reactions:write     # Dodawanie emoji reakcji
   ```

### Krok 3: Instalacja aplikacji

1. **Kliknij "Install to Workspace"**
2. **Autoryzuj aplikację**
3. **Skopiuj Bot User OAuth Token** (zaczyna się od `xoxb-`)

### Krok 4: Socket Mode (dla real-time komunikacji)

1. **Przejdź do "Socket Mode"**
2. **Włącz Socket Mode**
3. **Skopiuj App Token** (zaczyna się od `xapp-`)

### Krok 5: Event Subscriptions

1. **Przejdź do "Event Subscriptions"**
2. **Włącz Events**
3. **Dodaj Bot Events:**
   ```
   app_mention      # Gdy ktoś wspomni @AdamClay
   message.channels # Wiadomości na kanałach
   message.im       # Wiadomości prywatne
   ```

### Krok 6: Znajdowanie ID

#### Channel ID:
1. **Otwórz kanał** gdzie ma działać Adam
2. **Kliknij prawym przyciskiem** na nazwę kanału
3. **"Copy link"**
4. **ID jest na końcu URL:** `...../C1234567890`

#### User ID (Twoje):
1. **Kliknij na swój profil** w Slack
2. **"Copy member ID"**
3. **Wklej do konfiguracji**

### Krok 7: Dodanie do konfiguracji

```bash
# W pliku .env
SLACK_BOT_TOKEN=xoxb-1234567890123-1234567890123-abcdefghijklmnopqrstuvwx
SLACK_APP_TOKEN=xapp-1-A1234567890-1234567890123-abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmn
SLACK_CHANNEL_ID=C1234567890
SLACK_USER_ID=U1234567890
```

---

## 3. 🗄️ Baza Danych

### Opcja A: SQLite (Zalecana dla początkujących)

```bash
# W pliku .env
DATABASE_TYPE=sqlite
DATABASE_PATH=data/eden.db
```

**Zalety:**
- ✅ Brak dodatkowej konfiguracji
- ✅ Działa out-of-the-box
- ✅ Idealne do developmentu
- ✅ Automatyczne backup

**Wady:**
- ❌ Nie obsługuje concurrent access
- ❌ Mniejsza wydajność przy dużych danych

### Opcja B: MySQL (Zaawansowana)

#### Krok 1: Instalacja MySQL

**macOS (Homebrew):**
```bash
brew install mysql
brew services start mysql
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
```

#### Krok 2: Tworzenie bazy danych

```sql
-- Zaloguj się do MySQL
mysql -u root -p

-- Utwórz bazę danych
CREATE DATABASE adam_clay_eden CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Utwórz użytkownika
CREATE USER 'adam_clay_user'@'localhost' IDENTIFIED BY 'strong_password_here';

-- Nadaj uprawnienia
GRANT ALL PRIVILEGES ON adam_clay_eden.* TO 'adam_clay_user'@'localhost';
FLUSH PRIVILEGES;

EXIT;
```

#### Krok 3: Konfiguracja

```bash
# W pliku .env
DATABASE_TYPE=mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=adam_clay_eden
MYSQL_USERNAME=adam_clay_user
MYSQL_PASSWORD=strong_password_here
```

---

## 4. ⚙️ Konfiguracja Środowiska

### Krok 1: Skopiuj plik konfiguracyjny

```bash
# Skopiuj przykładowy plik
cp env.example .env

# Edytuj własną konfigurację
nano .env  # lub vim .env
```

### Krok 2: Dostosuj parametry psychologiczne

**Edytuj plik:** `autogen/config/eden_config.json`

```json
{
  "mood": {
    "curiosity": 0.8,        // Ciekawość (0-1)
    "excitement": 0.7,       // Podekscytowanie
    "happiness": 0.6,        // Szczęście
    "energy": 0.7,           // Energia
    "focus": 0.6            // Koncentracja
  },
  "dopamine": {
    "current_level": 50.0,   // Aktualny poziom dopaminy
    "triggers": {
      "positive_feedback": 15.0,  // +15 za pozytywny feedback
      "creative_achievement": 20.0 // +20 za kreatywne osiągnięcie
    }
  },
  "economic": {
    "daily_budget_limit": 10.0,    // $10/dzień limit
    "max_daily_requests": 500      // Max 500 requestów/dzień
  }
}
```

### Krok 3: Ustawienia snu

```json
{
  "sleep": {
    "deep_sleep_start": "01:00",    // Głęboki sen od 1:00
    "deep_sleep_end": "07:00",      // Do 7:00
    "light_sleep_start": "23:00",   // Lekki sen od 23:00
    "light_sleep_end": "08:00"      // Do 8:00
  }
}
```

---

## 5. ✅ Weryfikacja Konfiguracji

### Krok 1: Test instalatorem

```bash
# Uruchom instalator Eden
./install_eden.sh

# Wybierz opcję testowania konfiguracji
```

### Krok 2: Test ręczny

```bash
# Aktywuj środowisko
source venv_eden/bin/activate

# Test Anthropic API
python -c "
import os
from anthropic import Anthropic
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
print('✅ Anthropic API działa!')
"

# Test Slack API
python -c "
import os
from slack_sdk import WebClient
client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
response = client.auth_test()
print(f'✅ Slack API działa! Bot: {response[\"user\"]}')
"
```

### Krok 3: Test pełnej konfiguracji

```bash
# Przejdź do katalogu autogen
cd autogen

# Uruchom test konfiguracji
python -c "
from config.settings import get_config
config = get_config()
if config.validate_config():
    print('🎉 Konfiguracja jest kompletna!')
else:
    print('❌ Problemy z konfiguracją')
"
```

---

## 6. 🔧 Troubleshooting

### Problem: "Invalid API Key" (Anthropic)

**Rozwiązania:**
1. Sprawdź czy klucz jest poprawnie skopiowany (bez spacji)
2. Sprawdź czy masz środki na koncie Anthropic
3. Sprawdź czy klucz nie wygasł

### Problem: "Invalid Auth" (Slack)

**Rozwiązania:**
1. Sprawdź czy aplikacja jest zainstalowana w workspace
2. Sprawdź uprawnienia (scopes)
3. Wygeneruj nowe tokeny jeśli potrzeba

### Problem: "Database Connection Failed"

**SQLite:**
```bash
# Sprawdź uprawnienia
ls -la data/
mkdir -p data  # Utwórz katalog jeśli nie istnieje
```

**MySQL:**
```bash
# Test połączenia
mysql -h localhost -u adam_clay_user -p adam_clay_eden
```

### Problem: "Permission Denied"

```bash
# Popraw uprawnienia skryptów
chmod +x install_eden.sh
chmod +x adam_control_eden.sh
```

### Problem: "Module Not Found"

```bash
# Sprawdź środowisko wirtualne
source venv_eden/bin/activate
pip install -r requirements.txt
```

---

## 📞 Wsparcie

Jeśli masz problemy z konfiguracją:

1. **Sprawdź logi:** `tail -f data/logs/eden.log`
2. **Użyj centrum kontroli:** `./adam_control_eden.sh`
3. **Przeczytaj komunikaty błędów** - często są bardzo pomocne
4. **Sprawdź dokumentację API** - Anthropic i Slack

---

## 🎯 Następne Kroki

Po ukończeniu konfiguracji:

1. **Uruchom Adam Clay Eden:** `./adam_control_eden.sh`
2. **Napisz pierwszą wiadomość** na Slack: `@AdamClay cześć!`
3. **Monitoruj logi** czy wszystko działa
4. **Dostosuj parametry** osobowości według preferencji

**Gratulacje! Adam Clay Eden jest gotowy do życia!** 🌱✨ 