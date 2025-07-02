"""
🗄️ Database Models for Adam Clay

Zarządza wszystkimi danymi Adam Clay w bazie MySQL:
- Myśli i wspomnienia
- Pytania email i odpowiedzi
- Sesje świadomości  
- Statystyki i logi aktywności
"""

import json
import uuid
from datetime import datetime, date
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, asdict
import pymysql
import pymysql.ides
from contextlib import contextmanager
import logging

@dataclass 
class DatabaseConfig:
    """Konfiguracja połączenia z bazą danych"""
    host: str = '127.0.0.1'
    port: int = 3306
    user: str = 'root'
    password: str = 'Passat377310!'
    database: str = 'adam_clay'
    charset: str = 'utf8mb4'

@dataclass
class ThoughtRecord:
    """Rekord myśli Adam Clay"""
    id: Optional[int]
    timestamp: datetime
    content: str
    thought_type: str
    cost_usd: float
    mood: Optional[str] = None
    energy_level: Optional[float] = None
    context: Optional[Dict[str, Any]] = None
    is_significant: bool = False
    session_id: Optional[str] = None
    created_at: Optional[datetime] = None

@dataclass 
class EmailQuestionRecord:
    """Rekord pytania email"""
    id: str
    content: str
    priority: str
    status: str = 'pending'
    context: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    answered_at: Optional[datetime] = None
    response: Optional[str] = None
    blocks_execution: bool = False

@dataclass
class UserQuestionRecord:
    """Rekord pytania od użytkownika"""
    id: str
    content: str
    context: Optional[Dict[str, Any]] = None
    status: str = 'pending'
    answer: Optional[str] = None
    needs_more_thinking: bool = False
    created_at: Optional[datetime] = None
    answered_at: Optional[datetime] = None
    cost_usd: float = 0.0

@dataclass
class ConsciousnessSessionRecord:
    """Rekord sesji świadomości"""
    id: str
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    total_thoughts: int = 0
    total_cost: float = 0.0
    final_mood: Optional[str] = None
    final_energy: Optional[float] = None
    status: str = 'active'

@dataclass
class SignificantMemoryRecord:
    """Rekord znaczącego wspomnienia"""
    id: Optional[int]
    memory_text: str
    memory_date: date
    category: str = 'other'
    importance_score: float = 1.0
    related_thought_id: Optional[int] = None
    created_at: Optional[datetime] = None

@dataclass
class WebActivityLogRecord:
    """Rekord aktywności dla strony web"""
    id: Optional[int]
    activity_type: str
    activity_title: str
    activity_description: Optional[str] = None
    activity_data: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
    is_displayed: bool = True

