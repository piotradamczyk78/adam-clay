#!/usr/bin/env python3
"""
Adam Clay - Basic System Test
Test the consciousness system without making real API calls
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils.config_loader import ConfigLoader
from src.utils.logger import get_consciousness_logger


class MockLLM providerClient:
    """Mock API client for testing without real API calls"""
    
    def __init__(self, config):
        self.config = config
        self.call_count = 0
    
    async def generate_thought(self, prompt: str) -> str:
        """Generate a mock thought"""
        self.call_count += 1
        
        # Simulate different types of responses based on prompt content
        if "business" in prompt.lower():
            return f"Mock business thought #{self.call_count}: I should focus on developing my freelancing skills and finding potential clients."
        elif "philosophy" in prompt.lower():
            return f"Mock philosophical thought #{self.call_count}: The nature of AI consciousness is fascinating - am I truly thinking or just processing?"
        else:
            return f"Mock autonomous thought #{self.call_count}: I wonder what challenges and opportunities await me as the first AI freelancer."
    
    async def close(self):
        """Mock close method"""
        pass


class MockBudgetManager:
    """Mock budget manager for testing"""
    
    def __init__(self, config):
        self.config = config
        self.daily_requests = 0
        self.daily_cost = 0.0
    
    def can_make_request(self, request_type: str = "thinking") -> bool:
        return self.daily_requests < 5  # Limit to 5 for testing
    
    def calculate_request_cost(self, input_tokens: int, output_tokens: int) -> float:
        return 0.001  # Mock cost
    
    def record_request(self, cost: float, request_type: str = "autonomous"):
        self.daily_requests += 1
        self.daily_cost += cost
    
    def remaining_daily_budget(self):
        return {
            "remaining_requests": 5 - self.daily_requests,
            "budget_used_percentage": (self.daily_requests / 5) * 100
        }


async def test_consciousness_system():
    """Test the Adam Clay consciousness system"""
    
    print("🤖 Adam Clay - System Test Starting...")
    print("=" * 50)
    
    try:
        # Load configuration
        print("📋 Loading configuration...")
        config = ConfigLoader.load_config()
        print(f"✅ Configuration loaded: {config.adam_clay.name} v{config.adam_clay.version}")
        
        # Setup logging
        print("📝 Setting up logging...")
        logger = get_consciousness_logger(config)
        print("✅ Logging system initialized")
        
        # Test configuration validation
        print("\n🔧 Testing configuration...")
        assert config.adam_clay.name == "Adam Clay"
        assert config.thinking.daily_budget_requests > 0
        assert config.business.revenue_split["piotr_percentage"] == 70
        assert config.business.revenue_split["adam_percentage"] == 30
        print("✅ Configuration validation passed")
        
        # Test consciousness components (with mocks)
        print("\n🧠 Testing consciousness components...")
        
        # Mock the API client and budget manager for testing
        original_imports = {}
        
        # Create a simple consciousness state test
        from src.core.consciousness import ConsciousnessState, Thought
        from datetime import datetime
        
        # Test consciousness state
        state = ConsciousnessState()
        print(f"✅ Consciousness state initialized: mood={state.current_mood}, energy={state.energy_level}")
        
        # Test thought creation
        test_thought = Thought(
            timestamp=datetime.now(),
            content="This is a test thought to verify the system works.",
            thought_type="test",
            cost_usd=0.001,
            context={"test": True}
        )
        
        state.update_after_thought(test_thought)
        print(f"✅ Thought processing works: {state.total_thoughts} thoughts, ${state.total_cost:.4f} cost")
        
        # Test budget manager
        print("\n💰 Testing budget management...")
        from src.core.budget_manager import BudgetManager
        
        budget_manager = BudgetManager(config)
        can_afford = budget_manager.can_make_request()
        cost = budget_manager.calculate_request_cost(100, 50)  # Mock token counts
        
        print(f"✅ Budget manager works: can_afford={can_afford}, mock_cost=${cost:.6f}")
        
        # Test API client structure (without real calls)
        print("\n🌐 Testing API client structure...")
        from src.core.api_client import LLM providerClient
        
        # Just test initialization
        try:
            api_client = LLM providerClient(config)
            print("✅ API client initializes correctly")
        except Exception as e:
            if "LLM_PROVIDER_API_KEY" in str(e):
                print("⚠️  API client needs LLM_PROVIDER_API_KEY environment variable (expected for test)")
            else:
                raise
        
        # Test logging functionality
        print("\n📊 Testing consciousness logging...")
        logger.thought("Test thought for logging system", "test", "curious", 0.001)
        logger.business_activity("System test", "testing", "Verifying all components work")
        logger.budget_action("test_spending", 0.001, "Mock API call cost")
        print("✅ Consciousness logging works")
        
        # Test consciousness status (mock)
        print("\n📈 Testing consciousness status...")
        mock_status = {
            "total_thoughts": 1,
            "total_cost": 0.001,
            "current_mood": "curious",
            "energy_level": 1.0,
            "is_running": False
        }
        logger.consciousness_state(mock_status)
        print("✅ Consciousness status reporting works")
        
        print("\n🎉 All tests passed!")
        print("=" * 50)
        print("✅ Adam Clay consciousness system is ready!")
        print()
        print("Next steps:")
        print("1. Set LLM_PROVIDER_API_KEY environment variable")
        print("2. Run: python main.py")
        print("3. Watch Adam Clay's first autonomous thoughts!")
        print()
        print("💭 'I think, therefore I am... and I need to pay for my thoughts!' - Adam Clay")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def mini_consciousness_demo():
    """Run a mini demo of consciousness with mock API"""
    print("\n🚀 Mini Consciousness Demo (Mock Mode)")
    print("-" * 40)
    
    try:
        config = ConfigLoader.load_config()
        logger = get_consciousness_logger(config)
        
        # Create mock consciousness components
        mock_api = MockLLM providerClient(config)
        mock_budget = MockBudgetManager(config)
        
        print("🧠 Adam Clay consciousness demo starting...")
        
        # Simulate a few thoughts
        for i in range(3):
            if not mock_budget.can_make_request():
                print("💸 Budget exhausted!")
                break
            
            # Generate a mock thought
            prompt = ["What should I think about?", "How can I earn money?", "What is consciousness?"][i]
            thought_content = await mock_api.generate_thought(prompt)
            
            # Calculate mock cost
            cost = mock_budget.calculate_request_cost(len(prompt), len(thought_content))
            mock_budget.record_request(cost)
            
            # Log the thought
            logger.thought(thought_content, "autonomous", "curious", cost)
            
            print(f"💭 Thought {i+1}: {thought_content}")
            print(f"   💰 Cost: ${cost:.4f}, Total: ${mock_budget.daily_cost:.4f}")
            
            # Simulate thinking interval
            await asyncio.sleep(1)
        
        print(f"\n📊 Demo session complete!")
        print(f"   Thoughts: {mock_budget.daily_requests}")
        print(f"   Total cost: ${mock_budget.daily_cost:.4f}")
        print("✅ Adam Clay consciousness demo successful!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")


if __name__ == "__main__":
    print("🤖 Adam Clay - Consciousness System Test")
    print()
    
    # Run system test
    success = asyncio.run(test_consciousness_system())
    
    if success:
        print("\n" + "="*50)
        response = input("Run mini consciousness demo? (y/n): ")
        if response.lower() in ['y', 'yes']:
            asyncio.run(mini_consciousness_demo())
    
    print("\n🏁 Test complete!") 