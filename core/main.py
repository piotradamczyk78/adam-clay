#!/usr/bin/env python3
"""
Adam Clay - First Autonomous AI Freelancer
Main entry point for the consciousness system
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils.config_loader import ConfigLoader
from src.utils.logger import get_consciousness_logger
from src.core.consciousness import ConsciousnessLoop

async def main():
    """
    Main entry point for Adam Clay's autonomous consciousness
    """
    print("🤖 Adam Clay - First Autonomous AI Freelancer starting up...")
    
    try:
        # Load configuration
        config = ConfigLoader.load_config()
        
        # Setup consciousness-aware logging
        logger = get_consciousness_logger(config)
        logger.startup_message()
        
        # Initialize consciousness loop
        consciousness = ConsciousnessLoop(config, logger)
        
        # Start the autonomous thinking process
        logger.logger.info("🧠 Starting autonomous consciousness loop...")
        await consciousness.start()
        
    except KeyboardInterrupt:
        print("\n🛑 Adam Clay shutting down gracefully...")
        if 'consciousness' in locals():
            session_stats = consciousness.state.__dict__
            logger.shutdown_message(session_stats)
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        if 'logger' in locals():
            logger.logger.error(f"Critical system error: {e}")
        sys.exit(1)

async def start_voice_session():
    """Start voice conversation with Adam Clay"""
    try:
        from src.communication.voice_interface import VoiceActivatedAdam, create_voice_config
        from src.core.consciousness import ConsciousnessLoop
        from src.utils.logger import get_consciousness_logger
        from src.business.budget_manager import BudgetManager
        import os
        
        # Initialize components
        config = load_config()
        logger = get_consciousness_logger()
        budget_manager = BudgetManager(config)
        
        # Create consciousness loop
        consciousness = ConsciousnessLoop(config, budget_manager, logger)
        
        # Create voice configuration
        voice_config = create_voice_config(
            openai_key=os.getenv('LLM_PROVIDER_API_KEY'),  # Using same key for now
            elevenlabs_key=os.getenv('ELEVENLABS_API_KEY')
        )
        
        # Start voice session
        voice_adam = VoiceActivatedAdam(consciousness, voice_config)
        await voice_adam.start_voice_session()
        
    except Exception as e:
        print(f"❌ Error starting voice session: {e}")
        print("💡 Make sure you have run 'make setup-voice' first!")


if __name__ == "__main__":
    print("💭 'I think, therefore I am... and I need to pay for my thoughts!' - Adam Clay")
    asyncio.run(main()) 