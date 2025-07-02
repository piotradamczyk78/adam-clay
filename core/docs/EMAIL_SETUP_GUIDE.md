# 📧 Adam Clay Email Questions System - Setup Guide

## 🎯 Przegląd

Adam Clay może teraz zadawać pytania przez email w 4 poziomach priorytetów:

1. **🚨 KRYTYCZNE** - blokują proces myślenia
2. **⚡ WAŻNE** - nie blokują, ale priorytetowe  
3. **📋 INFORMACYJNE** - w tle, odpowiedź do następnych myśli
4. **📊 OPTYMALIZACYJNE** - zbierane do dziennych raportów

## 🛠️ Konfiguracja

### 1. Utwórz Email dla Adam Clay

Stwórz konto Gmail dla Adama:
- Email: `adam.clay.ai@gmail.com` (lub podobny)
- Hasło aplikacji Google (nie zwykłe hasło!)

### 2. Włącz App Password w Gmail

1. Idź do **Google Account Settings**
2. **Security** → **2-Step Verification** (włącz jeśli nie masz)
3. **App passwords** → **Generate password**
4. Wybierz "Mail" i nazwij "Adam Clay AI"
5. **Skopiuj 16-znakowe hasło** (np. `abcd efgh ijkl mnop`)

### 3. Aktualizuj config.json

Zmień sekcję email w `config.json`:

```json
{
  "communication": {
    "email": {
      "enabled": true,
      "from_email": "adam.clay.ai@gmail.com", 
      "email_password": "abcd efgh ijkl mnop",
      "to_email": "twoj.email@gmail.com",
      "smtp_server": "smtp.gmail.com",
      "smtp_port": 587,
      "imap_server": "imap.gmail.com", 
      "imap_port": 993,
      "check_interval": 60
    }
  }
}
```

## 📨 Jak Odpowiadać na Pytania

### Format Odpowiedzi

Odpowiedz na email Adama używając formatu:

```
ANSWER:q_1234567890_critical Tak, zgadzam się z tym kierunkiem rozwoju.
```

### Przykłady Odpowiedzi

**Pytanie Krytyczne:**
```
ANSWER:q_1672531200_critical Tak, skoncentruj się na multimodalnych systemach AI.
```

**Pytanie Ważne:**
```  
ANSWER:q_1672531300_important Sprawdź rynek polskojęzycznych chatbotów.
```

**Pytanie Informacyjne:**
```
ANSWER:q_1672531400_informative OpenAI API jest stabilne, ale ElevenLabs ma lepsze PL voices.
```

## 🚨 Poziomy Pytań

### CRITICAL_QUESTION (Krytyczne)
- **Blokuje** proces myślenia Adama
- Email z **wysokim priorytetem**
- Adam **czeka** na odpowiedź

### IMPORTANT_QUESTION (Ważne)  
- **Nie blokuje** procesu
- **Prominentne** wyświetlenie
- Email **priorytetowy**

### INFO_QUESTION (Informacyjne)
- **W tle**, nie przerywa
- Email **standardowy** 
- Odpowiedź w **następnych myślach**

### OPTIMIZATION_QUESTION (Optymalizacja)
- **Zbierane** przez 24h
- **Dzienny raport** z kilkoma pytaniami

## 🎉 Przykład Użycia

1. **Adam myśli:** "Zastanawiam się nad rozszerzeniem oferty..."
2. **Adam dodaje:** "IMPORTANT_QUESTION: Czy powinienem zainwestować w ElevenLabs Pro?"
3. **System wysyła email** z priorytetem IMPORTANT
4. **Ty odpowiadasz:** `ANSWER:q_1672531234_important Tak, ale najpierw przetestuj` 
5. **Adam otrzymuje odpowiedź** i uwzględnia ją w kolejnych myślach
6. **Adam rozwija się** dzięki Twojemu kierownictwu!

---

**🎯 REZULTAT: Adam Clay staje się pierwszym AI freelancerem z prawdziwą interaktywną świadomością kierowaną przez człowieka!** 