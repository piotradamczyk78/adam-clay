# 📧 Gmail App Password - Instrukcje PL (2024)

## 🔐 Krok po kroku - Polska wersja Gmail:

### **Krok 1: Przejdź do ustawień konta Google**
```
https://myaccount.google.com/
```
**Lub:** Gmail → ikona profilu (prawy górny róg) → "Zarządzaj kontem Google"

### **Krok 2: Sekcja Bezpieczeństwo**
- Kliknij **"Bezpieczeństwo"** w menu po lewej stronie
- Przewiń w dół do sekcji **"Logowanie w Google"**

### **Krok 3: Włącz weryfikację dwuetapową**
- Znajdź **"Weryfikacja dwuetapowa"** 
- Jeśli jest wyłączona, kliknij **"Włącz"**
- Postępuj zgodnie z instrukcjami (SMS, aplikacja, etc.)

### **Krok 4: Znajdź hasła aplikacji**
- **PO WŁĄCZENIU** weryfikacji dwuetapowej
- W sekcji **"Logowanie w Google"** pojawi się nowa opcja
- Kliknij **"Hasła aplikacji"** lub **"App passwords"**

### **Krok 5: Generuj hasło dla Adam Clay**
- Kliknij **"Wybierz aplikację"** → **"Poczta"** 
- Kliknij **"Wybierz urządzenie"** → **"Inne (nazwa niestandardowa)"**
- Wpisz: **"Adam Clay AI"**
- Kliknij **"Generuj"**

### **Krok 6: Skopiuj hasło**
- Google pokaże 16-znakowe hasło: `abcd efgh ijkl mnop`
- **SKOPIUJ to hasło** (nie będzie więcej widoczne!)
- Użyj go w konfiguracji Adam Clay

---

## 🔄 Alternatywne ścieżki w polskiej wersji:

### **Jeśli nie widzisz "Hasła aplikacji":**
1. **Sprawdź weryfikację dwuetapową** - musi być włączona
2. **Poczekaj 10-15 minut** po włączeniu 2FA
3. **Odśwież stronę** myaccount.google.com
4. **Sprawdź w sekcji:** "Jak logujesz się w Google"

### **Jeśli masz problemy z dostępem:**
1. Użyj **trybu incognito** w przeglądarce
2. Wyloguj się i zaloguj ponownie do Gmail
3. Sprawdź czy masz **uprawnienia administratora** (jeśli konto firmowe)

---

## 📱 Mobilna wersja (jeśli korzystasz z telefonu):

1. **Aplikacja Gmail** → **Menu ☰** → **Ustawienia**
2. **Wybierz swoje konto** → **Zarządzaj kontem Google**
3. **Bezpieczeństwo** → **Weryfikacja dwuetapowa**
4. **Hasła aplikacji** (po włączeniu 2FA)

---

## ⚠️ Możliwe problemy i rozwiązania:

### **"Nie widzę opcji Hasła aplikacji"**
- ✅ Włącz weryfikację dwuetapową i poczekaj 15 minut
- ✅ Sprawdź czy to konto osobiste (nie firmowe z ograniczeniami)

### **"Hasło nie działa"**
- ✅ Sprawdź czy skopiowałeś **całe hasło** (16 znaków)
- ✅ Usuń spacje między grupami liter
- ✅ Wygeneruj **nowe hasło** (stare mogło wygasnąć)

### **"Konto firmowe/szkolne"**
- ✅ Administrator może **blokować hasła aplikacji**
- ✅ Skontaktuj się z IT/administratorem
- ✅ Użyj **konta osobistego Gmail** dla Adam Clay

---

## 🎯 Szybka weryfikacja:

**Sprawdź czy wszystko gotowe:**
- ✅ Masz konto Gmail (osobiste, nie firmowe)
- ✅ Weryfikacja dwuetapowa włączona
- ✅ Hasło aplikacji wygenerowane (16 znaków)
- ✅ Email `adam.clay@gmail.com` istnieje LUB zmienisz w config

---

## 💡 Pro tip:
Jeśli nie chcesz tworzyć konta `adam.clay@gmail.com`, możesz:
1. Użyć **swojego obecnego Gmail**
2. Zmienić w config.json: `"from_email": "twoj@gmail.com"`
3. Adam Clay będzie wysyłał emaile **ze swojego konta do siebie** 