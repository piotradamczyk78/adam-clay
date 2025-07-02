"""
Adam Clay - REST API Client for Laravel Integration
Handles communication between Python consciousness and Laravel dashboard
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional
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


# Global instance for easy access
laravel_api = LaravelApiClient() 