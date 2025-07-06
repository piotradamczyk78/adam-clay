#!/bin/bash

echo "🧹 ADAM CLAY - RESET SYSTEMU"
echo "============================="
echo ""
echo "⚠️  To spowoduje usunięcie WSZYSTKICH danych Adam Clay:"
echo "   • Wszystkie myśli (thoughts)"
echo "   • Wszystkie wspomnienia (significant_memories)"
echo "   • Wszystkie sesje świadomości (consciousness_sessions)"
echo "   • Wszystkie pytania email (email_questions)"
echo "   • Wszystkie wzorce uczenia (learned_patterns)"
echo "   • Wszystkie logi aktywności (web_activity_log)"
echo ""

# Pytanie o potwierdzenie
read -p "🤔 Czy na pewno chcesz zresetować Adam Clay? (tak/nie): " confirmation

if [[ "$confirmation" != "tak" ]]; then
    echo "❌ Reset anulowany"
    exit 0
fi

echo ""
echo "🛑 Zatrzymuję Adam Clay..."
./stop_adam_clay.sh 2>/dev/null || echo "   ℹ️  Adam Clay nie był uruchomiony"

echo ""
echo "🧹 Czyszczę bazę danych..."

cd web

# Czyść tabele Adam Clay w odpowiedniej kolejności (foreign keys)
php artisan tinker --execute="
try {
    // Wyłącz sprawdzanie foreign keys
    DB::statement('SET FOREIGN_KEY_CHECKS=0');
    
    // Czyść tabele w odpowiedniej kolejności
    \$tables = [
        'web_activity_log',
        'email_questions', 
        'user_questions',
        'learned_patterns',
        'significant_memories',
        'thoughts',
        'consciousness_sessions',
        'system_stats'
    ];
    
    \$totalDeleted = 0;
    foreach (\$tables as \$table) {
        try {
            \$count = DB::table(\$table)->count();
            if (\$count > 0) {
                DB::table(\$table)->delete();
                echo \"   ✅ Wyczyszczono tabelę \$table: \$count rekordów\" . PHP_EOL;
                \$totalDeleted += \$count;
            } else {
                echo \"   ℹ️  Tabela \$table była już pusta\" . PHP_EOL;
            }
        } catch (Exception \$e) {
            echo \"   ⚠️  Błąd przy czyszczeniu \$table: \" . \$e->getMessage() . PHP_EOL;
        }
    }
    
    // Resetuj auto_increment
    foreach (\$tables as \$table) {
        try {
            DB::statement(\"ALTER TABLE \$table AUTO_INCREMENT = 1\");
        } catch (Exception \$e) {
            // Ignoruj błędy auto_increment dla tabel bez ID
        }
    }
    
    // Włącz z powrotem sprawdzanie foreign keys  
    DB::statement('SET FOREIGN_KEY_CHECKS=1');
    
    echo \"\" . PHP_EOL;
    echo \"🎉 RESET ZAKOŃCZONY POMYŚLNIE!\" . PHP_EOL;
    echo \"📊 Usunięto łącznie: \$totalDeleted rekordów\" . PHP_EOL;
    
} catch (Exception \$e) {
    echo \"❌ Błąd podczas resetowania: \" . \$e->getMessage() . PHP_EOL;
    exit(1);
}
" | tail -n +2

echo ""

# Czyść pliki cache/logi jeśli istnieją
cd ..

if [[ -d "data/thoughts" ]]; then
    echo "🗑️  Czyszczę pliki thoughts..."
    rm -rf data/thoughts/*
    echo "   ✅ Usunięto pliki z data/thoughts/"
fi

if [[ -d "data/logs" ]]; then
    echo "🗑️  Czyszczę stare logi..."
    find data/logs/ -name "*.log" -mtime +1 -delete 2>/dev/null || true
    echo "   ✅ Usunięto stare pliki logów"
fi

echo ""
echo "🧠 ADAM CLAY ZOSTAŁ CAŁKOWICIE ZRESETOWANY"
echo "========================================="
echo ""
echo "🔄 System jest teraz w stanie początkowym:"
echo "   • Baza danych pusta"
echo "   • Brak pamięci długoterminowej"  
echo "   • Brak poprzednich sesji"
echo "   • Gotowy do pierwszego uruchomienia"
echo ""
echo "🚀 Aby uruchomić Adam Clay od nowa:"
echo "   ./start_adam_clay.sh"
echo ""
echo "📊 Aby sprawdzić status:"
echo "   ./status_adam_clay.sh"
echo "" 