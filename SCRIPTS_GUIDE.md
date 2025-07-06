# 🚀 ADAM CLAY - SKRYPTY ZARZĄDZANIA

Szybki przewodnik po skryptach zarządzania systemem Adam Clay.

## ⚡ SZYBKI START

```bash
# 🚀 Uruchom cały system
./start_adam_clay.sh

# 📊 Sprawdź status
./status_adam_clay.sh

# 🔄 Restart systemu
./restart_adam_clay.sh

# 🛑 Zatrzymaj system
./stop_adam_clay.sh
```

## 📋 WSZYSTKIE SKRYPTY

| Skrypt | Opis | Użycie |
|--------|------|--------|
| `start_adam_clay.sh` | 🚀 Start całego systemu | Pierwsze uruchomienie |
| `stop_adam_clay.sh` | 🛑 Stop całego systemu | Koniec pracy |
| `restart_adam_clay.sh` | 🔄 Restart systemu | Przy problemach |
| `status_adam_clay.sh` | 📊 Status systemu | Monitoring |
| `start_laravel.sh` | 🌐 Start Laravel API | Tylko API |
| `stop_laravel.sh` | 🛑 Stop Laravel API | Tylko API |
| `restart_laravel.sh` | 🔄 Restart Laravel | Tylko API |
| `status_laravel.sh` | 📊 Status Laravel | Monitoring API |
| `reset_adam_clay.sh` | 🧹 Reset wszystkich danych | ⚠️ Nieodwracalne! |
| `test_empty_database.sh` | 🧪 Test pustej bazy | Po resecie |

## 🎯 NAJCZĘŚCIEJ UŻYWANE

### 🔧 **Problem z systemem?**
```bash
./restart_adam_clay.sh
```

### 📊 **Sprawdź co się dzieje**
```bash
./status_adam_clay.sh
```

### 🧹 **Zresetuj wszystko**
```bash
./reset_adam_clay.sh
./start_adam_clay.sh
```

### 📋 **Zobacz logi**
```bash
tail -f data/logs/consciousness.log
tail -f data/logs/laravel.log
```

## 🌐 DOSTĘP DO SYSTEMU

- **Dashboard:** http://adamclay.local:8004/consciousness
- **API Test:** http://adamclay.local:8004/api/hello
- **Status API:** http://adamclay.local:8004/api/consciousness/thinking-status

## 📖 PEŁNA DOKUMENTACJA

Zobacz `SYSTEM_MANAGEMENT.md` dla pełnej dokumentacji wszystkich skryptów. 