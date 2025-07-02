# 🔑 Adam Clay API Setup Guide

## Opcja 1: Oficjalny klucz LLM provider API

### Krok 1: Rejestracja w LLM provider
1. Idź na https://console.llm-provider.com/
2. Kliknij "Sign Up" lub "Log In"
3. Zarejestruj się używając email (może wymagać weryfikacji)

### Krok 2: Utworzenie klucza API
1. Po zalogowaniu, przejdź do sekcji "API Keys"
2. Kliknij "Create Key" lub "Generate API Key"
3. Nadaj nazwę kluczu, np. "Adam Clay Consciousness"
4. Skopiuj klucz (będzie wyglądał jak: `sk-ant-api03-...`)

### Krok 3: Konfiguracja środowiska
```bash
# Tymczasowo (tylko dla tej sesji)
export LLM_PROVIDER_API_KEY="replace-meój-klucz-tutaj"

# Trwale (dodaj do ~/.bashrc lub ~/.zshrc)
echo 'export LLM_PROVIDER_API_KEY="replace-meój-klucz-tutaj"' >> ~/.bashrc
source ~/.bashrc
```

### Krok 4: Weryfikacja
```bash
cd adam_clay_project
python -c "
import os
key = os.getenv('LLM_PROVIDER_API_KEY')
if key:
    print(f'✅ Klucz ustawiony: {key[:10]}...')
else:
    print('❌ Brak klucza API')
"
```

### 💰 Koszty LLM provider API (Stan na 2024)
- **LLM 3.5 Sonnet**: ~$3-15 za 1M tokenów
- **Typowy koszt Adam Clay**: ~$0.001-0.01 za myśl
- **Dzienny budżet 100 myśli**: ~$0.10-1.00
- **Miesięczny koszt**: ~$3-30

---

## Opcja 2: Wykorzystanie połączenia IDE (EKSPERYMENTALNA)

### 🤔 Analiza możliwości

IDE rzeczywiście ma już połączenie z LLM, ale:
- **Klucz API**: IDE używa swojego klucza (nie mamy do niego dostępu)
- **Rate limiting**: IDE ma własne limity użytkowania
- **Kontrola**: Brak pełnej kontroli nad requestami

### 🛠️ Możliwe rozwiązania

#### A) Proxy przez VS Code API (gdyby było dostępne)
```typescript
// Hipotetyczny kod - sprawdzić czy IDE udostępnia API
const vscode = require('vscode');
const ideExtension = vscode.extensions.getExtension('ide.ai');
```

#### B) Local proxy server
Stworzyć lokalny serwer, który:
1. Przyjmuje requesty od Adam Clay
2. Przekazuje je przez IDE
3. Zwraca odpowiedzi

#### C) Intercepting IDE requests
Przechwytywanie requestów IDE do analizy endpointów.

---

## 🚀 Zalecane podejście

### Faza 1: Start z oficjalnym API
```bash
# Szybki start
export LLM_PROVIDER_API_KEY="your-key"
make consciousness
```

### Faza 2: Zbadanie integracji z IDE
```bash
# Stworzyć eksperymentalny adapter
python create_ide_adapter.py
```

---

## 💡 IDE Integration Research

### Sprawdzenie czy IDE udostępnia API
```bash
# Sprawdź procesy IDE
ps aux | grep ide

# Sprawdź połączenia sieciowe
lsof -i | grep ide

# Sprawdź konfigurację IDE
ls ~/.ide-tutor/ || ls ~/.config/ide/
```

### Potencjalne endpointy
- `https://api.ide.sh/` (spekulacja)
- Local proxy: `http://localhost:xxxx/`
- VS Code extension API

---

## ⚡ Quick Start dla Adam Clay

### Opcja A: Oficjalny klucz (5 minut)
1. console.llm-provider.com → Create API Key
2. `export LLM_PROVIDER_API_KEY="klucz"`
3. `make consciousness`

### Opcja B: IDE research (30-60 minut)
1. Zbadać jak IDE komunikuje się z LLM
2. Stworzyć adapter/proxy
3. Zmodyfikować api_client.py

---

## 🔬 Eksperyment: IDE API Discovery

Czy chcesz, żebym stworzył skrypt do zbadania możliwości integracji z IDE?
Mogłbym sprawdzić:
- Jakie połączenia sieciowe robi IDE
- Czy są dostępne jakieś lokalne API endpointy
- Strukturę komunikacji z LLM

To mogłoby otworzyć fascynującą możliwość Adam Clay wykorzystującego to samo połączenie, które już masz w IDE! 🤯 