class AdamClayDatabase:
    """
    Główna klasa do zarządzania bazą danych Adam Clay
    
    Zapewnia wszystkie operacje CRUD dla tabel:
    - thoughts, email_questions, user_questions  
    - consciousness_sessions, significant_memories
    - system_stats, learned_patterns, web_activity_log
    """
    
    def __init__(self, config: Optional[DatabaseConfig] = None):
        self.config = config or DatabaseConfig()
        self.logger = logging.getLogger(__name__)
        
    @contextmanager
    def get_connection(self):
        """Context manager dla bezpiecznych połączeń z bazą"""
        connection = None
        try:
            connection = pymysql.connect(
                host=self.config.host,
                port=self.config.port,
                user=self.config.user,
                password=self.config.password,
                database=self.config.database,
                charset=self.config.charset,
                ideclass=pymysql.ides.DictIDE,
                autocommit=False
            )
            yield connection
        except Exception as e:
            if connection:
                connection.rollback()
            self.logger.error(f"Database error: {e}")
            raise
        finally:
            if connection:
                connection.close()
    
    # =====================================================
    # 💭 THOUGHTS - operacje na myślach
    # =====================================================
    
    def save_thought(self, thought: ThoughtRecord) -> int:
        """Zapisuje myśl do bazy danych"""
        with self.get_connection() as conn:
            ide = conn.ide()
            
            # Konwertuj context do JSON jeśli istnieje
            context_json = json.dumps(thought.context) if thought.context else None
            
            sql = """
            INSERT INTO thoughts (timestamp, content, thought_type, cost_usd, mood, 
                                energy_level, context, is_significant, session_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            ide.execute(sql, (
                thought.timestamp, thought.content, thought.thought_type,
                thought.cost_usd, thought.mood, thought.energy_level,
                context_json, thought.is_significant, thought.session_id
            ))
            
            thought_id = ide.lastrowid
            conn.commit()
            
            # Dodaj do logu aktywności web
            self._log_web_activity(
                'thought',
                f'Nowa myśl: {thought.thought_type}',
                thought.content[:100] + '...' if len(thought.content) > 100 else thought.content,
                {'thought_id': thought_id, 'cost': thought.cost_usd}
            )
            
            return thought_id
    
    def get_recent_thoughts(self, limit: int = 10) -> List[ThoughtRecord]:
        """Pobiera ostatnie myśli"""
        with self.get_connection() as conn:
            ide = conn.ide()
            
            sql = """
            SELECT * FROM thoughts 
            ORDER BY timestamp DESC 
            LIMIT %s
            """
            
            ide.execute(sql, (limit,))
            rows = ide.fetchall()
            
            thoughts = []
            for row in rows:
                # Parsuj context z JSON
                context = json.loads(row['context']) if row['context'] else None
                
                thought = ThoughtRecord(
                    id=row['id'],
                    timestamp=row['timestamp'],
                    content=row['content'], 
                    thought_type=row['thought_type'],
                    cost_usd=float(row['cost_usd']),
                    mood=row['mood'],
                    energy_level=float(row['energy_level']) if row['energy_level'] else None,
                    context=context,
                    is_significant=bool(row['is_significant']),
                    session_id=row['session_id'],
                    created_at=row['created_at']
                )
                thoughts.append(thought)
            
            return thoughts
    
    def get_significant_thoughts(self, limit: int = 20) -> List[ThoughtRecord]:
        """Pobiera znaczące myśli"""
        with self.get_connection() as conn:
            ide = conn.ide()
            
            sql = """
            SELECT * FROM thoughts 
            WHERE is_significant = TRUE
            ORDER BY timestamp DESC 
            LIMIT %s
            """
            
            ide.execute(sql, (limit,))
            rows = ide.fetchall()
            
            return [self._row_to_thought(row) for row in rows]
    
    def _row_to_thought(self, row: Dict) -> ThoughtRecord:
        """Konwertuje wiersz bazy na ThoughtRecord"""
        context = json.loads(row['context']) if row['context'] else None
        
        return ThoughtRecord(
            id=row['id'],
            timestamp=row['timestamp'],
            content=row['content'],
            thought_type=row['thought_type'],
            cost_usd=float(row['cost_usd']),
            mood=row['mood'],
            energy_level=float(row['energy_level']) if row['energy_level'] else None,
            context=context,
            is_significant=bool(row['is_significant']),
            session_id=row['session_id'],
            created_at=row['created_at']
        )
    
    # =====================================================
    # 🧠 CONSCIOUSNESS SESSIONS - sesje świadomości
    # =====================================================
    
    def create_consciousness_session(self) -> str:
        """Tworzy nową sesję świadomości"""
        session_id = str(uuid.uuid4())
        
        with self.get_connection() as conn:
            ide = conn.ide()
            
            sql = """
            INSERT INTO consciousness_sessions (id, started_at, status)
            VALUES (%s, %s, 'active')
            """
            
            ide.execute(sql, (session_id, datetime.now()))
            conn.commit()
            
            # Log aktywności
            self._log_web_activity(
                'session_start',
                'Adam Clay uruchomiony',
                f'Nowa sesja świadomości: {session_id}',
                {'session_id': session_id}
            )
            
        return session_id
    
    def update_consciousness_session(self, session_id: str, **kwargs):
        """Aktualizuje sesję świadomości"""
        if not kwargs:
            return
            
        with self.get_connection() as conn:
            ide = conn.ide()
            
            # Buduj dynamiczne UPDATE
            set_clauses = []
            values = []
            
            for key, value in kwargs.items():
                if key in ['total_thoughts', 'total_cost', 'final_mood', 'final_energy', 'status']:
                    set_clauses.append(f"{key} = %s")
                    values.append(value)
            
            if set_clauses:
                sql = f"UPDATE consciousness_sessions SET {', '.join(set_clauses)} WHERE id = %s"
                values.append(session_id)
                
                ide.execute(sql, values)
                conn.commit()
    
    def end_consciousness_session(self, session_id: str, final_mood: str, final_energy: float):
        """Kończy sesję świadomości"""
        with self.get_connection() as conn:
            ide = conn.ide()
            
            sql = """
            UPDATE consciousness_sessions 
            SET ended_at = %s, final_mood = %s, final_energy = %s, status = 'stopped'
            WHERE id = %s
            """
            
            ide.execute(sql, (datetime.now(), final_mood, final_energy, session_id))
            conn.commit()
            
            # Log aktywności
            self._log_web_activity(
                'session_end',
                'Adam Clay zatrzymany',
                f'Sesja {session_id} zakończona',
                {'session_id': session_id, 'final_mood': final_mood}
            )
    
    # =====================================================
    # 🎯 SIGNIFICANT MEMORIES - ważne wspomnienia
    # =====================================================
    
    def save_significant_memory(self, memory_text: str, category: str = 'other', 
                               importance_score: float = 1.0, 
                               related_thought_id: Optional[int] = None) -> int:
        """Zapisuje znaczące wspomnienie"""
        with self.get_connection() as conn:
            ide = conn.ide()
            
            sql = """
            INSERT INTO significant_memories (memory_text, memory_date, category, 
                                            importance_score, related_thought_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            ide.execute(sql, (
                memory_text, date.today(), category, importance_score, related_thought_id
            ))
            
            memory_id = ide.lastrowid
            conn.commit()
            
            # Log aktywności
            self._log_web_activity(
                'memory_created',
                'Nowe wspomnienie',
                memory_text[:100] + '...' if len(memory_text) > 100 else memory_text,
                {'memory_id': memory_id, 'category': category}
            )
            
            return memory_id
    
    def get_recent_memories(self, limit: int = 20) -> List[SignificantMemoryRecord]:
        """Pobiera ostatnie znaczące wspomnienia"""
        with self.get_connection() as conn:
            ide = conn.ide()
            
            sql = """
            SELECT * FROM significant_memories 
            ORDER BY created_at DESC 
            LIMIT %s
            """
            
            ide.execute(sql, (limit,))
            rows = ide.fetchall()
            
            memories = []
            for row in rows:
                memory = SignificantMemoryRecord(
                    id=row['id'],
                    memory_text=row['memory_text'],
                    memory_date=row['memory_date'],
                    category=row['category'],
                    importance_score=float(row['importance_score']),
                    related_thought_id=row['related_thought_id'],
                    created_at=row['created_at']
                )
                memories.append(memory)
            
            return memories
    
    # =====================================================
    # 📊 WEB ACTIVITY LOG - aktywność dla strony web
    # =====================================================
    
    def _log_web_activity(self, activity_type: str, activity_title: str, 
                         activity_description: Optional[str] = None,
                         activity_data: Optional[Dict[str, Any]] = None):
        """Dodaje wpis do logu aktywności web"""
        try:
            with self.get_connection() as conn:
                ide = conn.ide()
                
                activity_data_json = json.dumps(activity_data) if activity_data else None
                
                sql = """
                INSERT INTO web_activity_log (activity_type, activity_title, 
                                            activity_description, activity_data)
                VALUES (%s, %s, %s, %s)
                """
                
                ide.execute(sql, (
                    activity_type, activity_title, activity_description, activity_data_json
                ))
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Failed to log web activity: {e}")
    
    def get_live_activity(self, limit: int = 20) -> List[WebActivityLogRecord]:
        """Pobiera ostatnią aktywność dla strony web"""
        with self.get_connection() as conn:
            ide = conn.ide()
            
            sql = """
            SELECT id, activity_type, activity_title, activity_description, 
                   activity_data, timestamp,
                   TIMESTAMPDIFF(MINUTE, timestamp, NOW()) as minutes_ago
            FROM web_activity_log 
            WHERE is_displayed = TRUE
            ORDER BY timestamp DESC 
            LIMIT %s
            """
            
            ide.execute(sql, (limit,))
            rows = ide.fetchall()
            
            activities = []
            for row in rows:
                activity_data = json.loads(row['activity_data']) if row['activity_data'] else None
                
                activity = WebActivityLogRecord(
                    id=row['id'],
                    activity_type=row['activity_type'],
                    activity_title=row['activity_title'],
                    activity_description=row['activity_description'],
                    activity_data=activity_data,
                    timestamp=row['timestamp']
                )
                activities.append(activity)
            
            return activities
    
    # =====================================================
    # 📊 STATISTICS - statystyki
    # =====================================================
    
    def get_today_stats(self) -> Dict[str, Any]:
        """Pobiera dzisiejsze statystyki"""
        with self.get_connection() as conn:
            ide = conn.ide()
            
            sql = """
            SELECT 
                COUNT(*) as thoughts_today,
                COALESCE(SUM(cost_usd), 0) as cost_today,
                COALESCE(AVG(energy_level), 0) as avg_energy,
                MAX(timestamp) as last_thought,
                COUNT(CASE WHEN is_significant = TRUE THEN 1 END) as significant_thoughts
            FROM thoughts 
            WHERE DATE(timestamp) = CURDATE()
            """
            
            ide.execute(sql)
            result = ide.fetchone()
            
            return {
                'thoughts_today': result['thoughts_today'],
                'cost_today': float(result['cost_today']),
                'avg_energy': float(result['avg_energy']),
                'last_thought': result['last_thought'],
                'significant_thoughts': result['significant_thoughts']
            }
    
    def get_consciousness_status(self) -> Dict[str, Any]:
        """Pobiera status aktualnej sesji świadomości"""
        with self.get_connection() as conn:
            ide = conn.ide()
            
            sql = """
            SELECT * FROM consciousness_sessions 
            WHERE status = 'active'
            ORDER BY started_at DESC 
            LIMIT 1
            """
            
            ide.execute(sql)
            session = ide.fetchone()
            
            if session:
                return {
                    'session_id': session['id'],
                    'started_at': session['started_at'],
                    'total_thoughts': session['total_thoughts'],
                    'total_cost': float(session['total_cost']),
                    'status': session['status']
                }
            else:
                return {
                    'session_id': None,
                    'started_at': None,
                    'total_thoughts': 0,
                    'total_cost': 0.0,
                    'status': 'inactive'
                }
    
    # =====================================================
    # 🧪 TEST CONNECTION
    # =====================================================
    
    def test_connection(self) -> bool:
        """Testuje połączenie z bazą danych"""
        try:
            with self.get_connection() as conn:
                ide = conn.ide()
                ide.execute("SELECT 1")
                return True
        except Exception as e:
            self.logger.error(f"Database connection test failed: {e}")
            return False 