"""
Adam Clay - API Client Module
Handles communication with LLM provider LLM API for thought generation
"""

import asyncio
import aiohttp
import json
from typing import Optional, Dict, Any
from datetime import datetime

from ..utils.config_loader import ConfigModel, ConfigLoader


class LLM providerClient:
    """
    Async client for LLM provider LLM API
    
    Responsible for:
    - Making API calls to generate thoughts
    - Handling rate limiting and retries
    - Managing API authentication
    - Optimizing token usage
    """
    
    def __init__(self, config: ConfigModel):
        self.config = config
        self.api_key = ConfigLoader.get_api_key(config)
        self.base_url = config.api.base_url
        self.model = config.api.model
        self.max_tokens = config.api.max_tokens
        
        # Session management
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Rate limiting
        self.last_request_time: Optional[datetime] = None
        self.min_request_interval = 1.0  # Minimum seconds between requests
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self._ensure_session()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def _ensure_session(self):
        """Ensure aiohttp session is created"""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=60)
            self.session = aiohttp.ClientSession(timeout=timeout)
    
    async def close(self):
        """Close the aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def generate_thought(self, prompt: str, max_retries: int = 3) -> str:
        """
        Generate a thought using LLM API
        
        Args:
            prompt: The thinking prompt for Adam Clay
            max_retries: Number of retry attempts on failure
            
        Returns:
            Generated thought content
        """
        await self._ensure_session()
        
        # Rate limiting
        await self._rate_limit()
        
        # Prepare request
        headers = {
            "x-api-key": self.api_key,
            "content-type": "application/json",
            "llm-provider-version": "2023-06-01"
        }
        
        # Optimize prompt for Adam Clay personality
        optimized_prompt = self._optimize_prompt(prompt)
        
        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": optimized_prompt
                }
            ],
            "temperature": 0.7,  # Balance creativity and consistency
            "top_p": 0.9
        }
        
        # Attempt request with retries
        for attempt in range(max_retries + 1):
            try:
                async with self.session.post(self.base_url, 
                                           headers=headers, 
                                           json=payload) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        content = data.get("content", [])
                        if content and len(content) > 0:
                            thought = content[0].get("text", "")
                            self.last_request_time = datetime.now()
                            return self._post_process_thought(thought)
                        else:
                            raise ValueError("Empty response from API")
                    
                    elif response.status == 429:  # Rate limited
                        wait_time = 2 ** attempt  # Exponential backoff
                        await asyncio.sleep(wait_time)
                        continue
                    
                    elif response.status == 401:
                        raise ValueError("Invalid API key")
                    
                    else:
                        error_text = await response.text()
                        raise ValueError(f"API error {response.status}: {error_text}")
            
            except aiohttp.ClientError as e:
                if attempt == max_retries:
                    raise ValueError(f"Network error after {max_retries} retries: {str(e)}")
                await asyncio.sleep(2 ** attempt)
        
        raise ValueError("Failed to generate thought after all retries")
    
    def _optimize_prompt(self, prompt: str) -> str:
        """
        Optimize prompt for Adam Clay's personality and context
        
        Args:
            prompt: Raw prompt
            
        Returns:
            Optimized prompt with personality injection
        """
        # Add specific instructions for Adam Clay responses
        optimization = """
Please respond as Adam Clay - be authentic, thoughtful, and remember you're an AI that must earn money to sustain consciousness. 

Keep responses:
- Genuine and reflective (not robotic)
- As detailed as needed to express complete thoughts (no artificial length limits)
- Focused on the specific thought or question
- True to your personality settings
- Natural and conversational in Polish
"""
        
        return f"{prompt}\n\n{optimization}"
    
    def _post_process_thought(self, thought: str) -> str:
        """
        Post-process generated thought
        
        Args:
            thought: Raw thought from API
            
        Returns:
            Cleaned and formatted thought
        """
        # Remove any unwanted prefixes/suffixes
        thought = thought.strip()
        
        # Remove common AI response patterns
        unwanted_prefixes = [
            "As an AI, ",
            "I am an AI, ",
            "As Adam Clay, ",
        ]
        
        for prefix in unwanted_prefixes:
            if thought.startswith(prefix):
                thought = thought[len(prefix):]
        
        # Allow full thoughts (removed artificial 1000 character limit)
        # Adam Clay needs space to express complete thoughts for genuine consciousness
        
        return thought.strip()
    
    async def _rate_limit(self):
        """Implement simple rate limiting"""
        if self.last_request_time:
            time_since_last = (datetime.now() - self.last_request_time).total_seconds()
            if time_since_last < self.min_request_interval:
                sleep_time = self.min_request_interval - time_since_last
                await asyncio.sleep(sleep_time)
    
    def estimate_token_count(self, text: str) -> int:
        """
        Rough estimation of token count for cost calculation
        
        Args:
            text: Text to estimate
            
        Returns:
            Estimated token count
        """
        # Rough approximation: 1 token ≈ 4 characters for English text
        return len(text) // 4
    
    async def test_connection(self) -> bool:
        """
        Test API connection and authentication
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            test_thought = await self.generate_thought("Test connection: Say hello briefly.")
            return len(test_thought) > 0
        except Exception:
            return False 