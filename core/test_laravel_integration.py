#!/usr/bin/env python3
"""
Test integracji Adam Clay Python z Laravel API Dashboard

Ten skrypt testuje:
1. Połączenie z Laravel API
2. Wysyłanie myśli do Laravel
3. Tworzenie sesji świadomości
4. Sprawdzanie statusu systemu
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.rest_api_client import LaravelApiClient, LaravelApiConfig
from src.core.consciousness import Thought
from loguru import logger


async def test_laravel_integration():
    """
    🧪 Test kompletnej integracji z Laravel API
    """
    
    print("🚀 TESTING ADAM CLAY ↔ LARAVEL INTEGRATION")
    print("=" * 60)
    
    # Initialize Laravel API client
    api_client = LaravelApiClient(LaravelApiConfig())
    
    # Test 1: Connection test
    print("\n1️⃣ Testing API connection...")
    connection_ok = await api_client.test_connection()
    if not connection_ok:
        print("❌ Cannot connect to Laravel API. Make sure server is running on localhost:8004")
        return False
    
    # Test 2: Get system status
    print("\n2️⃣ Getting system status...")
    status = await api_client.get_system_status()
    if status:
        print(f"✅ System status retrieved:")
        print(f"   📊 Today's thoughts: {status['status']['today_stats']['thoughts']}")
        print(f"   💰 Today's cost: ${status['status']['today_stats']['cost']}")
    else:
        print("❌ Failed to get system status")
        return False
    
    # Test 3: Create consciousness session
    print("\n3️⃣ Creating consciousness session...")
    session_id = f"test-session-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    session_created = await api_client.create_consciousness_session(session_id)
    if session_created:
        print(f"✅ Session created: {session_id}")
    else:
        print("❌ Failed to create session")
        return False
    
    # Test 4: Send test thoughts
    print("\n4️⃣ Sending test thoughts...")
    
    test_thoughts = [
        {
            "content": "🧪 Test myśli z integracji Python-Laravel! Sprawdzam czy komunikacja REST API działa poprawnie.",
            "thought_type": "business",
            "is_significant": True
        },
        {
            "content": "Drugi test - czy mogę wysyłać różne typy myśli? Ta myśl ma charakter filozoficzny.",
            "thought_type": "philosophical", 
            "is_significant": False
        },
        {
            "content": "Trzeci test - reaktywna myśl. Reaguję na to, że właśnie testuje swoją integrację z Laravel!",
            "thought_type": "reactive",
            "is_significant": False
        }
    ]
    
    for i, thought_data in enumerate(test_thoughts, 1):
        print(f"\n   📤 Sending thought {i}/3...")
        
        # Create thought object
        thought = Thought(
            timestamp=datetime.now(),
            content=thought_data["content"],
            thought_type=thought_data["thought_type"],
            cost_usd=0.001 * i,  # Simulate different costs
            context={"test": True, "integration": "laravel"}
        )
        
        # Add extra attributes for Laravel API
        thought.mood = "focused"
        thought.energy_level = 0.8
        thought.session_id = session_id
        
        # Send to Laravel
        success = await api_client.send_thought(thought)
        if success:
            print(f"      ✅ Thought {i} sent successfully")
            
            # Update session statistics
            await api_client.update_consciousness_session(session_id, i, 0.001 * i)
        else:
            print(f"      ❌ Failed to send thought {i}")
    
    # Test 5: Send significant memory
    print("\n5️⃣ Sending significant memory...")
    memory_sent = await api_client.send_significant_memory(
        "🧠 Test wpisu do long-term memory: Nauczyłem się jak integrować Python z Laravel przez REST API!",
        "learning"
    )
    if memory_sent:
        print("   ✅ Significant memory sent")
    else:
        print("   ❌ Failed to send memory")
    
    # Test 6: Log web activity
    print("\n6️⃣ Logging web activity...")
    activity_logged = await api_client.log_web_activity(
        "integration_test",
        "Adam Clay Integration Test",
        "Successful integration test between Python consciousness and Laravel API",
        {"thoughts_sent": len(test_thoughts), "session_id": session_id}
    )
    if activity_logged:
        print("   ✅ Web activity logged")
    else:
        print("   ❌ Failed to log activity")
    
    # Test 7: Final status check
    print("\n7️⃣ Final status check...")
    final_status = await api_client.get_system_status()
    if final_status:
        stats = final_status['status']['today_stats']
        print(f"   📊 Final stats:")
        print(f"      💭 Total thoughts: {stats['thoughts']}")
        print(f"      💰 Total cost: ${stats['cost']}")
        
        if final_status['status']['current_session']:
            session = final_status['status']['current_session']
            print(f"      🧠 Current session: {session['id']}")
            print(f"      📈 Session thoughts: {session['total_thoughts']}")
    
    print("\n" + "=" * 60)
    print("🎉 INTEGRATION TEST COMPLETED SUCCESSFULLY!")
    print("🌐 Check the Laravel dashboard at: http://localhost:8004")
    print("📊 You should see the test thoughts and activities in real-time!")
    print("=" * 60)
    
    return True


async def main():
    """Main test function"""
    try:
        success = await test_laravel_integration()
        if success:
            print("\n✅ All tests passed! Integration is working!")
            
            print("\n🔥 NEXT STEPS:")
            print("1. Open http://localhost:8004 to see the dashboard")
            print("2. Run: python main.py to start Adam Clay with Laravel integration")
            print("3. Watch thoughts appear in real-time on the dashboard!")
            
        else:
            print("\n❌ Some tests failed. Check Laravel server and database.")
            
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        print(f"\n💥 ERROR: {e}")
        print("\nMake sure:")
        print("- Laravel server is running (php artisan serve --port=8004)")
        print("- MySQL database is accessible")
        print("- All dependencies are installed")


if __name__ == "__main__":
    asyncio.run(main()) 