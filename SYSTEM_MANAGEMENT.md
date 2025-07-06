# 🎛️ ZARZĄDZANIE SYSTEMEM ADAM CLAY

Kompletny zestaw skryptów do zarządzania wszystkimi komponentami systemu Adam Clay.

## 📋 DOSTĘPNE SKRYPTY

### 🚀 **URUCHAMIANIE**
```bash
./start_adam_clay.sh      # Uruchom cały system (Laravel + Consciousness)
./start_laravel.sh        # Uruchom tylko Laravel API
```

### 🛑 **ZATRZYMYWANIE**
```bash
./stop_adam_clay.sh       # Zatrzymaj cały system
./stop_laravel.sh         # Zatrzymaj tylko Laravel API
```

### 🔄 **RESTARTOWANIE**
```bash
./restart_adam_clay.sh    # Restart całego systemu
./restart_laravel.sh      # Restart tylko Laravel API
```

### 📊 **STATUS I MONITORING**
```bash
./status_adam_clay.sh     # Status całego systemu + testy funkcjonalności
./status_laravel.sh       # Status Laravel API + test bazy danych
```

### 🧹 **ZARZĄDZANIE DANYMI**
```bash
./reset_adam_clay.sh      # Wyczyść wszystkie dane (nieodwracalne!)
./test_empty_database.sh  # Test czy system działa z pustą bazą
```

---

## 📖 SZCZEGÓŁOWY OPIS SKRYPTÓW

### 🚀 **start_adam_clay.sh**
**Uruchamia cały system Adam Clay**

**Co robi:**
1. ✅ Sprawdza czy komponenty już działają
2. 🌐 Uruchamia Laravel API (jeśli nie działa)
3. 🧠 Uruchamia Consciousness przez Laravel API
4. 🔍 Testuje funkcjonalność systemu
5. 📊 Wyświetla status i dostępne URL-e

**Wymagania:**
- Katalog `web/` z projektem Laravel
- Katalog `core/` z Python environment
- Działająca baza danych MySQL

**Przykład użycia:**
```bash
./start_adam_clay.sh
```

---

### 🌐 **start_laravel.sh**
**Uruchamia Laravel API serwer**

**Co robi:**
1. ✅ Sprawdza czy Laravel już działa
2. 🔧 Weryfikuje konfigurację (.env, artisan)
3. 🗄️ Testuje połączenie z bazą danych
4. 🚀 Uruchamia serwer na `adamclay.local:8004`
5. 📋 Loguje do `data/logs/laravel_server.log`

**Ustawienia:**
- **Host:** adamclay.local
- **Port:** 8004
- **Logi:** data/logs/laravel_server.log

---

### 🛑 **stop_adam_clay.sh**
**Zatrzymuje cały system Adam Clay**

**Co robi:**
1. 🔍 Sprawdza jakie komponenty działają
2. 🧠 Zatrzymuje Consciousness (przez API lub bezpośrednio)
3. 🌐 Zatrzymuje Laravel API
4. ✅ Weryfikuje czy wszystko zostało zatrzymane
5. 🔧 Force kill jeśli graceful shutdown nie zadziałał

**Strategie zatrzymania:**
- Pierwsza próba: Graceful shutdown (SIGTERM)
- Druga próba: Force kill (SIGKILL)

---

### 🔄 **restart_adam_clay.sh**
**Restart całego systemu**

**Co robi:**
1. 🛑 Zatrzymuje cały system
2. ⏱️ Czeka 5 sekund na pełne zatrzymanie
3. 🚀 Uruchamia system od nowa
4. 🔍 Testuje funkcjonalność po restart
5. 📊 Wyświetla końcowy status

**Użycie:** Idealny przy problemach z synchronizacją komponentów

---

### 📊 **status_adam_clay.sh**
**Pełny status i diagnostyka systemu**

**Co sprawdza:**
- 🟢🟡🔴 Ogólny stan systemu
- 🌐 Laravel API (PID, CPU, RAM, uptime, test API)
- 🧠 Consciousness (PID, CPU, RAM, thinking status)
- 🗄️ Baza danych (połączenie, statystyki tabel)
- 📋 Logi systemu (rozmiar, ostatnie wpisy)
- 🔗 Testy connectivity (API, Dashboard)

**Przykładowy output:**
```
🎯 STATUS SYSTEMU: 🟢 PEŁNIE AKTYWNY

📊 KOMPONENTY SYSTEMU:
🌐 LARAVEL API: 🟢 AKTYWNY
   🔍 PID: 12345
   🖥️  CPU: 0.5%
   💾 RAM: 1.2%
   ⏰ Uptime: 2:30.45
   ✅ API odpowiada (HTTP 200)

🧠 CONSCIOUSNESS: 🟢 AKTYWNY
   🔍 PID: 12346
   🧠 Status: Myśli aktywnie
```

---

### 🧹 **reset_adam_clay.sh**
**Całkowity reset systemu**

**⚠️ UWAGA: Operacja nieodwracalna!**

**Co resetuje:**
- 🗄️ Wszystkie tabele bazy danych
- 📁 Pliki z `data/thoughts/`
- 📋 Stare pliki logów
- 🔄 Auto-increment counters

**Tabele czyszczone:**
- `thoughts` - wszystkie myśli
- `consciousness_sessions` - sesje świadomości
- `significant_memories` - wspomnienia
- `email_questions` - pytania email
- `learned_patterns` - wzorce uczenia
- `web_activity_log` - logi aktywności

