#!/bin/bash

# 🌐 Adam Clay - Friendly Domain Setup Script
# Konfiguruje adamclay.local jako lokalny adres dashboard

echo "🌐 ADAM CLAY - FRIENDLY DOMAIN SETUP"
echo "=================================="

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script is designed for macOS"
    exit 1
fi

# Check if already configured
if grep -q "adamclay.local" /etc/hosts; then
    echo "✅ adamclay.local już skonfigurowane w /etc/hosts"
else
    echo "📝 Dodaję adamclay.local do /etc/hosts..."
    echo "127.0.0.1 adamclay.local" | sudo tee -a /etc/hosts > /dev/null
    echo "✅ adamclay.local dodane do /etc/hosts"
fi

# Show current Laravel server status
echo ""
echo "🔍 Sprawdzam status serwera Laravel..."
if lsof -i :8004 > /dev/null 2>&1; then
    echo "✅ Laravel server działa na porcie 8004"
    
    # Test the new domain
    echo ""
    echo "🧪 Testuje połączenie z adamclay.local:8004..."
    if curl -s "http://adamclay.local:8004/api/hello" > /dev/null 2>&1; then
        echo "✅ adamclay.local:8004/api/hello - OK"
    else
        echo "❌ Nie można połączyć się z adamclay.local:8004"
    fi
    
else
    echo "⚠️ Laravel server nie działa na porcie 8004"
    echo "Uruchom: php artisan serve --port=8004"
fi

echo ""
echo "🎉 KONFIGURACJA ZAKOŃCZONA!"
echo ""
echo "🌐 Dostępne adresy Adam Clay Dashboard:"
echo "   • http://adamclay.local:8004 (główny)"
echo "   • http://adamclay.local:8004/dashboard"
echo "   • http://adamclay.local:8004/console"
echo "   • http://adamclay.local:8004/monitor"
echo "   • http://adamclay.local:8004/consciousness"
echo ""
echo "🔌 API Endpoint:"
echo "   • http://adamclay.local:8004/api/"
echo ""
echo "💡 Tip: Dodaj bookmark do adamclay.local:8004 w przeglądarce!"

# Optional: Try to open in browser
if command -v open > /dev/null 2>&1; then
    echo ""
    read -p "🌐 Otworzyć dashboard w przeglądarce? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open "http://adamclay.local:8004"
        echo "🚀 Dashboard otwarty w przeglądarce!"
    fi
fi 