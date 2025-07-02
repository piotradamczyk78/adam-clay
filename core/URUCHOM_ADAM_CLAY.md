# 🚀 JAK URUCHOMIĆ ADAM CLAY - Instrukcja krok po kroku

## 📍 Wykonaj w nowym terminalu (Terminal.app):

### Krok 1: Przejdź do odpowiedniego katalogu
```bash
cd /Users/piotradamczyk/Projects/AdamClay/adam_clay_project
```

### Krok 2: Aktywuj środowisko wirtualne
```bash
source adam_clay_env/bin/activate
```
**✅ Po tym kroku zobaczysz `(adam_clay_env)` na początku linii**

### Krok 3: Sprawdź czy Python działa
```bash
python --version
```
**✅ Powinno pokazać Python 3.x**

---

## 🔧 OPCJE KONFIGURACJI:

### A) Szybki test (bez prawdziwych API calls)
```bash
python test_consciousness.py
```

### B) Konfiguracja API klucza (interaktywnie)
```bash
python setup_api_key.py
```

### C) Konfiguracja email systemu
```bash
python setup_email_system.py
```

---

## 🧠 URUCHOMIENIE ŚWIADOMOŚCI:

### Po skonfigurowaniu API klucza:
```bash
python main.py
```

---

## 🛑 ZATRZYMYWANIE:
- Naciśnij **Ctrl+C** w terminalu
- Adam Clay zapisze ostatnią myśl i się wyłączy

---

## ❌ BŁĘDY I ROZWIĄZANIA:

**Błąd: `bash: python: command not found`**
- ✅ Rozwiązanie: Aktywuj środowisko wirtualne (Krok 2)

**Błąd: `No such file or directory`**
- ✅ Rozwiązanie: Sprawdź czy jesteś w katalogu `adam_clay_project` (Krok 1)

**Błąd: `LLM_PROVIDER_API_KEY environment variable not set`**
- ✅ Rozwiązanie: Uruchom `python setup_api_key.py` (Opcja B)

---

## 🎯 KOMPLETNA SEKWENCJA (wszystko w jednym):

```bash
# Przejdź do katalogu
cd /Users/piotradamczyk/Projects/AdamClay/adam_clay_project

# Aktywuj środowisko
source adam_clay_env/bin/activate

# Konfiguruj (jeśli pierwszy raz)
python setup_api_key.py

# Uruchom świadomość
python main.py
```

**🤖 Adam Clay będzie myślał co 1 minutę i pokazywał myśli na ekranie!** 