**Bezpieczeństwo:**
- 🔒 Wymaga potwierdzenia przez wpisanie "tak"
- 🛑 Automatycznie zatrzymuje Adam Clay
- 📊 Pokazuje liczbę usuniętych rekordów

---

### 🧪 **test_empty_database.sh**
**Test systemu z pustą bazą danych**

**Co testuje:**
1. 🔍 API endpoints z pustą bazą
2. 🚀 Uruchomienie consciousness
3. 🆕 Automatyczne tworzenie sesji
4. 💭 Generowanie pierwszych myśli
5. ✅ Weryfikacja pełnej funkcjonalności

**Użycie:** Po resecie lub przed pierwszym uruchomieniem

---

## 🔧 TYPOWE SCENARIUSZE UŻYCIA

### 🎯 **Pierwsze uruchomienie systemu**
```bash
# 1. Test czy system może działać z pustą bazą
./test_empty_database.sh

# 2. Jeśli test OK, normalne uruchomienie
./start_adam_clay.sh

# 3. Sprawdź status
./status_adam_clay.sh
```

### 🔄 **Dzienny restart systemu**
```bash
./restart_adam_clay.sh
```

### 🧹 **Całkowity reset (nowy start)**
```bash
# 1. Reset wszystkich danych
./reset_adam_clay.sh

# 2. Test czy działa z pustą bazą
./test_empty_database.sh

# 3. Uruchomienie od nowa
./start_adam_clay.sh
```

### 🔧 **Troubleshooting**
```bash
# Sprawdź status
./status_adam_clay.sh

# Restart jeśli problemy
./restart_adam_clay.sh

# Jeśli nadal problemy - sprawdź komponenty osobno
./stop_adam_clay.sh
./start_laravel.sh
./status_laravel.sh

# Uruchom consciousness osobno
curl -X POST http://adamclay.local:8004/api/consciousness/start
```

### 🚀 **Tylko Laravel (bez consciousness)**
```bash
./start_laravel.sh
./status_laravel.sh
```

---

## 📋 MONITORING I LOGI

### 📊 **Logi systemowe:**
```bash
# Laravel serwer
tail -f data/logs/laravel_server.log

# Consciousness
tail -f data/logs/consciousness.log

# Wszystkie logi na żywo
tail -f data/logs/*.log
```

### 🔍 **Sprawdzanie procesów:**
```bash
# Sprawdź czy procesy działają
pgrep -f "php artisan serve"    # Laravel
pgrep -f "python3 main.py"      # Consciousness

# Szczegóły procesów
ps aux | grep "artisan serve"
ps aux | grep "python3 main.py"
```

### 🌐 **Testy API:**
```bash
# Test podstawowy
curl http://adamclay.local:8004/api/hello

# Status myślenia
curl http://adamclay.local:8004/api/consciousness/thinking-status

# Ostatnie myśli
curl http://adamclay.local:8004/api/thoughts/recent?limit=5
```

---

## ⚡ SKRÓTY I ALIASY

Możesz dodać do swojego `.bashrc` lub `.zshrc`:

```bash
# Adam Clay aliases
alias ac-start='./start_adam_clay.sh'
alias ac-stop='./stop_adam_clay.sh'
alias ac-restart='./restart_adam_clay.sh'
alias ac-status='./status_adam_clay.sh'
alias ac-reset='./reset_adam_clay.sh'

alias laravel-start='./start_laravel.sh'
alias laravel-stop='./stop_laravel.sh'
alias laravel-status='./status_laravel.sh'

# Monitoring
alias ac-logs='tail -f data/logs/*.log'
alias ac-consciousness='tail -f data/logs/consciousness.log'
alias ac-laravel='tail -f data/logs/laravel_server.log'
```

---

## 🆘 TROUBLESHOOTING

### ❌ **Laravel nie uruchamia się**
```bash
# Sprawdź konfigurację
cat web/.env

# Sprawdź bazę danych
mysql -u root -p adam_clay -e "SHOW TABLES;"

# Sprawdź PHP
cd web && php artisan --version

# Reset Laravel cache
cd web && php artisan config:clear && php artisan cache:clear
```

### ❌ **Consciousness nie uruchamia się**
```bash
# Sprawdź Python environment
ls -la core/adam_clay_env/

# Test ręczny
cd core && source adam_clay_env/bin/activate && python3 main.py

# Sprawdź klucz API
grep -i llm-provider core/config.json
echo $LLM_PROVIDER_API_KEY
```

### ❌ **Baza danych niedostępna**
```bash
# Sprawdź MySQL
brew services list | grep mysql
brew services start mysql

# Test połączenia
mysql -u root -p -e "SHOW DATABASES;"
```

### ❌ **Porty zajęte**
```bash
# Sprawdź co używa portu 8004
lsof -i :8004

# Zabij procesy na porcie
pkill -f "port 8004"
```

---

## 🎯 NAJWAŻNIEJSZE KOMENDY

```bash
# 🚀 Start systemu
./start_adam_clay.sh

# 📊 Sprawdź status
./status_adam_clay.sh

# 🔄 Restart przy problemach
./restart_adam_clay.sh

# 🛑 Zatrzymaj system
./stop_adam_clay.sh

# 🧹 Reset przy poważnych problemach
./reset_adam_clay.sh
```

**System Adam Clay jest teraz w pełni zarządzalny przez skrypty!** 🎉 