"""
Advanced Budget Manager for Adam Clay Eden
Zaawansowany manager budżetu z systemem dopaminowym i limitami kosztów
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, asdict
import sqlite3
from pathlib import Path

@dataclass
class UsageRecord:
    """Rekord użycia API"""
    timestamp: str
    request_type: str  # 'anthropic', 'slack', 'other'
    cost: float
    tokens_used: int
    success: bool
    agent_triggered: str = ""
    mood_level: float = 0.0
    dopamine_level: float = 0.0

class BudgetManager:
    """Manager budżetu z systemem dopaminowym"""
    
    def __init__(self, config, db_path: str = "data/budget.db"):
        self.config = config
        self.db_path = db_path
        self.ensure_database()
        
        # Cache dla optymalizacji
        self._daily_cache = {}
        self._last_cache_update = None
    
    def ensure_database(self):
        """Upewnij się że baza danych istnieje"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS usage_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    request_type TEXT NOT NULL,
                    cost REAL NOT NULL,
                    tokens_used INTEGER DEFAULT 0,
                    success BOOLEAN NOT NULL,
                    agent_triggered TEXT DEFAULT '',
                    mood_level REAL DEFAULT 0.0,
                    dopamine_level REAL DEFAULT 0.0,
                    metadata TEXT DEFAULT '{}'
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS daily_summaries (
                    date TEXT PRIMARY KEY,
                    total_cost REAL NOT NULL,
                    total_requests INTEGER NOT NULL,
                    successful_requests INTEGER NOT NULL,
                    avg_mood REAL DEFAULT 0.0,
                    avg_dopamine REAL DEFAULT 0.0,
                    dominant_agents TEXT DEFAULT '[]'
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON usage_records(timestamp);
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_date ON daily_summaries(date);
            """)
    
    def record_usage(self, request_type: str, cost: float, tokens_used: int = 0, 
                    success: bool = True, agent_triggered: str = "") -> bool:
        """Zapisz użycie API"""
        
        # Sprawdź limity PRZED zapisaniem
        if not self.check_budget_limits(cost):
            return False
        
        record = UsageRecord(
            timestamp=datetime.now().isoformat(),
            request_type=request_type,
            cost=cost,
            tokens_used=tokens_used,
            success=success,
            agent_triggered=agent_triggered,
            mood_level=self._get_current_mood_score(),
            dopamine_level=self.config.dopamine.current_level
        )
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO usage_records 
                    (timestamp, request_type, cost, tokens_used, success, 
                     agent_triggered, mood_level, dopamine_level)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    record.timestamp, record.request_type, record.cost,
                    record.tokens_used, record.success, record.agent_triggered,
                    record.mood_level, record.dopamine_level
                ))
            
            # Aktualizuj cache
            self._invalidate_cache()
            
            # Aktualizuj dzienne podsumowanie
            self._update_daily_summary()
            
            return True
            
        except Exception as e:
            print(f"❌ Błąd zapisywania budżetu: {e}")
            return False
    
    def check_budget_limits(self, additional_cost: float = 0.0) -> bool:
        """Sprawdź czy można wykonać request w ramach budżetu"""
        current_usage = self.get_current_usage()
        
        # Sprawdź dzienny limit
        if (current_usage['daily_cost'] + additional_cost) > self.config.economic.daily_budget_limit:
            print(f"⚠️ Przekroczony dzienny limit budżetu: ${current_usage['daily_cost']:.2f} + ${additional_cost:.2f} > ${self.config.economic.daily_budget_limit:.2f}")
            return False
        
        # Sprawdź liczba requestów
        if current_usage['daily_requests'] >= self.config.economic.max_daily_requests:
            print(f"⚠️ Przekroczony dzienny limit requestów: {current_usage['daily_requests']} >= {self.config.economic.max_daily_requests}")
            return False
        
        # Sprawdź godzinny limit requestów
        if current_usage['hourly_requests'] >= self.config.economic.max_hourly_requests:
            print(f"⚠️ Przekroczony godzinny limit requestów: {current_usage['hourly_requests']} >= {self.config.economic.max_hourly_requests}")
            return False
        
        return True
    
    def get_current_usage(self) -> Dict:
        """Pobierz aktualne użycie budżetu"""
        if self._should_use_cache():
            return self._daily_cache
        
        today = datetime.now().date().isoformat()
        hour_ago = (datetime.now() - timedelta(hours=1)).isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Dzienne statystyki
            daily_stats = conn.execute("""
                SELECT 
                    COALESCE(SUM(cost), 0) as daily_cost,
                    COUNT(*) as daily_requests,
                    COUNT(CASE WHEN success = 1 THEN 1 END) as successful_requests,
                    AVG(mood_level) as avg_mood,
                    AVG(dopamine_level) as avg_dopamine
                FROM usage_records 
                WHERE DATE(timestamp) = ?
            """, (today,)).fetchone()
            
            # Godzinne statystyki
            hourly_stats = conn.execute("""
                SELECT COUNT(*) as hourly_requests
                FROM usage_records 
                WHERE timestamp >= ?
            """, (hour_ago,)).fetchone()
            
            result = {
                'daily_cost': daily_stats['daily_cost'] or 0.0,
                'daily_requests': daily_stats['daily_requests'] or 0,
                'hourly_requests': hourly_stats['hourly_requests'] or 0,
                'successful_requests': daily_stats['successful_requests'] or 0,
                'avg_mood': daily_stats['avg_mood'] or 0.0,
                'avg_dopamine': daily_stats['avg_dopamine'] or 0.0,
                'budget_used_percent': (daily_stats['daily_cost'] or 0.0) / self.config.economic.daily_budget_limit * 100,
                'requests_used_percent': (daily_stats['daily_requests'] or 0) / self.config.economic.max_daily_requests * 100
            }
        
        # Cache wyników
        self._daily_cache = result
        self._last_cache_update = datetime.now()
        
        return result
    
    def should_enter_economy_mode(self) -> bool:
        """Sprawdź czy powinniśmy wejść w tryb oszczędnościowy"""
        usage = self.get_current_usage()
        
        budget_threshold = self.config.economic.economy_mode_threshold
        
        return (usage['budget_used_percent'] / 100) >= budget_threshold
    
    def get_request_frequency_multiplier(self) -> float:
        """Pobierz mnożnik częstotliwości requestów na podstawie dopaminy"""
        dopamine_normalized = self.config.dopamine.current_level / 100.0
        
        if dopamine_normalized > 0.8:
            return self.config.dopamine.high_dopamine_multiplier
        elif dopamine_normalized < 0.3:
            return self.config.dopamine.low_dopamine_multiplier
        else:
            # Liniowa interpolacja między 0.3 a 0.8
            if dopamine_normalized < 0.55:  # Środek
                factor = (dopamine_normalized - 0.3) / (0.55 - 0.3)
                return self.config.dopamine.low_dopamine_multiplier + factor * (1.0 - self.config.dopamine.low_dopamine_multiplier)
            else:
                factor = (dopamine_normalized - 0.55) / (0.8 - 0.55)
                return 1.0 + factor * (self.config.dopamine.high_dopamine_multiplier - 1.0)
    
    def get_budget_status(self) -> Dict:
        """Pobierz pełny status budżetu"""
        usage = self.get_current_usage()
        
        # Określ status
        if usage['budget_used_percent'] >= 95:
            status = "EMERGENCY"
            color = "🔴"
        elif usage['budget_used_percent'] >= 80:
            status = "WARNING"
            color = "🟡"
        elif usage['budget_used_percent'] >= 70:
            status = "ECONOMY"
            color = "🟠"
        else:
            status = "NORMAL"
            color = "🟢"
        
        return {
            'status': status,
            'color': color,
            'usage': usage,
            'remaining_budget': self.config.economic.daily_budget_limit - usage['daily_cost'],
            'remaining_requests': self.config.economic.max_daily_requests - usage['daily_requests'],
            'economy_mode': self.should_enter_economy_mode(),
            'dopamine_multiplier': self.get_request_frequency_multiplier()
        }
    
    def get_weekly_summary(self) -> Dict:
        """Pobierz podsumowanie tygodniowe"""
        week_ago = (datetime.now() - timedelta(days=7)).date().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            summary = conn.execute("""
                SELECT 
                    COALESCE(SUM(cost), 0) as total_cost,
                    COUNT(*) as total_requests,
                    COUNT(CASE WHEN success = 1 THEN 1 END) as successful_requests,
                    AVG(mood_level) as avg_mood,
                    AVG(dopamine_level) as avg_dopamine,
                    COUNT(DISTINCT DATE(timestamp)) as active_days
                FROM usage_records 
                WHERE DATE(timestamp) >= ?
            """, (week_ago,)).fetchone()
            
            # Najaktywniejsze agenty
            agents = conn.execute("""
                SELECT agent_triggered, COUNT(*) as count
                FROM usage_records 
                WHERE DATE(timestamp) >= ? AND agent_triggered != ''
                GROUP BY agent_triggered
                ORDER BY count DESC
                LIMIT 5
            """, (week_ago,)).fetchall()
        
        return {
            'total_cost': summary['total_cost'] or 0.0,
            'total_requests': summary['total_requests'] or 0,
            'successful_requests': summary['successful_requests'] or 0,
            'success_rate': (summary['successful_requests'] or 0) / max(summary['total_requests'] or 1, 1) * 100,
            'avg_mood': summary['avg_mood'] or 0.0,
            'avg_dopamine': summary['avg_dopamine'] or 0.0,
            'active_days': summary['active_days'] or 0,
            'top_agents': [{'agent': row['agent_triggered'], 'count': row['count']} for row in agents],
            'weekly_budget_used_percent': (summary['total_cost'] or 0.0) / self.config.economic.weekly_budget_limit * 100
        }
    
    def estimate_request_cost(self, request_type: str, tokens: int = 1000) -> float:
        """Oszacuj koszt requesta"""
        if request_type == 'anthropic':
            # Claude-3.5-Sonnet pricing (orientacyjnie)
            input_cost_per_1k = 0.003  # $3 per 1M tokens
            output_cost_per_1k = 0.015  # $15 per 1M tokens
            
            # Szacujemy 70% input, 30% output
            estimated_cost = (tokens * 0.7 * input_cost_per_1k / 1000) + (tokens * 0.3 * output_cost_per_1k / 1000)
            return estimated_cost
        elif request_type == 'slack':
            return 0.0  # Slack API jest darmowe w podstawowym zakresie
        else:
            return self.config.economic.cost_per_request
    
    def _get_current_mood_score(self) -> float:
        """Oblicz aktualny wynik nastroju"""
        mood = self.config.mood
        return (mood.happiness + mood.energy + mood.focus + mood.excitement + mood.curiosity) / 5
    
    def _should_use_cache(self) -> bool:
        """Sprawdź czy można użyć cache"""
        if not self._last_cache_update:
            return False
        
        # Cache jest ważny przez 5 minut
        return (datetime.now() - self._last_cache_update).seconds < 300
    
    def _invalidate_cache(self):
        """Unieważnij cache"""
        self._daily_cache = {}
        self._last_cache_update = None
    
    def _update_daily_summary(self):
        """Aktualizuj dzienne podsumowanie"""
        today = datetime.now().date().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            # Pobierz statystyki dnia
            stats = conn.execute("""
                SELECT 
                    COALESCE(SUM(cost), 0) as total_cost,
                    COUNT(*) as total_requests,
                    COUNT(CASE WHEN success = 1 THEN 1 END) as successful_requests,
                    AVG(mood_level) as avg_mood,
                    AVG(dopamine_level) as avg_dopamine
                FROM usage_records 
                WHERE DATE(timestamp) = ?
            """, (today,)).fetchone()
            
            # Najaktywniejsze agenty
            agents = conn.execute("""
                SELECT agent_triggered, COUNT(*) as count
                FROM usage_records 
                WHERE DATE(timestamp) = ? AND agent_triggered != ''
                GROUP BY agent_triggered
                ORDER BY count DESC
                LIMIT 3
            """, (today,)).fetchall()
            
            dominant_agents = json.dumps([row[0] for row in agents])
            
            # Upsert dziennego podsumowania
            conn.execute("""
                INSERT OR REPLACE INTO daily_summaries 
                (date, total_cost, total_requests, successful_requests, 
                 avg_mood, avg_dopamine, dominant_agents)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                today, stats[0], stats[1], stats[2],
                stats[3] or 0.0, stats[4] or 0.0, dominant_agents
            ))
    
    def get_cost_prediction(self) -> Dict:
        """Przewiduj koszty na podstawie obecnego trendu"""
        usage = self.get_current_usage()
        current_hour = datetime.now().hour
        
        if current_hour == 0:
            current_hour = 1  # Unikaj dzielenia przez zero
        
        # Przewidywanie na podstawie obecnego użycia
        hourly_rate = usage['daily_cost'] / current_hour
        predicted_daily = hourly_rate * 24
        
        # Uwzględnij mnożnik dopaminy
        dopamine_multiplier = self.get_request_frequency_multiplier()
        adjusted_prediction = predicted_daily * dopamine_multiplier
        
        return {
            'current_hourly_rate': hourly_rate,
            'predicted_daily_cost': predicted_daily,
            'adjusted_prediction': adjusted_prediction,
            'dopamine_multiplier': dopamine_multiplier,
            'will_exceed_budget': adjusted_prediction > self.config.economic.daily_budget_limit,
            'budget_risk_level': min(adjusted_prediction / self.config.economic.daily_budget_limit, 2.0)
        }
    
    def export_usage_data(self, days: int = 30) -> str:
        """Eksportuj dane użycia do JSON"""
        start_date = (datetime.now() - timedelta(days=days)).date().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            records = conn.execute("""
                SELECT * FROM usage_records 
                WHERE DATE(timestamp) >= ?
                ORDER BY timestamp DESC
            """, (start_date,)).fetchall()
            
            summaries = conn.execute("""
                SELECT * FROM daily_summaries 
                WHERE date >= ?
                ORDER BY date DESC
            """, (start_date,)).fetchall()
        
        export_data = {
            'export_date': datetime.now().isoformat(),
            'days_exported': days,
            'records': [dict(row) for row in records],
            'daily_summaries': [dict(row) for row in summaries],
            'total_records': len(records)
        }
        
        return json.dumps(export_data, indent=2, ensure_ascii=False) 