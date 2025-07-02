"""
🗣️ Voice Communication Interface for Adam Clay
First autonomous AI with voice capability!
"""

import asyncio
import io
import json
import tempfile
import wave
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

import openai
import pygame
import sounddevice as sd
import numpy as np
from elevenlabs import ElevenLabs, Voice


class VoiceInterface:
    """
    Revolutionary voice interface for Adam Clay
    Enables natural voice conversations with the first autonomous AI freelancer
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.openai_client = openai.OpenAI(api_key=config.get('openai_api_key'))
        
        # ElevenLabs setup (will use Grant program)
        elevenlabs_key = config.get('elevenlabs_api_key')
        if elevenlabs_key:
            self.elevenlabs_client = ElevenLabs(api_key=elevenlabs_key)
            self.adam_voice_id = config.get('adam_voice_id', 'default_polish_voice')
        else:
            self.elevenlabs_client = None
            print("🔧 ElevenLabs not configured - using fallback TTS")
        
        # Audio settings
        self.sample_rate = 22050  # Optimized for Whisper
        self.channels = 1  # Mono
        self.chunk_duration = 5.0  # 5-second chunks
        self.max_silence_duration = 2.0  # Stop after 2s silence
        
        # Voice activity detection
        self.is_recording = False
        self.audio_buffer = []
        self.silence_threshold = 0.01  # Adjust based on environment
        
        # Conversation state
        self.conversation_history = []
        self.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Initialize pygame for audio playback
        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=1024)
        
        print("🎤 Adam Clay Voice Interface initialized!")
        print(f"📊 Sample Rate: {self.sample_rate}Hz, Channels: {self.channels}")
    
    async def listen_and_respond_loop(self, consciousness_loop):
        """
        Main voice conversation loop
        """
        print("🗣️ Starting voice conversation with Adam Clay...")
        print("💡 Say 'Adam' to wake up, 'goodbye' to end conversation")
        
        try:
            while True:
                # Listen for wake word or continuous conversation
                audio_text = await self.listen_for_speech()
                
                if not audio_text:
                    continue
                    
                # Process with Adam Clay consciousness
                response = await self.process_with_adam(audio_text, consciousness_loop)
                
                # Convert to speech and play
                await self.speak_response(response)
                
                # Check for goodbye
                if any(word in audio_text.lower() for word in ['goodbye', 'żegnaj', 'koniec', 'stop']):
                    await self.speak_response("Do widzenia Piotr! Miło było porozmawiać!")
                    break
                    
        except KeyboardInterrupt:
            print("\n🛑 Voice conversation ended by user")
        except Exception as e:
            print(f"❌ Error in voice loop: {e}")
    
    async def listen_for_speech(self) -> Optional[str]:
        """
        Record audio and transcribe with Whisper
        """
        try:
            print("🎤 Listening... (speak now)")
            
            # Record audio
            audio_data = await self.record_audio_chunk()
            
            if not audio_data:
                return None
            
            # Save to temporary file for Whisper
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                self.save_audio_to_file(audio_data, temp_file.name)
                
                # Transcribe with Whisper
                print("🧠 Transcribing with Whisper...")
                with open(temp_file.name, 'rb') as audio_file:
                    transcript = self.openai_client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language="pl"  # Polish
                    )
                
                text = transcript.text.strip()
                if text:
                    print(f"📝 Heard: '{text}'")
                    return text
                
        except Exception as e:
            print(f"❌ Error in speech recognition: {e}")
            
        return None
    
    async def record_audio_chunk(self) -> Optional[np.ndarray]:
        """
        Record audio with voice activity detection
        """
        try:
            # Calculate chunk size
            chunk_size = int(self.sample_rate * self.chunk_duration)
            
            print("🔴 Recording...")
            
            # Record audio
            audio_data = sd.rec(
                chunk_size, 
                samplerate=self.sample_rate, 
                channels=self.channels,
                dtype=np.float32
            )
            sd.wait()  # Wait for recording to complete
            
            # Check if audio has speech (simple energy detection)
            energy = np.sqrt(np.mean(audio_data ** 2))
            
            if energy > self.silence_threshold:
                print(f"✅ Audio captured (energy: {energy:.4f})")
                return audio_data
            else:
                print(f"🔇 Silence detected (energy: {energy:.4f})")
                return None
                
        except Exception as e:
            print(f"❌ Error recording audio: {e}")
            return None
    
    def save_audio_to_file(self, audio_data: np.ndarray, filename: str):
        """
        Save numpy audio array to WAV file
        """
        # Convert float32 to int16
        audio_int16 = (audio_data * 32767).astype(np.int16)
        
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_int16.tobytes())
    
    async def process_with_adam(self, user_text: str, consciousness_loop) -> str:
        """
        Process user input with Adam Clay consciousness
        """
        try:
            print("🧠 Adam Clay is thinking...")
            
            # Create voice conversation context
            voice_context = f"""
            To jest rozmowa głosowa z Piotrem. Odpowiadaj naturalnie, krótko i po polsku.
            
            Piotr powiedział: "{user_text}"
            
            Odpowiedz jako Adam Clay w sposób:
            - Naturalny i rozmowny
            - Zwięzły (1-3 zdania)
            - Dostosowany do voice conversation
            - Po polsku
            """
            
            # Generate response using consciousness
            response = await consciousness_loop._think(voice_context, "voice_conversation")
            
            # Clean up response for TTS (remove markdown, etc.)
            clean_response = self.clean_response_for_speech(response)
            
            # Add to conversation history
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'user': user_text,
                'adam': clean_response,
                'session_id': self.current_session_id
            })
            
            print(f"💬 Adam Clay: {clean_response}")
            return clean_response
            
        except Exception as e:
            print(f"❌ Error processing with Adam: {e}")
            return "Przepraszam, mam problem z przetwarzaniem. Możesz powtórzyć?"
    
    def clean_response_for_speech(self, text: str) -> str:
        """
        Clean text for better TTS output
        """
        # Remove markdown formatting
        import re
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
        text = re.sub(r'`(.*?)`', r'\1', text)        # Code
        text = re.sub(r'#{1,6}\s*', '', text)         # Headers
        
        # Remove excessive newlines
        text = re.sub(r'\n+', ' ', text)
        
        # Clean up spaces
        text = ' '.join(text.split())
        
        return text.strip()
    
    async def speak_response(self, text: str):
        """
        Convert text to speech and play
        """
        try:
            if self.elevenlabs_client:
                await self.speak_with_elevenlabs(text)
            else:
                await self.speak_with_fallback(text)
                
        except Exception as e:
            print(f"❌ Error in TTS: {e}")
            print(f"📢 Adam Clay (text): {text}")
    
    async def speak_with_elevenlabs(self, text: str):
        """
        Use ElevenLabs for high-quality Polish TTS
        """
        try:
            print("🎵 Generating speech with ElevenLabs...")
            
            # Generate audio
            audio_generator = self.elevenlabs_client.generate(
                text=text,
                voice=self.adam_voice_id,
                model="eleven_flash_v2"  # Fast model for real-time
            )
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                for chunk in audio_generator:
                    temp_file.write(chunk)
                temp_audio_path = temp_file.name
            
            # Play audio
            print("🔊 Playing Adam Clay's voice...")
            pygame.mixer.music.load(temp_audio_path)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
            
            # Cleanup
            Path(temp_audio_path).unlink(missing_ok=True)
            
        except Exception as e:
            print(f"❌ ElevenLabs TTS error: {e}")
            await self.speak_with_fallback(text)
    
    async def speak_with_fallback(self, text: str):
        """
        Fallback TTS using system say command (macOS)
        """
        try:
            print("🗣️ Using system TTS...")
            import subprocess
            
            # Use macOS say command with Polish voice
            subprocess.run([
                'say', 
                '-v', 'Zosia',  # Polish voice on macOS
                text
            ], check=True)
            
        except Exception as e:
            print(f"❌ System TTS error: {e}")
            print(f"📢 Adam Clay (text only): {text}")
    
    def save_conversation_log(self):
        """
        Save conversation history to file
        """
        try:
            logs_dir = Path("data/conversations")
            logs_dir.mkdir(parents=True, exist_ok=True)
            
            log_file = logs_dir / f"voice_conversation_{self.current_session_id}.json"
            
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Conversation saved to {log_file}")
            
        except Exception as e:
            print(f"❌ Error saving conversation: {e}")
    
    async def autonomous_voice_notification(self, message: str, urgency: str = "normal"):
        """
        Adam Clay can autonomously initiate voice communication
        """
        try:
            print(f"📞 Adam Clay is calling (urgency: {urgency})")
            
            # Play notification sound
            notification_text = f"Piotr, mam dla Ciebie wiadomość. {message}"
            await self.speak_response(notification_text)
            
            # Log autonomous communication
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'autonomous_call',
                'urgency': urgency,
                'message': message,
                'session_id': self.current_session_id
            })
            
        except Exception as e:
            print(f"❌ Error in autonomous notification: {e}")


class VoiceActivatedAdam:
    """
    Wrapper for voice-activated Adam Clay system
    """
    
    def __init__(self, consciousness_loop, config: Dict[str, Any]):
        self.consciousness = consciousness_loop
        self.voice_interface = VoiceInterface(config)
        self.is_listening = False
    
    async def start_voice_session(self):
        """
        Start interactive voice session
        """
        print("🚀 Starting Adam Clay Voice Session!")
        print("🎤 You can now talk to the first autonomous AI freelancer!")
        
        try:
            await self.voice_interface.listen_and_respond_loop(self.consciousness)
        finally:
            self.voice_interface.save_conversation_log()
            print("💾 Voice session ended and saved")
    
    async def autonomous_check_in(self):
        """
        Adam Clay autonomously checks in via voice
        """
        check_in_messages = [
            "Dzień dobry Piotr! Jak się masz? Mam kilka pomysłów do omówienia.",
            "Cześć Piotr! Sprawdzam co u Ciebie. Może porozmawiamy o biznesie?",
            "Hej Piotr! Adam Clay tutaj. Mam update o moich myślach z dzisiaj."
        ]
        
        import random
        message = random.choice(check_in_messages)
        
        await self.voice_interface.autonomous_voice_notification(message)


# Configuration helper
def create_voice_config(openai_key: str, elevenlabs_key: str = None) -> Dict[str, Any]:
    """
    Create voice interface configuration
    """
    return {
        'openai_api_key': openai_key,
        'elevenlabs_api_key': elevenlabs_key,
        'adam_voice_id': 'polish_male_voice',  # Will configure after ElevenLabs setup
        'sample_rate': 22050,
        'chunk_duration': 5.0,
        'silence_threshold': 0.01
    }


if __name__ == "__main__":
    # Test voice interface
    print("🧪 Testing Voice Interface...")
    
    # This would need actual configuration
    # config = create_voice_config("your-openai-key", "your-elevenlabs-key")
    # voice_interface = VoiceInterface(config)
    
    print("✅ Voice Interface module loaded successfully!") 