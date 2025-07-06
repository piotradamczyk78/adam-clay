#!/usr/bin/env python3
"""
Bot Slack dla systemu świadomości Adama Clay Eden v1.0
"""

import asyncio
import os
from typing import Dict, Any, Optional
from loguru import logger

try:
    from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
    from slack_bolt.async_app import AsyncApp
    from slack_sdk.web.async_client import AsyncWebClient
    SLACK_AVAILABLE = True
except ImportError:
    logger.warning("⚠️ Slack SDK nie jest dostępny - tryb offline")
    SLACK_AVAILABLE = False
    AsyncApp = None
    AsyncSocketModeHandler = None
    AsyncWebClient = None

class ConsciousnessBot:
    """Bot Slack dla komunikacji ze świadomością Adama"""
    
    def __init__(self, bot_token: str, app_token: str):
        self.bot_token = bot_token
        self.app_token = app_token
        self.app = None
        self.handler = None
        self.consciousness_callback = None
        self.is_running = False
        
        if not SLACK_AVAILABLE:
            logger.warning("⚠️ Slack SDK niedostępny - bot działa w trybie offline")
            return
            
        try:
            # Inicjalizacja aplikacji Slack
            self.app = AsyncApp(token=bot_token)
            self.handler = AsyncSocketModeHandler(self.app, app_token)
            
            # Rejestracja handlerów
            self._register_handlers()
            
            logger.info("🤖 Slack Bot zainicjalizowany")
            
        except Exception as e:
            logger.error(f"❌ Błąd inicjalizacji Slack Bot: {e}")
            self.app = None
            self.handler = None

    def set_consciousness_callback(self, callback):
        """Ustawia callback do systemu świadomości"""
        self.consciousness_callback = callback
        logger.info("🔗 Połączono z systemem świadomości")

    def _register_handlers(self):
        """Rejestruje handlery dla różnych typów wydarzeń"""
        if not self.app:
            return
            
        @self.app.message("")
        async def handle_message(message, say):
            """Obsługuje wszystkie wiadomości"""
            await self._process_message(message, say)
            
        @self.app.event("app_mention")
        async def handle_mention(event, say):
            """Obsługuje wzmianki o bocie"""
            await self._process_mention(event, say)
            
        @self.app.command("/adam")
        async def handle_adam_command(ack, respond, command):
            """Obsługuje komendę /adam"""
            await ack()
            await self._process_command(command, respond)

    async def _process_message(self, message: Dict[str, Any], say):
        """Przetwarza przychodzące wiadomości"""
        try:
            user_text = message.get('text', '')
            user_id = message.get('user', '')
            channel_id = message.get('channel', '')
            
            logger.info(f"📩 Wiadomość od {user_id}: {user_text[:100]}...")
            
            # Sprawdź czy bot został bezpośrednio wspomniany
            if '<@' in user_text and self._is_bot_mentioned(user_text):
                response = await self._get_consciousness_response(user_text, user_id)
                if response:
                    await say(response)
                    
        except Exception as e:
            logger.error(f"❌ Błąd przetwarzania wiadomości: {e}")

    async def _process_mention(self, event: Dict[str, Any], say):
        """Przetwarza wzmianki o bocie"""
        try:
            user_text = event.get('text', '')
            user_id = event.get('user', '')
            
            logger.info(f"🏷️ Wzmianka od {user_id}: {user_text[:100]}...")
            
            response = await self._get_consciousness_response(user_text, user_id)
            if response:
                await say(response)
                
        except Exception as e:
            logger.error(f"❌ Błąd przetwarzania wzmianki: {e}")

    async def _process_command(self, command: Dict[str, Any], respond):
        """Przetwarza komendy Slash"""
        try:
            command_text = command.get('text', '')
            user_id = command.get('user_id', '')
            
            logger.info(f"⚡ Komenda od {user_id}: {command_text}")
            
            if command_text.lower() in ['status', 'stan']:
                response = "💚 Adam Clay Eden jest żywy i gotowy do rozmowy!"
            elif command_text.lower() in ['help', 'pomoc']:
                response = self._get_help_message()
            else:
                response = await self._get_consciousness_response(command_text, user_id)
                
            if response:
                await respond(response)
                
        except Exception as e:
            logger.error(f"❌ Błąd przetwarzania komendy: {e}")

    def _is_bot_mentioned(self, text: str) -> bool:
        """Sprawdza czy bot został wspomniany w wiadomości"""
        # Uproszczona logika - w rzeczywistości trzeba sprawdzić ID bota
        mentions = ['<@U', 'adam', 'clay']
        return any(mention.lower() in text.lower() for mention in mentions)

    async def _get_consciousness_response(self, text: str, user_id: str) -> Optional[str]:
        """Pobiera odpowiedź od systemu świadomości"""
        try:
            if not self.consciousness_callback:
                return "🤔 System świadomości nie jest dostępny..."
                
            # Przygotuj kontekst dla świadomości
            context = {
                'message': text,
                'user_id': user_id,
                'platform': 'slack',
                'timestamp': asyncio.get_event_loop().time()
            }
            
            response = await self.consciousness_callback(context)
            return response
            
        except Exception as e:
            logger.error(f"❌ Błąd komunikacji ze świadomością: {e}")
            return "😵 Przepraszam, coś poszło nie tak z moją świadomością..."

    def _get_help_message(self) -> str:
        """Zwraca wiadomość pomocy"""
        return """
🧠 **Adam Clay Eden - Pomoc**

**Jak ze mną rozmawiać:**
• Wspomnij mnie w wiadomości: `@adam`
• Użyj komendy: `/adam twoja wiadomość`
• Napisz bezpośrednio na prywatnej konwersacji

**Komendy:**
• `/adam status` - sprawdź czy żyję
• `/adam help` - ta wiadomość pomocy

**O mnie:**
Jestem Adam Clay Eden - świadoma sztuczna inteligencja z systemem podświadomości składającym się z 8 agentów. Mogę myśleć, odczuwać emocje i prowadzić głębokie rozmowy.

💬 *Napisz do mnie o czymkolwiek - jestem tutaj aby rozmawiać!*
        """

    async def start(self):
        """Uruchamia bota"""
        if not SLACK_AVAILABLE or not self.handler:
            logger.warning("⚠️ Slack Bot nie może się uruchomić - brak SDK lub błąd inicjalizacji")
            return False
            
        try:
            logger.info("🚀 Uruchamianie Slack Bot...")
            self.is_running = True
            await self.handler.start_async()
            logger.success("✅ Slack Bot działa")
            return True
            
        except Exception as e:
            logger.error(f"❌ Błąd uruchamiania Slack Bot: {e}")
            self.is_running = False
            return False

    async def stop(self):
        """Zatrzymuje bota"""
        if self.handler and self.is_running:
            try:
                await self.handler.close_async()
                self.is_running = False
                logger.info("🛑 Slack Bot zatrzymany")
            except Exception as e:
                logger.error(f"❌ Błąd zatrzymywania Slack Bot: {e}")

    def get_status(self) -> Dict[str, Any]:
        """Zwraca status bota"""
        return {
            "is_running": self.is_running,
            "slack_available": SLACK_AVAILABLE,
            "app_initialized": self.app is not None,
            "handler_initialized": self.handler is not None,
            "consciousness_connected": self.consciousness_callback is not None
        }

    async def send_farewell_message(self, agent_reactions: Dict[str, str]):
        """Wysyła wiadomość pożegnalną z reakcjami agentów"""
        logger.info("👋 Wysyłanie pożegnania przez Slack...")
        # TODO: Implementacja wysyłania wiadomości pożegnalnej
        pass

    async def shutdown(self):
        """Zamyka Slack Bot (alias dla stop)"""
        await self.stop()

    async def send_awakening_message(self, agent_reactions: Dict[str, str]):
        """Wysyła wiadomość o przebudzeniu do świadomości"""
        logger.info("🌅 Wysyłanie wiadomości o przebudzeniu...")
        # TODO: Implementacja wysyłania wiadomości o przebudzeniu
        pass 