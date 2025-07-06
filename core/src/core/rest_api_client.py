"""
Adam Clay - REST API Client for Laravel Integration
Handles communication between Python consciousness and Laravel dashboard
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from loguru import logger


@dataclass
class LaravelApiConfig:
    """Configuration for Laravel API connection"""
    base_url: str = "http://adamclay.local:8004/api"
    timeout: int = 10
    verify_ssl: bool = False
    

class LaravelApiClient:
    """
    🔌 REST API Client for Laravel Integration
    
    Handles all communication with Laravel dashboard API:
    - Sending thoughts to /api/thoughts
    - Creating/updating consciousness sessions
    - Logging web activity
    - Sending significant memories
    """
    
    def __init__(self, config: LaravelApiConfig = None):
        self.config = config or LaravelApiConfig()
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Adam-Clay-Python/1.0'
        })
        
        logger.info(f"🔌 Laravel API Client initialized: {self.config.base_url}")
    
    async def send_thought(self, thought) -> bool:
        """
        📤 Send a thought to Laravel API
        
        Args:
            thought: Thought object from consciousness
            
        Returns:
            bool: Success status
        """
        try:
            # Convert Thought to Laravel API format
            payload = {
                "timestamp": thought.timestamp.isoformat(),
                "content": thought.content,
                "thought_type": self._map_thought_type(thought.thought_type),
                "cost_usd": float(thought.cost_usd),
                "mood": getattr(thought, 'mood', None),
                "energy_level": getattr(thought, 'energy_level', None),
                "context": thought.context or {},
                "is_significant": self._is_significant_thought(thought),
                "session_id": getattr(thought, 'session_id', 'default-session')
            }
            
            response = self.session.post(
                f"{self.config.base_url}/thoughts",
                json=payload,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )
            
            if response.status_code == 201:
                logger.success(f"💭 Thought sent to Laravel: {thought.content[:50]}...")
                return True
            else:
                logger.error(f"❌ Failed to send thought: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"🚫 Network error sending thought: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error sending thought: {e}")
            return False
    
    async def create_consciousness_session(self, session_id: str) -> bool:
        """
        🧠 Create new consciousness session in Laravel
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            bool: Success status
        """
        try:
            payload = {
                "session_id": session_id,
                "started_at": datetime.now().isoformat(),
                "status": "active"
            }
            
            response = self.session.post(
                f"{self.config.base_url}/sessions",
                json=payload,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )
            
            if response.status_code in [200, 201]:
                logger.success(f"🧠 Consciousness session created: {session_id}")
                return True
            else:
                logger.error(f"❌ Failed to create session: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error creating consciousness session: {e}")
            return False
    
    async def update_consciousness_session(self, session_id: str, total_thoughts: int, total_cost: float) -> bool:
        """
        📊 Update consciousness session statistics
        
        Args:
            session_id: Session identifier
            total_thoughts: Total thoughts generated
            total_cost: Total cost in USD
            
        Returns:
            bool: Success status
        """
        try:
            payload = {
                "total_thoughts": total_thoughts,
                "total_cost": float(total_cost),
                "status": "active"
            }
            
            response = self.session.put(
                f"{self.config.base_url}/sessions/{session_id}",
                json=payload,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )
            
            if response.status_code in [200, 201]:
                logger.debug(f"📊 Session updated: {total_thoughts} thoughts, ${total_cost:.4f}")
                return True
            else:
                logger.warning(f"⚠️ Failed to update session: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error updating consciousness session: {e}")
            return False
    
    async def send_significant_memory(self, memory_text: str, category: str = "learning") -> bool:
        """
        🎯 Send significant memory to Laravel
        
        Args:
            memory_text: The memory content
            category: Memory category (insight, learning, strategy, etc.)
            
        Returns:
            bool: Success status
        """
        try:
            payload = {
                "memory_text": memory_text,
                "category": category,
                "timestamp": datetime.now().isoformat()
            }
            
            response = self.session.post(
                f"{self.config.base_url}/memories",
                json=payload,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )
            
            if response.status_code in [200, 201]:
                logger.success(f"🎯 Significant memory sent: {memory_text[:50]}...")
                return True
            else:
                logger.error(f"❌ Failed to send memory: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error sending significant memory: {e}")
            return False
    
    async def log_web_activity(self, activity_type: str, title: str, description: str, data: Dict[str, Any] = None) -> bool:
        """
        📱 Log activity for web dashboard
        
        Args:
            activity_type: Type of activity (thought, question_sent, question_answered, session_start, session_end, memory_created)
            title: Activity title
            description: Activity description
            data: Additional activity data
            
        Returns:
            bool: Success status
        """
        # Map activity types to valid ENUM values
        activity_mapping = {
            'integration_test': 'thought',
            'test': 'thought',
            'thought': 'thought',
            'session': 'session_start',
            'memory': 'memory_created',
            'question': 'question_sent'
        }
        
        mapped_activity_type = activity_mapping.get(activity_type, 'thought')
        try:
            payload = {
                "activity_type": mapped_activity_type,
                "activity_title": title,
                "activity_description": description,
                "activity_data": data or {},
                "timestamp": datetime.now().isoformat()
            }
            
            response = self.session.post(
                f"{self.config.base_url}/activity",
                json=payload,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )
            
            if response.status_code in [200, 201]:
                logger.debug(f"📱 Web activity logged: {title}")
                return True
            else:
                logger.warning(f"⚠️ Failed to log activity: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error logging web activity: {e}")
            return False
    
    async def get_system_status(self) -> Optional[Dict[str, Any]]:
        """
        📊 Get system status from Laravel API
        
        Returns:
            Dict containing system status or None if failed
        """
        try:
            response = self.session.get(
                f"{self.config.base_url}/status",
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"⚠️ Failed to get status: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error getting system status: {e}")
            return None
    
    async def test_connection(self) -> bool:
        """
        🔍 Test connection to Laravel API
        
        Returns:
            bool: Connection status
        """
        try:
            response = self.session.get(
                f"{self.config.base_url}/hello",
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.success(f"✅ Laravel API connected: {data.get('message', 'OK')}")
                return True
            else:
                logger.error(f"❌ Laravel API connection failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"🚫 Cannot connect to Laravel API: {e}")
            return False
    
    def _map_thought_type(self, thought_type: str) -> str:
        """Map Python thought types to Laravel enum values"""
        mapping = {
            'autonomous': 'autonomous',
            'reactive': 'reactive', 
            'business': 'business',
            'philosophical': 'philosophical',
            'system': 'autonomous',  # fallback
            'creative': 'philosophical',  # fallback
            'analytical': 'business'  # fallback
        }
        return mapping.get(thought_type, 'autonomous')
    
    def _is_significant_thought(self, thought) -> bool:
        """Determine if thought is significant (same logic as consciousness)"""
        content = thought.content.lower()
        
        significant_keywords = [
            'nauczyłem się', 'zrozumiałem', 'odkryłem', 'wniosek',
            'strategia', 'plan', 'cel', 'priorytet', 'klient',
            'błąd', 'sukces', 'problemem', 'rozwiązanie',
            'ważne', 'kluczowe', 'przełomowe'
        ]
        
        return any(keyword in content for keyword in significant_keywords) or \
               thought.thought_type == "business" or \
               len(thought.content) > 200
    
    async def get_thinking_status(self) -> Optional[Dict[str, Any]]:
        """
        🧠 Get thinking status from Laravel API (checks session status in database)
        
        Returns:
            Dict containing thinking status or None if failed
        """
        try:
            response = self.session.get(
                f"{self.config.base_url}/consciousness/thinking-status",
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.debug(f"🧠 Thinking status checked: {data.get('thinking_status', {}).get('message', 'Unknown')}")
                return data
            else:
                logger.warning(f"⚠️ Failed to get thinking status: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error getting thinking status: {e}")
            return None
    
    async def save_email_question(self, question_id: str, content: str, priority: str, 
                                blocks_execution: bool, context: Dict[str, Any] = None) -> bool:
        """
        📧 Save email question to Laravel database
        
        Args:
            question_id: Unique question identifier
            content: Question content
            priority: Question priority (CRITICAL, IMPORTANT, etc.)
            blocks_execution: Whether this question blocks Adam's thinking
            context: Additional context data
            
        Returns:
            bool: Success status
        """
        try:
            payload = {
                "id": question_id,
                "content": content,
                "priority": priority,
                "status": "pending",
                "context": context or {},
                "blocks_execution": blocks_execution,
                "created_at": datetime.now().isoformat()
            }
            
            response = self.session.post(
                f"{self.config.base_url}/email-questions",
                json=payload,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )
            
            if response.status_code in [200, 201]:
                logger.success(f"📧 Email question saved to database: {question_id}")
                return True
            else:
                logger.error(f"❌ Failed to save email question: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error saving email question: {e}")
            return False
    
    async def save_significant_memory(self, memory_text: str, category: str, importance_score: float, related_thought_id: Optional[int] = None) -> Optional[int]:
        """
        💾 Save significant memory to database
        
        Args:
            memory_text: Text of the memory (max 2000 chars)
            category: Category (business, learning, insight, strategy, error, success, other)
            importance_score: Importance score 0.00-9.99
            related_thought_id: Optional related thought ID
            
        Returns:
            Memory ID if successful, None if failed
        """
        try:
            data = {
                'memory_text': memory_text[:2000],  # Ensure max length
                'memory_date': datetime.now().date().isoformat(),
                'category': category,
                'importance_score': min(9.99, max(0.00, importance_score)),
                'related_thought_id': related_thought_id
            }
            
            response = self.session.post(
                f"{self.config.base_url}/memories/significant",
                json=data,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    memory_id = result.get('memory_id')
                    logger.success(f"💾 Significant memory saved: {memory_id}")
                    return memory_id
            
            logger.warning(f"⚠️ Failed to save significant memory: {response.status_code}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Failed to save significant memory: {e}")
            return None
    
    async def get_significant_memories(self, limit: int = 20, category: Optional[str] = None, min_importance: float = 0.0) -> Optional[List[Dict]]:
        """
        🧠 Get significant memories from database
        
        Args:
            limit: Maximum number of memories (1-50)
            category: Filter by category (optional)
            min_importance: Minimum importance score
            
        Returns:
            List of memories or None if failed
        """
        try:
            params = {
                'limit': min(50, max(1, limit)),
                'min_importance': min_importance
            }
            
            if category:
                params['category'] = category
            
            response = self.session.get(
                f"{self.config.base_url}/memories/significant",
                params=params,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    memories = result.get('memories', [])
                    logger.debug(f"🧠 Retrieved {len(memories)} significant memories")
                    return memories
            
            logger.warning(f"⚠️ Failed to get significant memories: {response.status_code}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Failed to get significant memories: {e}")
            return None
    
    async def get_recent_thoughts_from_db(self, limit: int = 10, hours_back: int = 24) -> Optional[List[Dict]]:
        """
        💭 Get recent thoughts from database to avoid repetition
        
        Args:
            limit: Maximum number of thoughts
            hours_back: How many hours back to look
            
        Returns:
            List of recent thoughts or None if failed
        """
        try:
            # Calculate timestamp from hours back
            since_time = (datetime.now() - timedelta(hours=hours_back)).isoformat()
            
            params = {
                'limit': limit,
                'since': since_time
            }
            
            response = self.session.get(
                f"{self.config.base_url}/thoughts/recent",
                params=params,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    thoughts = result.get('thoughts', [])
                    logger.debug(f"💭 Retrieved {len(thoughts)} recent thoughts")
                    return thoughts
            
            logger.warning(f"⚠️ Failed to get recent thoughts: {response.status_code}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Failed to get recent thoughts: {e}")
            return None


# Global instance for easy access
laravel_api = LaravelApiClient() 