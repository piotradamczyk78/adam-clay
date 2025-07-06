# 🌐 Adam Clay - Przyjazny Adres Skonfigurowany!

## ✅ **Problem Rozwiązany**

**Błąd:** `SQLSTATE[42S02]: Base table or view not found: 1146 Table 'adam_clay.sessions' doesn't exist`

**Rozwiązanie:** Zmiana konfiguracji Laravel z database sessions na file sessions

## 🎯 **Dostępne Adresy**

### 🌐 **Główny Dashboard:**
- **http://adamclay.local:8004** (główny)
- http://adamclay.local:8004/dashboard
- http://adamclay.local:8004/console
- http://adamclay.local:8004/monitor  
- http://adamclay.local:8004/consciousness

### 🔌 **API Endpoint:**
- **http://adamclay.local:8004/api/** (dla Python client)

## ⚙️ **Zmiany Techniczne**

### 1. **DNS Mapping**
```bash
# /etc/hosts
127.0.0.1 adamclay.local
```

### 2. **Laravel Sessions**
```php
// config/session.php
'driver' => env('SESSION_DRIVER', 'file'),  // zmienione z 'database'
```

### 3. **Python REST Client**
```python
# src/core/rest_api_client.py
base_url: str = "http://adamclay.local:8004/api"  // zaktualizowane
```

### 4. **Laravel Routes**
```php
// routes/web.php - dodane przyjazne URLe:
Route::get('/', [DashboardController::class, 'index']);
Route::get('/dashboard', [DashboardController::class, 'index']);
Route::get('/console', [DashboardController::class, 'index']);
Route::get('/monitor', [DashboardController::class, 'index']);
Route::get('/consciousness', [DashboardController::class, 'index']);
```

## 🧪 **Status Testów**

✅ **DNS Resolution:** adamclay.local → 127.0.0.1  
✅ **Laravel Server:** aktywny na porcie 8004  
✅ **API Endpoint:** `/api/hello` odpowiada  
✅ **Dashboard:** renderuje bez błędów  
✅ **Sessions:** file-based, działają poprawnie  
✅ **Python Client:** łączy się z adamclay.local  

## 🚀 **Jak używać**

### **Otwórz Dashboard:**
```bash
open http://adamclay.local:8004
```

### **Test API:**
```bash
curl http://adamclay.local:8004/api/hello
```

### **Uruchom Adam Clay:**
```bash
cd adam_clay_project
python main.py
```

## 📁 **Pliki Skonfigurowane**

- ✅ `/etc/hosts` - DNS mapping
- ✅ `adam_clay_project/src/core/rest_api_client.py` - nowy base_url
- ✅ `adam_clay_web/config/session.php` - zmiana na file sessions
- ✅ `adam_clay_web/routes/web.php` - dodatkowe URLe
- ✅ `adam_clay_web/setup_friendly_domain.sh` - skrypt pomocniczy

## 💡 **Tips**

1. **Bookmark:** Dodaj `adamclay.local:8004` do zakładek przeglądarki
2. **Mobile:** Użyj `http://adamclay.local:8004` na telefonie (w tej samej sieci)
3. **Development:** Wszystkie URLe prowadzą do tego samego dashboard
4. **SSL:** W przyszłości można dodać HTTPS z self-signed cert

---

**🎉 Adam Clay Dashboard dostępny pod przyjaznym adresem: `adamclay.local:8004`**

*Problem z sessions rozwiązany • Python integration działa • Wszystkie testy przeszły* 