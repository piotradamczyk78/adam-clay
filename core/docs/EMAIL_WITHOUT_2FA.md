# 📧 Email BEZ 2FA - Alternatywni Dostawcy

## 🎯 Problem z Gmail

**Gmail wymusza weryfikację dwuetapową (2FA)** od maja 2022. Google wyłączył opcję "Less secure apps", więc wszystkie aplikacje trzecie muszą używać App Passwords.

**⚠️ To oznacza:** Gmail = 2FA obowiązkowe

## ✅ Rozwiązania BEZ 2FA

### 📨 1. OUTLOOK.COM / HOTMAIL (NAJLEPSZE)

**Zalety:**
- ✅ **BEZ weryfikacji dwuetapowej**
- ✅ Wystarczy zwykłe hasło konta
- ✅ Darmowe konto Microsoft
- ✅ Niezawodny SMTP/IMAP
- ✅ Dobra reputacja emailowa

**Konfiguracja:**
```
1. Utwórz konto: https://outlook.com
2. Email: adam.clay.ai@outlook.com
3. Użyj zwykłego hasła konta (nie App Password!)

SMTP: smtp-mail.outlook.com:587
IMAP: outlook.office365.com:993
```

**Uruchom:** `python setup_simple_email.py` → opcja 1

---

### 📬 2. YAHOO MAIL (DRUGIE MIEJSCE)

**Zalety:**
- ✅ Opcja "Less secure app access" nadal dostępna
- ✅ Może działać bez 2FA
- ✅ Darmowe konto

**Uwagi:**
- ⚠️ Yahoo może wymagać App Password w przyszłości
- ⚠️ Mniej niezawodny niż Outlook

**Konfiguracja:**
```
1. Utwórz konto: https://mail.yahoo.com
2. Account Security → Less secure app access → ON
3. Email: adam.clay.ai@yahoo.com

SMTP: smtp.mail.yahoo.com:587
IMAP: imap.mail.yahoo.com:993
```

---

### 🛠️ 3. MAILTRAP (TYLKO TESTY)

**Zalety:**
- ✅ **TYLKO do testów** - nie wysyła prawdziwych emaili
- ✅ Webowy podgląd wszystkich emaili
- ✅ Bez 2FA, proste hasło
- ✅ Darmowy plan (100 emaili/miesiąc)

**Ograniczenia:**
- ❌ Emaile NIE docierają do odbiorców
- ❌ Tylko SMTP (bez IMAP)
- ✅ Idealne do developmentu

**Konfiguracja:**
```
1. Zarejestruj się: https://mailtrap.io
2. Email Testing → My Inbox → Show Credentials
3. Skopiuj Username i Password

SMTP: smtp.mailtrap.io:587
```

---

### 🏠 4. WŁASNY SERWER SMTP

**Dla zaawansowanych:**
- 🏢 Hostingi z SMTP (nazwa.pl, home.pl, etc.)
- 🖥️ Własny serwer mailowy
- 🧪 Lokalne serwery testowe

**Przykłady:**
```
home.pl:     smtp.home.pl:587
nazwa.pl:    smtp.nazwa.pl:587
localhost:   localhost:1025 (dla testów)
```

---

## 🚀 Szybka konfiguracja

### Opcja A: Outlook (Zalecane)
```bash
python setup_simple_email.py
# Wybierz opcję 1 (Outlook)
```

### Opcja B: Yahoo
```bash
python setup_simple_email.py
# Wybierz opcję 2 (Yahoo)
```

### Opcja C: Mailtrap (Testy)
```bash
python setup_simple_email.py
# Wybierz opcję 3 (Mailtrap)
```

---

## 📋 Porównanie dostawców

| Dostawca | 2FA? | Niezawodność | Koszt | Użycie |
|----------|------|--------------|-------|---------|
| **Gmail** | ❌ Tak | ⭐⭐⭐⭐⭐ | 🆓 | Wymaga App Password |
| **Outlook** | ✅ Nie | ⭐⭐⭐⭐⭐ | 🆓 | **NAJLEPSZE** |
| **Yahoo** | ⚠️ Opcjonalne | ⭐⭐⭐ | 🆓 | Może się zmienić |
| **Mailtrap** | ✅ Nie | ⭐⭐⭐⭐⭐ | 🆓/💰 | Tylko testy |

---

## 🔧 Konfiguracja w kodzie

Po uruchomieniu `setup_simple_email.py`, konfiguracja zostanie zapisana w `config.json`:

```json
{
  "communication": {
    "email": {
      "enabled": true,
      "from_email": "adam.clay.ai@outlook.com",
      "email_password": "twoje_haslo_outlook",
      "to_email": "twoj@email.com",
      "smtp_server": "smtp-mail.outlook.com",
      "smtp_port": 587,
      "imap_server": "outlook.office365.com",
      "imap_port": 993,
      "check_interval": 60
    }
  }
}
```

---

## 🎉 Po konfiguracji

1. **Uruchom Adam Clay:** `python main.py`
2. **System pytań działa** - wszystkie 4 priorytety
3. **Test wysyłania:** `python demo_email_questions.py`

---

## 💡 Pro Tips

### Outlook.com
- ✅ **Najlepszy wybór** - stabilny, bez 2FA
- ✅ Można użyć istniejącego konta Microsoft
- ✅ Doskonała integracja z systemami Microsoft

### Yahoo Mail
- ⚠️ Sprawdź ustawienia "Less secure apps"
- ⚠️ Yahoo może w przyszłości wymuszać 2FA

### Mailtrap
- 🧪 **Idealne do developmentu** systemu pytań
- 📧 Wszystkie emaile widoczne w panelu webowym
- ✅ Nie spamuje prawdziwej skrzynki

### Własny SMTP
- 🏢 Jeśli masz hosting email - użyj go
- 🔒 Najlepsza kontrola nad bezpieczeństwem
- ⚙️ Wymaga znajomości konfiguracji SMTP

---

## 🆘 Rozwiązywanie problemów

### "Authentication failed"
1. Sprawdź email i hasło
2. Outlook: sprawdź czy to konto Microsoft
3. Yahoo: włącz "Less secure app access"

### "Connection refused"
1. Sprawdź serwer SMTP i port
2. Firewall może blokować port 587
3. Spróbuj port 465 (SSL) zamiast 587 (TLS)

### "SSL/TLS errors"
1. Zaktualizuj Python (SSL certificates)
2. Sprawdź czy STARTTLS jest obsługiwane

---

**🚀 Adam Clay jest gotowy do komunikacji bez 2FA!** 