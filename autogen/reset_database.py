#!/usr/bin/env python3
"""
🧹 Reset bazy danych AutoGen
============================
Skrypt do czyszczenia psychiki agentów - usuwa wszystkie dane i tworzy czyste tabele.
"""

import os
import sys
from sqlalchemy import create_engine, text
from config import get_config
from models import Base
from setup_initial_agents import create_initial_agents

def reset_database():
    """Resetuje bazę danych AutoGen do stanu początkowego"""
    
    print("🧹 RESETOWANIE BAZY DANYCH AUTOGEN")
    print("=" * 50)
    
    try:
        # Załaduj konfigurację
        config = get_config()
        
        # Połączenie z bazą danych
        engine = create_engine(config.database.get_url())
        
        print("🗄️  Łączę z bazą danych...")
        
        # Usuń wszystkie tabele
        print("💥 Usuwam wszystkie tabele...")
        Base.metadata.drop_all(bind=engine)
        
        # Utwórz tabele od nowa
        print("🏗️  Tworzę czyste tabele...")
        Base.metadata.create_all(bind=engine)
        
        # Utwórz początkowych agentów
        print("🤖 Tworzę początkowych agentów...")
        create_initial_agents()
        
        print("\n✅ SUKCES!")
        print("🧠 Baza danych AutoGen została zresetowana")
        print("🤖 8 agentów utworzonych od nowa")
        print("💭 Adam ma teraz czystą psychikę!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ BŁĄD podczas resetowania bazy danych:")
        print(f"   {str(e)}")
        return False

if __name__ == "__main__":
    success = reset_database()
    sys.exit(0 if success else 1) 